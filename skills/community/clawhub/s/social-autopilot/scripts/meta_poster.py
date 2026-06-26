"""Posts quiz content to a Facebook Page using the Graph API."""

import logging
import os
import time

import requests

logger = logging.getLogger(__name__)

GRAPH_API_VERSION = "v21.0"
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"
MAX_RETRIES = 2
RETRY_DELAY = 5  # seconds


def _post_with_retry(url: str, params: dict) -> str:
    """Make a POST request with retry logic. Returns the post/comment ID."""
    for attempt in range(1, MAX_RETRIES + 2):
        try:
            resp = requests.post(url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            post_id = str(data["id"])
            logger.info("Meta post created (id=%s, attempt=%d)", post_id, attempt)
            return post_id
        except Exception as e:
            logger.error("Meta API error (attempt %d/%d): %s", attempt, MAX_RETRIES + 1, e)
            if attempt <= MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                raise


def post_question(text: str) -> str | None:
    """Post a question to the Facebook Page feed. Returns post ID or None on failure."""
    try:
        page_id = os.environ["META_PAGE_ID"]
        access_token = os.environ["META_PAGE_ACCESS_TOKEN"]
        url = f"{GRAPH_API_BASE}/{page_id}/feed"
        params = {"message": text, "access_token": access_token}
        return _post_with_retry(url, params)
    except Exception as e:
        logger.error("Failed to post question to Meta: %s", e)
        return None


def post_answer(text: str, reply_to_post_id: str) -> str | None:
    """Post an answer as a comment on the previous post. Returns comment ID or None on failure."""
    try:
        access_token = os.environ["META_PAGE_ACCESS_TOKEN"]
        url = f"{GRAPH_API_BASE}/{reply_to_post_id}/comments"
        params = {"message": text, "access_token": access_token}
        return _post_with_retry(url, params)
    except Exception as e:
        logger.error("Failed to post answer to Meta: %s", e)
        return None
