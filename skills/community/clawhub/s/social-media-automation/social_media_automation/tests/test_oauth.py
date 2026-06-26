"""
Tests for OAuth functionality
"""

import pytest
from unittest.mock import Mock, patch

from social_media_automation.core.oauth import OAuthFlow


@pytest.fixture
def mock_config():
    """Create a mock config"""
    config = Mock()
    config.twitter_api_key = "test_api_key"
    config.twitter_api_secret = "test_api_secret"
    return config


def test_oauth_flow_initialization(mock_config):
    """Test OAuthFlow initialization"""
    flow = OAuthFlow(mock_config)

    assert flow.config == mock_config


def test_oauth_get_auth_url(mock_config):
    """Test getting authorization URL"""
    # Setup mock
    with patch("social_media_automation.core.oauth.tweepy.OAuth1UserHandler") as mock_tweepy:
        mock_handler = Mock()
        mock_handler.get_authorization_url.return_value = "https://twitter.com/oauth/authenticate?oauth_token=test_token"
        mock_tweepy.return_value = mock_handler

        # Execute
        flow = OAuthFlow(mock_config)
        auth_url = flow.get_auth_url()

        # Verify
        assert auth_url == "https://twitter.com/oauth/authenticate?oauth_token=test_token"
        mock_handler.get_authorization_url.assert_called_once()


def test_oauth_refresh_token(mock_config):
    """Test refreshing access token (placeholder for OAuth 2.0)"""
    # OAuth 1.0 doesn't support token refresh
    flow = OAuthFlow(mock_config)

    # OAuth 1.0 doesn't support refresh tokens
    access_token, access_token_secret = flow.refresh_token()

    # Should return empty strings and log warning
    assert access_token == ""
    assert access_token_secret == ""
