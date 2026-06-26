"""YouTube OAuth 2.0 authentication helper.

This module handles the OAuth flow for YouTube Data API access.
On first run, it will open a browser for user authorization.
Subsequent runs will use the saved token from youtube_token.json.

Supports both:
- Pickle format (local development)
- JSON format (GitHub Actions / CI/CD)
"""

import json
import logging
import os
import pickle
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from bot.yt_config import (
    CLIENT_SECRETS_FILE,
    TOKEN_FILE,
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    YOUTUBE_SCOPES,
)

logger = logging.getLogger(__name__)


def get_authenticated_service():
    """Authenticate and return YouTube API service object.

    Returns:
        googleapiclient.discovery.Resource: Authenticated YouTube API service

    Raises:
        FileNotFoundError: If client_secrets.json is missing
        Exception: If authentication fails
    """
    if not CLIENT_SECRETS_FILE.exists():
        raise FileNotFoundError(
            f"Missing {CLIENT_SECRETS_FILE}. "
            "Download it from Google Cloud Console and place it in the project root."
        )

    credentials = None

    # Load saved token if it exists (supports both pickle and JSON)
    if TOKEN_FILE.exists():
        logger.info("Loading saved credentials from %s", TOKEN_FILE)
        try:
            # Try pickle format first (local development)
            with open(TOKEN_FILE, "rb") as token:
                credentials = pickle.load(token)
        except (pickle.UnpicklingError, EOFError):
            # Fall back to JSON format (GitHub Actions)
            logger.info("Pickle failed, trying JSON format")
            with open(TOKEN_FILE, "r") as token:
                token_data = json.load(token)
                credentials = Credentials(
                    token=token_data.get("token"),
                    refresh_token=token_data.get("refresh_token"),
                    token_uri=token_data.get("token_uri"),
                    client_id=token_data.get("client_id"),
                    client_secret=token_data.get("client_secret"),
                    scopes=token_data.get("scopes"),
                )

    # If no valid credentials, authenticate
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            logger.info("Refreshing expired credentials")
            credentials.refresh(Request())
        else:
            logger.info("Starting OAuth flow (browser will open)")
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, YOUTUBE_SCOPES
            )
            credentials = flow.run_local_server(
                port=8080,
                prompt="consent",
                authorization_prompt_message="Please visit this URL to authorize: {url}",
            )

        # Save credentials for next run
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(credentials, token)
            logger.info("Saved credentials to %s", TOKEN_FILE)

    logger.info("Building YouTube API service")
    return build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        credentials=credentials,
    )


def revoke_credentials():
    """Revoke saved credentials (useful for testing or switching accounts)."""
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
        logger.info("Revoked credentials (deleted %s)", TOKEN_FILE)
    else:
        logger.info("No saved credentials to revoke")
