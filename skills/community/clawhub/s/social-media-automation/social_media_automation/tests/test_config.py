"""
Additional unit tests for config validation
"""

import pytest
from social_media_automation.config import Config


def test_config_load_empty():
    """Test loading config with no values"""
    import os

    # Remove environment variables
    for key in list(os.environ.keys()):
        if key.startswith("TWITTER_") or key.startswith("BLUESKY_"):
            del os.environ[key]

    config = Config.load()

    # Should not crash
    assert config is not None
    assert config.twitter_bearer_token is None
    assert config.twitter_api_key is None


def test_config_validate_all_missing():
    """Test validation with all required fields missing"""
    import os

    # Remove environment variables
    for key in list(os.environ.keys()):
        if key.startswith("TWITTER_"):
            del os.environ[key]

    config = Config.load()
    is_valid, errors = config.validate()

    # Should fail validation
    assert is_valid is False
    assert len(errors) > 0


def test_config_validate_partial():
    """Test validation with partial config"""
    import os

    # Set only bearer token
    os.environ["TWITTER_BEARER_TOKEN"] = "test_token"

    config = Config.load()
    is_valid, errors = config.validate()

    # Should still fail (need API key)
    assert is_valid is False
    assert "API Key" in str(errors) or "api_key" in str(errors).lower()


def test_config_load_env():
    """Test loading config from environment variables"""
    import os

    # Set environment variables
    os.environ["TWITTER_BEARER_TOKEN"] = "test_bearer"
    os.environ["TWITTER_API_KEY"] = "test_key"
    os.environ["TWITTER_API_SECRET"] = "test_secret"

    config = Config.load()

    # Should load values
    assert config.twitter_bearer_token == "test_bearer"
    assert config.twitter_api_key == "test_key"
    assert config.twitter_api_secret == "test_secret"
