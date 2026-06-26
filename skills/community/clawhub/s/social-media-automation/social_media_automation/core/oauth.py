"""
OAuth 2.0 flow for Twitter API authentication
"""

import webbrowser
from typing import Any

import tweepy

from social_media_automation.config import Config
from social_media_automation.utils.logger import setup_logger

logger = setup_logger()


class OAuthFlow:
    """OAuth 2.0 flow handler"""

    def __init__(self, config: Config) -> None:
        """Initialize OAuth flow"""
        self.config = config

    def get_auth_url(self) -> str:
        """Get authentication URL"""
        # Twitter OAuth 2.0 flow
        oauth1_user_handler = tweepy.OAuth1UserHandler(
            consumer_key=self.config.twitter_api_key or "",
            consumer_secret=self.config.twitter_api_secret or "",
            callback="oob",
        )

        return oauth1_user_handler.get_authorization_url()

    def get_access_token(self, verifier: str) -> tuple[str, str]:
        """Get access token from verifier"""
        oauth1_user_handler = tweepy.OAuth1UserHandler(
            consumer_key=self.config.twitter_api_key or "",
            consumer_secret=self.config.twitter_api_secret or "",
            callback="oob",
        )

        access_token, access_token_secret = oauth1_user_handler.get_access_token(verifier)

        logger.info("Access token obtained successfully")
        return access_token, access_token_secret

    def interactive_auth(self) -> tuple[str, str]:
        """Interactive authentication flow"""
        logger.info("Starting interactive OAuth flow")

        # Get auth URL
        auth_url = self.get_auth_url()

        # Open browser
        logger.info(f"Opening browser: {auth_url}")
        webbrowser.open(auth_url)

        # Get verifier
        verifier = input("Enter the verifier code from the browser: ").strip()

        # Get access token
        access_token, access_token_secret = self.get_access_token(verifier)

        logger.info("Authentication successful")
        return access_token, access_token_secret

    def refresh_token(self) -> tuple[str, str]:
        """Refresh access token"""
        # Twitter OAuth 1.0a doesn't support token refresh
        # OAuth 2.0 would need refresh token implementation
        logger.warning("Token refresh not implemented for OAuth 1.0a")
        return "", ""


def save_tokens(access_token: str, access_token_secret: str, env_path: str = ".env") -> None:
    """Save tokens to .env file"""
    with open(env_path, "r") as f:
        lines = f.readlines()

    updated = False
    for i, line in enumerate(lines):
        if line.startswith("TWITTER_ACCESS_TOKEN="):
            lines[i] = f"TWITTER_ACCESS_TOKEN={access_token}\n"
            updated = True
        elif line.startswith("TWITTER_ACCESS_SECRET="):
            lines[i] = f"TWITTER_ACCESS_SECRET={access_token_secret}\n"
            updated = True

    with open(env_path, "w") as f:
        f.writelines(lines)

    logger.info("Tokens saved to .env file")
