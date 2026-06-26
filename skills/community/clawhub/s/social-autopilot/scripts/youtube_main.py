"""YouTube Shorts Quiz Bot — Entry point.

Usage:
    python -m bot.youtube_main              # Post one Short
    python -m bot.youtube_main --count 3    # Post 3 Shorts
    python -m bot.youtube_main --dry-run    # Generate video only (no upload)
"""

import argparse
import logging
import signal
import sys
from logging.handlers import RotatingFileHandler

from bot.csv_manager import get_next_question, get_unposted_count, mark_as_posted
from bot.html_video_generator import generate_html_video as generate_video
from bot.yt_config import LOGS_DIR
from bot.yt_shorts_poster import post_short

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
logger = logging.getLogger(__name__)

_shutdown = False


def _setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    root.addHandler(console)
    log_file = LOGS_DIR / "youtube.log"
    fh = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
    fh.setFormatter(logging.Formatter(LOG_FORMAT))
    root.addHandler(fh)


def _signal_handler(signum, frame):
    global _shutdown
    logger.info("Shutdown signal received — finishing current task...")
    _shutdown = True


def process_one(dry_run: bool = False) -> bool:
    """Process one video: generate → upload → comment.

    Args:
        dry_run: If True, only generate video without uploading

    Returns:
        bool: True if should continue processing more videos
    """
    result = get_next_question()
    if result is None:
        logger.info("No unposted questions remaining")
        return False

    index, question_data = result

    logger.info("── Step 1/2: Generating video ──")
    try:
        video_path = generate_video(question_data)
    except Exception:
        logger.exception("Video generation failed — skipping question %d", index)
        return True

    if dry_run:
        logger.info("── DRY RUN — skipping upload ──")
        logger.info("Video saved at: %s", video_path)
        logger.info("Question: %s", question_data.get("question", "")[:100])
        return True

    logger.info("── Step 2/2: Uploading to YouTube ──")
    try:
        video_id = post_short(video_path, question_data)
        logger.info("Successfully posted Short! Video ID: %s", video_id)
        logger.info("URL: https://youtube.com/shorts/%s", video_id)
    except Exception:
        logger.exception("YouTube upload failed — skipping question %d", index)
        return True

    mark_as_posted(index)

    try:
        video_path.unlink()
        logger.info("Cleaned up video file: %s", video_path)
    except OSError:
        logger.warning("Failed to delete video file: %s", video_path)

    return True


def main():
    _setup_logging()

    parser = argparse.ArgumentParser(description="YouTube Shorts Quiz Bot")
    parser.add_argument("--count", type=int, default=1, help="Number of Shorts to post")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate videos only, don't upload",
    )
    args = parser.parse_args()

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    remaining = get_unposted_count()
    logger.info("YouTube Shorts Bot started — %d unposted questions available", remaining)

    # First run will trigger OAuth flow
    if args.dry_run:
        logger.info("DRY RUN mode — videos will be generated but not uploaded")
    else:
        logger.info("Authenticating with YouTube (browser may open on first run)")

    posted = 0
    for i in range(args.count):
        if _shutdown:
            logger.info("Shutting down gracefully after %d Short(s)", posted)
            break
        logger.info("━━━ Processing Short %d/%d ━━━", i + 1, args.count)
        if not process_one(dry_run=args.dry_run):
            break
        posted += 1

    action = "generated" if args.dry_run else "posted"
    logger.info("Done! %d Short(s) %s", posted, action)


if __name__ == "__main__":
    main()
