"""
Tests for TwitterClient
"""

import pytest
from unittest.mock import Mock, patch

from social_media_automation.platforms.x.client import TwitterClient


@pytest.fixture
def mock_config():
    """Create a mock config"""
    config = Mock()
    config.twitter_bearer_token = "test_bearer_token"
    config.twitter_api_key = "test_api_key"
    config.twitter_api_secret = "test_api_secret"
    config.twitter_access_token = "test_access_token"
    config.twitter_access_secret = "test_access_secret"
    return config


@pytest.fixture
def mock_tweepy_client():
    """Create a mock Tweepy client"""
    with patch("social_media_automation.platforms.x.client.tweepy.Client") as mock:
        yield mock


def test_twitter_client_initialization(mock_config, mock_tweepy_client):
    """Test TwitterClient initialization"""
    client = TwitterClient(mock_config)

    assert client.config == mock_config
    mock_tweepy_client.assert_called_once()


def test_twitter_client_missing_bearer_token(mock_config):
    """Test TwitterClient initialization with missing bearer token"""
    mock_config.twitter_bearer_token = None

    with pytest.raises(ValueError, match="Twitter Bearer Token is not configured"):
        TwitterClient(mock_config)


def test_post_tweet(mock_config, mock_tweepy_client):
    """Test posting a tweet"""
    # Setup mock
    mock_client_instance = mock_tweepy_client.return_value
    mock_response = Mock()
    mock_response.data.id = "1234567890"
    mock_client_instance.create_tweet.return_value = mock_response

    # Execute
    client = TwitterClient(mock_config)
    response = client.post_tweet("Hello, world!")

    # Verify
    assert response.data.id == "1234567890"
    mock_client_instance.create_tweet.assert_called_once_with(text="Hello, world!")


def test_post_tweet_failure(mock_config, mock_tweepy_client):
    """Test posting a tweet with API error"""
    # Setup mock
    mock_client_instance = mock_tweepy_client.return_value
    mock_client_instance.create_tweet.side_effect = Exception("API Error")

    # Execute and verify
    client = TwitterClient(mock_config)
    with pytest.raises(Exception, match="API Error"):
        client.post_tweet("Hello, world!")


def test_get_user_info(mock_config, mock_tweepy_client):
    """Test getting user information"""
    # Setup mock
    mock_client_instance = mock_tweepy_client.return_value
    mock_response = Mock()
    mock_response.data.data = {"id": "1234567890", "username": "testuser"}
    mock_client_instance.get_user.return_value = mock_response

    # Execute
    client = TwitterClient(mock_config)
    user_info = client.get_user_info("testuser")

    # Verify
    assert user_info["username"] == "testuser"
    mock_client_instance.get_user.assert_called_once_with(username="testuser")


def test_delete_tweet(mock_config, mock_tweepy_client):
    """Test deleting a tweet"""
    # Setup mock
    mock_client_instance = mock_tweepy_client.return_value

    # Execute
    client = TwitterClient(mock_config)
    result = client.delete_tweet("1234567890")

    # Verify
    assert result is True
    mock_client_instance.delete_tweet.assert_called_once_with("1234567890")


def test_delete_tweet_failure(mock_config, mock_tweepy_client):
    """Test deleting a tweet with API error"""
    # Setup mock
    mock_client_instance = mock_tweepy_client.return_value
    mock_client_instance.delete_tweet.side_effect = Exception("API Error")

    # Execute and verify
    client = TwitterClient(mock_config)
    with pytest.raises(Exception, match="API Error"):
        client.delete_tweet("1234567890")
