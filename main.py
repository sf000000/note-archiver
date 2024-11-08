import asyncio
import logging

from instagram_client import InstagramClient
from db import SupabaseClient
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MusicNoteArchiver:
    def __init__(self):
        self.ig_client = InstagramClient()
        self.db_client = SupabaseClient()

    async def process_new_notes(self):
        """
        Fetch and process new music notes
        """
        try:
            music_notes = await self.ig_client.get_music_notes()

            for note in music_notes:
                if not await self.db_client.note_exists(note["note_id"]):
                    if await self.db_client.save_music_note(note):
                        logger.info(
                            f"Saved new music note: {note['note_response_info']['music_note_response_info']['music_info']['music_asset_info']['title']}"
                        )

        except Exception as e:
            logger.error(f"Error processing music notes: {str(e)}")

    async def run(self):
        """
        Run the archiver
        """
        try:
            while True:
                await self.process_new_notes()
                await asyncio.sleep(settings.CHECK_INTERVAL)
        finally:
            await self.ig_client.close()


async def main():
    archiver = MusicNoteArchiver()
    await archiver.run()


if __name__ == "__main__":
    asyncio.run(main())
