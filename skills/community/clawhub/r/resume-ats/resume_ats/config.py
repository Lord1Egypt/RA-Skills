"""
Configuration management for Resume/ATS Optimization
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

    # OpenAI API
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")

    # Resume Settings
    default_template: str = Field(default="modern", alias="DEFAULT_TEMPLATE")
    output_format: str = Field(default="pdf", alias="OUTPUT_FORMAT")
    font_size: int = Field(default=11, alias="FONT_SIZE")
    font_family: str = Field(default="Arial", alias="FONT_FAMILY")

    # Database
    db_path: str = Field(default="./data/resume_ats.db", alias="DB_PATH")


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

        # Check database path
        config = cls.load()
        db_dir = Path(config.db_path).parent
        if not db_dir.exists():
            errors.append(f"Database directory does not exist: {db_dir}")

        return len(errors) == 0, errors
