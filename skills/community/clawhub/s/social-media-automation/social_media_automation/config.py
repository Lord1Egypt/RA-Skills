"""
Configuration management for social media automation
"""

from pathlib import Path

import pydantic_settings
from pydantic import Field


class Settings(pydantic_settings.BaseSettings):
    """Application settings"""

    model_config = pydantic_settings.SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Twitter/X API
    twitter_bearer_token: str | None = Field(default=None, alias="TWITTER_BEARER_TOKEN")
    twitter_api_key: str | None = Field(default=None, alias="TWITTER_API_KEY")
    twitter_api_secret: str | None = Field(default=None, alias="TWITTER_API_SECRET")
    twitter_access_token: str | None = Field(default=None, alias="TWITTER_ACCESS_TOKEN")
    twitter_access_secret: str | None = Field(default=None, alias="TWITTER_ACCESS_SECRET")

    # Bluesky
    bluesky_handle: str | None = Field(default=None, alias="BLUESKY_HANDLE")
    bluesky_app_password: str | None = Field(default=None, alias="BLUESKY_APP_PASSWORD")

    # LinkedIn
    linkedin_access_token: str | None = Field(default=None, alias="LINKEDIN_ACCESS_TOKEN")

    # Database
    db_path: str = Field(default="./data/social_media.db", alias="DB_PATH")


class Config:
    """Configuration manager"""

    _instance: Settings | None = None

    @classmethod
    def load(cls) -> Settings:
        """Load configuration from environment"""
        if cls._instance is None:
            cls._instance = Settings()
        return cls._instance

    @classmethod
    def validate(cls) -> tuple[bool, list[str]]:
        """Validate required configuration"""
        errors = []

        # Check Twitter configuration
        if not cls.load().twitter_bearer_token:
            errors.append("Twitter Bearer Token is not configured")
        if not cls.load().twitter_api_key:
            errors.append("Twitter API Key is not configured")

        return len(errors) == 0, errors
