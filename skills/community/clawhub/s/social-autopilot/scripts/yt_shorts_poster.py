"""YouTube Shorts uploader module.

This module handles uploading video files to YouTube as Shorts.
Videos are automatically classified as Shorts if they are:
- Vertical (9:16 aspect ratio)
- Under 60 seconds duration
"""

import logging
import time
from pathlib import Path

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from bot.yt_auth import get_authenticated_service
from bot.yt_config import (
    VIDEO_PRIVACY,
    YOUTUBE_CATEGORY_EDUCATION,
    build_description,
    build_title,
)

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
BACKOFF_BASE = 2


def build_answer_comment(question_data: dict) -> str:
    """Build answer comment text from question data."""
    answer_letter = question_data["answer"].strip().upper()
    answer_map = {"A": "option_a", "B": "option_b", "C": "option_c", "D": "option_d"}
    answer_key = answer_map.get(answer_letter, "option_a")
    answer_text = question_data[answer_key]
    explanation = question_data.get("explanation", "")

    comment = f"✅ Answer: {answer_letter}) {answer_text}"
    if explanation:
        comment += f"\n\n💡 Explanation:\n{explanation}"

    return comment


def upload_video(
    video_path: Path,
    question_data: dict,
    privacy: str = VIDEO_PRIVACY,
) -> str:
    """Upload video to YouTube as a Short.

    Args:
        video_path: Path to video file
        question_data: Question metadata for title/description
        privacy: Video privacy status ("public", "private", or "unlisted")

    Returns:
        str: YouTube video ID

    Raises:
        FileNotFoundError: If video file doesn't exist
        HttpError: If upload fails
    """
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    youtube = get_authenticated_service()

    title = build_title(question_data)
    description = build_description(question_data)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": [
                "UPSC",
                "IAS",
                "Civil Services",
                "Quiz",
                "Previous Year Question",
                "{BRAND_NAME}",
                "Shorts",
            ],
            "categoryId": YOUTUBE_CATEGORY_EDUCATION,
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(
        str(video_path),
        mimetype="video/mp4",
        resumable=True,
        chunksize=1024 * 1024,  # 1MB chunks
    )

    logger.info("Uploading video: %s", video_path.name)
    logger.info("Title: %s", title)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            request = youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media,
            )

            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    logger.info("Upload progress: %d%%", progress)

            video_id = response["id"]
            logger.info("Upload complete! Video ID: %s", video_id)
            logger.info("URL: https://youtube.com/shorts/%s", video_id)
            return video_id

        except HttpError as e:
            wait = BACKOFF_BASE**attempt
            logger.warning(
                "Upload failed (attempt %d/%d): %s — retrying in %ds",
                attempt,
                MAX_RETRIES,
                e,
                wait,
            )
            if attempt == MAX_RETRIES:
                raise
            time.sleep(wait)

    raise RuntimeError("Upload failed after all retries")


def comment_on_video(video_id: str, text: str) -> str:
    """Post a comment on a YouTube video.

    Args:
        video_id: YouTube video ID
        text: Comment text

    Returns:
        str: Comment ID

    Raises:
        HttpError: If comment posting fails
    """
    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "videoId": video_id,
            "topLevelComment": {
                "snippet": {
                    "textOriginal": text,
                }
            },
        }
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            request = youtube.commentThreads().insert(
                part="snippet",
                body=body,
            )
            response = request.execute()
            comment_id = response["id"]
            logger.info("Posted comment %s on video %s", comment_id, video_id)
            return comment_id

        except HttpError as e:
            wait = BACKOFF_BASE**attempt
            logger.warning(
                "Comment posting failed (attempt %d/%d): %s — retrying in %ds",
                attempt,
                MAX_RETRIES,
                e,
                wait,
            )
            if attempt == MAX_RETRIES:
                raise
            time.sleep(wait)

    raise RuntimeError("Comment posting failed after all retries")


def post_short(
    video_path: Path,
    question_data: dict,
    add_answer_comment: bool = True,
) -> str:
    """Upload a Short to YouTube and optionally comment with the answer.

    Args:
        video_path: Path to video file
        question_data: Question metadata
        add_answer_comment: Whether to post answer as comment

    Returns:
        str: YouTube video ID
    """
    video_id = upload_video(video_path, question_data)

    if add_answer_comment:
        try:
            comment_text = build_answer_comment(question_data)
            comment_on_video(video_id, comment_text)
        except Exception:
            logger.exception("Failed to post answer comment on %s", video_id)

    return video_id
