import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    IG_USER_AGENT: str = (
        "Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0"
    )
    IG_API_URL: str = "https://www.instagram.com/graphql/query"
    IG_APP_ID: str = "936619743392459"
    IG_CSRF_TOKEN: str = os.getenv("IG_CSRF_TOKEN")
    IG_SESSION_ID: str = os.getenv("IG_SESSION_ID")

    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")

    CHECK_INTERVAL: int = 600  # 10 minutes

    class Config:
        env_file = ".env"


settings = Settings()
