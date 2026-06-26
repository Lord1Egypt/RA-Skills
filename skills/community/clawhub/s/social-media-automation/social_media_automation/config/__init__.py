"""Configuration management for Social Media Automation."""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from python_dotenv import load_dotenv

# Load environment variables
PROJECT_DIR = Path(__file__).parent.parent
ENV_FILE = PROJECT_DIR / ".env"
load_dotenv(ENV_FILE)


class PlatformConfig(BaseModel):
    """Configuration for a social media platform."""

    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    access_token: Optional[str] = None
    access_secret: Optional[str] = None
    enabled: bool = True
    rate_limit_posts_per_hour: int = Field(default=50, ge=1)


class OpenClawConfig(BaseModel):
    """OpenClaw integration configuration."""

    monitored_repos: list[str] = Field(default_factory=list)
    poll_interval: int = Field(default=300, ge=60)  # 5 minutes
    content_templates: Dict[str, str] = Field(default_factory=dict)
    bot_channels: Dict[str, str] = Field(default_factory=dict)
    auto_post: bool = Field(default=False)
    platforms: list[str] = Field(default_factory=lambda: ["x", "linkedin"])


class SchedulingConfig(BaseModel):
    """Scheduling configuration."""

    timezone: str = Field(default="Asia/Tokyo")
    default_post_time: str = Field(default="09:00")
    batch_size: int = Field(default=5, ge=1, le=20)
    retry_attempts: int = Field(default=3, ge=1, le=10)
    retry_delay: int = Field(default=60, ge=10, le=600)


class DatabaseConfig(BaseModel):
    """Database configuration."""

    path: str = Field(default="~/.social-media/data.db")
    backup_enabled: bool = Field(default=True)
    backup_interval: int = Field(default=86400, ge=3600)  # 24 hours


class LoggingConfig(BaseModel):
    """Logging configuration."""

    level: str = Field(default="INFO")
    file: str = Field(default="~/.social-media/logs/app.log")
    max_size: int = Field(default=10485760, ge=10240)  # 10MB
    backup_count: int = Field(default=5, ge=1, le=10)


class SocialMediaConfig(BaseModel):
    """Main configuration for Social Media Automation."""

    openclaw: OpenClawConfig
    platforms: Dict[str, PlatformConfig] = Field(default_factory=dict)
    scheduling: SchedulingConfig
    database: DatabaseConfig
    logging: LoggingConfig


def load_config(config_path: Optional[Path] = None) -> SocialMediaConfig:
    """Load configuration from file.

    Args:
        config_path: Path to YAML config file

    Returns:
        SocialMediaConfig object
    """
    if config_path is None:
        config_path = PROJECT_DIR / "social-media.yaml"

    if config_path.exists():
        try:
            import yaml
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f)

            # Convert platform configs to PlatformConfig objects
            platform_configs = {}
            for platform, platform_data in config_data.get('platforms', {}).items():
                platform_configs[platform] = PlatformConfig(**platform_data)

            # Create full config
            config = SocialMediaConfig(
                openclaw=OpenClawConfig(**config_data.get('openclaw', {})),
                platforms=platform_configs,
                scheduling=SchedulingConfig(**config_data.get('scheduling', {})),
                database=DatabaseConfig(**config_data.get('database', {})),
                logging=LoggingConfig(**config_data.get('logging', {}))
            )

            return config

        except Exception as e:
            print(f"[red]Failed to load config: {e}[/red]")
            return SocialMediaConfig()
    else:
        # Create default config from environment variables
        return SocialMediaConfig(
            platforms={
                "x": PlatformConfig(
                    api_key=os.getenv("X_API_KEY"),
                    api_secret=os.getenv("X_API_SECRET"),
                    access_token=os.getenv("X_ACCESS_TOKEN"),
                    access_secret=os.getenv("X_ACCESS_SECRET"),
                ),
                "linkedin": PlatformConfig(
                    client_id=os.getenv("LINKEDIN_CLIENT_ID"),
                    client_secret=os.getenv("LINKEDIN_CLIENT_SECRET"),
                    access_token=os.getenv("LINKEDIN_ACCESS_TOKEN"),
                )
            }
        )


def get_config() -> SocialMediaConfig:
    """Get current configuration.

    Returns:
        SocialMediaConfig object
    """
    config = load_config()
    return config
