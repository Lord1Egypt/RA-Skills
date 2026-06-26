"""Tests for Social Media Automation."""

import pytest
from pathlib import Path
import sys
import os

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# Test imports
def test_imports():
    """Test that all modules can be imported."""
    from social_media_automation.cli import app
    from social_media_automation.config import get_config
    from social_media_automation.storage.database import Database
    from social_media_automation.platforms.x import TwitterClient

    assert app is not None
    assert get_config is not None
    assert Database is not None
    assert TwitterClient is not None


def test_config_loading():
    """Test configuration loading."""
    from social_media_automation.config import SocialMediaConfig, PlatformConfig

    # Test default config
    config = SocialMediaConfig()
    assert config is not None
    assert config.openclaw.monitored_repos == []
    assert config.scheduling.timezone == "Asia/Tokyo"

    # Test platform config
    platform_config = PlatformConfig(
        enabled=True,
        rate_limit_posts_per_hour=50
    )

    assert platform_config.enabled is True
    assert platform_config.rate_limit_posts_per_hour == 50


def test_cli_app():
    """Test CLI app initialization."""
    from social_media_automation.cli import app

    assert app is not None
    assert app.info == "Social Media Automation with OpenClaw integration"
