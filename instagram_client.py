import logging
import httpx

from tenacity import retry, stop_after_attempt, wait_exponential
from config import settings
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InstagramClient:
    def __init__(self):
        self.base_url = settings.IG_API_URL
        self.client = httpx.AsyncClient(timeout=30.0)

    def _get_default_headers(self) -> Dict[str, str]:
        return {
            "User-Agent": settings.IG_USER_AGENT,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-FB-Friendly-Name": "IGDInboxTrayQuery",
            "X-BLOKS-VERSION-ID": "a2e134f798301e28e517956976df910b8fa9c85f9187c2963f77cdd733f46130",
            "X-CSRFToken": settings.IG_CSRF_TOKEN,
            "X-IG-App-ID": settings.IG_APP_ID,
            "Origin": "https://www.instagram.com",
            "Referer": "https://www.instagram.com/direct/inbox/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }

    def _get_default_cookies(self) -> Dict[str, str]:
        return {
            "csrftoken": settings.IG_CSRF_TOKEN,
            "sessionid": settings.IG_SESSION_ID,
        }

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def fetch_inbox_tray(self) -> Dict[str, Any]:
        """
        Fetch Instagram inbox tray data.
        """
        try:
            data = {
                "av": "17841404879894766",
                "__d": "www",
                "__user": "0",
                "__a": "1",
                "variables": "{}",
                "doc_id": "8012364548831822",
            }

            response = await self.client.post(
                self.base_url,
                headers=self._get_default_headers(),
                cookies=self._get_default_cookies(),
                data=data,
            )
            response.raise_for_status()

            return response.json()

        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise

    def _extract_music_notes(
        self, response_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Extract music notes from the response data
        """
        try:
            items = response_data["data"]["response"]["inbox_tray_items"]
            music_notes = []

            for item in items:
                if (
                    item["inbox_tray_item_type"] == "note"
                    and "music_note_response_info"
                    in item["note_dict"]["note_response_info"]
                ):
                    note_dict = item["note_dict"]
                    note_dict["note_id"] = item["inbox_tray_item_id"]
                    music_notes.append(note_dict)

            return music_notes
        except Exception as e:
            logger.error(f"Failed to extract music notes: {str(e)}")
            return []

    async def get_music_notes(self) -> List[Dict[str, Any]]:
        """
        Fetch and extract music notes
        """
        response_data = await self.fetch_inbox_tray()
        return self._extract_music_notes(response_data)

    async def close(self):
        await self.client.aclose()
