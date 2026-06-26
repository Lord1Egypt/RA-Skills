"""Posts quiz content to X (Twitter) using tweepy."""

import logging
import os
import time

import tweepy

logger = logging.getLogger(__name__)

MAX_RETRIES = 2
RETRY_DELAY = 5  # seconds


def _get_client() -> tweepy.Client:
    """Create an authenticated tweepy Client using env vars."""
    return tweepy.Client(
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )


def _get_v1_api() -> tweepy.API:
    """Create an authenticated tweepy v1.1 API (needed for media upload)."""
    auth = tweepy.OAuth1UserHandler(
        os.environ["X_API_KEY"],
        os.environ["X_API_SECRET"],
        os.environ["X_ACCESS_TOKEN"],
        os.environ["X_ACCESS_TOKEN_SECRET"],
    )
    return tweepy.API(auth)


def _post_with_retry(client: tweepy.Client, text: str, reply_to: str | None = None) -> str:
    """Post a tweet with retry logic. Returns the tweet ID as a string."""
    for attempt in range(1, MAX_RETRIES + 2):
        try:
            kwargs = {"text": text}
            if reply_to:
                kwargs["in_reply_to_tweet_id"] = reply_to
            response = client.create_tweet(**kwargs)
            tweet_id = str(response.data["id"])
            logger.info("Tweet posted (id=%s, attempt=%d)", tweet_id, attempt)
            return tweet_id
        except Exception as e:
            logger.error("X API error (attempt %d/%d): %s", attempt, MAX_RETRIES + 1, e)
            if attempt <= MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                raise


def post_question(text: str) -> str | None:
    """Post a question tweet. Returns tweet ID or None on failure."""
    try:
        client = _get_client()
        return _post_with_retry(client, text)
    except Exception as e:
        logger.error("Failed to post question to X: %s", e)
        return None


def post_answer(text: str, reply_to_tweet_id: str) -> str | None:
    """Post an answer as a reply tweet. Returns tweet ID or None on failure."""
    try:
        client = _get_client()
        return _post_with_retry(client, text, reply_to=reply_to_tweet_id)
    except Exception as e:
        logger.error("Failed to post answer to X: %s", e)
        return None


def post_thread(tweets: list[str]) -> list[str]:
    """Post a thread (list of tweets). Each tweet replies to the previous. Returns list of tweet IDs."""
    if not tweets:
        return []
    client = _get_client()
    ids = []
    reply_to = None
    for i, text in enumerate(tweets):
        try:
            tweet_id = _post_with_retry(client, text, reply_to=reply_to)
            ids.append(tweet_id)
            reply_to = tweet_id
            logger.info("Thread tweet %d/%d posted (id=%s)", i + 1, len(tweets), tweet_id)
            if i < len(tweets) - 1:
                import time as _time
                _time.sleep(2)  # small delay between tweets
        except Exception as e:
            logger.error("Thread tweet %d failed: %s", i + 1, e)
            break
    return ids


def post_image(image_path: str, text: str = "") -> str | None:
    """Post a tweet with an image. Returns tweet ID or None on failure."""
    try:
        api = _get_v1_api()
        media = api.media_upload(image_path)
        logger.info("Media uploaded (id=%s)", media.media_id)

        client = _get_client()
        kwargs = {"media_ids": [media.media_id]}
        if text:
            kwargs["text"] = text
        response = client.create_tweet(**kwargs)
        tweet_id = str(response.data["id"])
        logger.info("Image tweet posted (id=%s)", tweet_id)
        return tweet_id
    except Exception as e:
        logger.error("Failed to post image to X: %s", e)
        return None
