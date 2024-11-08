import logging

from supabase import create_client
from config import settings
from typing import Dict, Any

logger = logging.getLogger(__name__)


class SupabaseClient:
    def __init__(self):
        self.client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    async def save_music_note(self, note_dict: Dict[str, Any]) -> bool:
        """
        Save a music note to Supabase
        """
        try:
            music_info = note_dict["note_response_info"]["music_note_response_info"][
                "music_info"
            ]["music_asset_info"]

            data = {
                "note_id": note_dict["note_id"],
                "created_at": note_dict["created_at"],
                "title": music_info["title"],
                "artist": music_info["display_artist"],
                "is_explicit": music_info["is_explicit"],
                "audio_cluster_id": music_info["audio_cluster_id"],
                "raw_data": note_dict,
            }

            self.client.table("music_notes").insert(data).execute()
            return True

        except Exception as e:
            logger.error(f"Failed to save music note: {str(e)}")
            return False

    async def note_exists(self, note_id: str) -> bool:
        """
        Check if a note already exists in the database
        """
        try:
            result = (
                self.client.table("music_notes")
                .select("note_id")
                .eq("note_id", note_id)
                .execute()
            )
            return len(result.data) > 0
        except Exception as e:
            logger.error(f"Failed to check note existence: {str(e)}")
            return False
