import logging
import time

import requests

from bot.ig_config import (
    INSTAGRAM_ACCESS_TOKEN,
    INSTAGRAM_API_BASE,
    INSTAGRAM_API_VERSION,
    INSTAGRAM_USER_ID,
)

logger = logging.getLogger(__name__)

API_URL = f"{INSTAGRAM_API_BASE}/{INSTAGRAM_API_VERSION}"

MAX_RETRIES = 3
BACKOFF_BASE = 2
POLL_INTERVAL = 30
POLL_TIMEOUT = 600


def _api_request(method: str, url: str, max_retries: int = MAX_RETRIES, **kwargs) -> dict:
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.request(method, url, timeout=30, **kwargs)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            wait = BACKOFF_BASE ** attempt
            logger.warning(
                "API request failed (attempt %d/%d): %s — retrying in %ds",
                attempt, max_retries, e, wait,
            )
            if attempt == max_retries:
                raise
            time.sleep(wait)
    raise RuntimeError("API request failed after all retries")


def create_container(video_url: str, caption: str) -> str:
    url = f"{API_URL}/{INSTAGRAM_USER_ID}/media"
    params = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "share_to_feed": "true",
        "access_token": INSTAGRAM_ACCESS_TOKEN,
    }
    data = _api_request("POST", url, params=params)
    container_id = data["id"]
    logger.info("Created container: %s", container_id)
    return container_id


def poll_container_status(container_id: str) -> str:
    url = f"{API_URL}/{container_id}"
    params = {
        "fields": "status_code",
        "access_token": INSTAGRAM_ACCESS_TOKEN,
    }
    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        if elapsed > POLL_TIMEOUT:
            raise TimeoutError(
                f"Container {container_id} not ready after {POLL_TIMEOUT}s"
            )
        data = _api_request("GET", url, params=params)
        status = data.get("status_code", "UNKNOWN")
        logger.info("Container %s status: %s (%.0fs elapsed)", container_id, status, elapsed)
        if status == "FINISHED":
            return status
        if status == "ERROR":
            raise RuntimeError(f"Container {container_id} processing failed: ERROR")
        time.sleep(POLL_INTERVAL)


def publish_container(container_id: str) -> str:
    url = f"{API_URL}/{INSTAGRAM_USER_ID}/media_publish"
    params = {
        "creation_id": container_id,
        "access_token": INSTAGRAM_ACCESS_TOKEN,
    }
    data = _api_request("POST", url, params=params)
    media_id = data["id"]
    logger.info("Published reel: %s", media_id)
    return media_id


def comment_on_media(media_id: str, text: str) -> str:
    url = f"{API_URL}/{media_id}/comments"
    params = {
        "message": text,
        "access_token": INSTAGRAM_ACCESS_TOKEN,
    }
    data = _api_request("POST", url, params=params)
    comment_id = data["id"]
    logger.info("Posted comment %s on media %s", comment_id, media_id)
    return comment_id


def build_answer_comment(question_data: dict) -> str:
    answer_letter = question_data["answer"].strip().upper()
    answer_map = {"A": "option_a", "B": "option_b", "C": "option_c", "D": "option_d"}
    answer_key = answer_map.get(answer_letter, "option_a")
    answer_text = question_data[answer_key]
    explanation = question_data.get("explanation", "")
    comment = f"\u2705 Answer: {answer_letter}) {answer_text}"
    if explanation:
        comment += f"\n\n\U0001f4a1 Explanation:\n{explanation}"
    return comment


def post_reel(video_url: str, caption: str, question_data: dict | None = None) -> str:
    container_id = create_container(video_url, caption)
    poll_container_status(container_id)
    media_id = publish_container(container_id)

    if question_data:
        try:
            comment_text = build_answer_comment(question_data)
            comment_on_media(media_id, comment_text)
        except Exception:
            logger.exception("Failed to post answer comment on %s", media_id)

    return media_id
