"""Instagram Quiz Reel Bot — Entry point.

Usage:
    python -m bot.instagram_main              # Post one reel
    python -m bot.instagram_main --count 3    # Post 3 reels
    python -m bot.instagram_main --dry-run    # Generate video only
"""

import argparse
import logging
import signal
import sys
from logging.handlers import RotatingFileHandler

from bot.csv_manager import get_next_question, get_unposted_count, mark_as_posted
from bot.ig_config import LOGS_DIR, build_caption
from bot.ig_reel_poster import post_reel
from bot.r2_uploader import upload_to_r2
from bot.html_video_generator import generate_html_video as generate_video

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
logger = logging.getLogger(__name__)

_shutdown = False


def _setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    root.addHandler(console)
    log_file = LOGS_DIR / "instagram.log"
    fh = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
    fh.setFormatter(logging.Formatter(LOG_FORMAT))
    root.addHandler(fh)


def _signal_handler(signum, frame):
    global _shutdown
    logger.info("Shutdown signal received — finishing current task...")
    _shutdown = True


def process_one(dry_run: bool = False) -> bool:
    result = get_next_question()
    if result is None:
        logger.info("No unposted questions remaining")
        return False

    index, question_data = result
    caption = build_caption(question_data)

    logger.info("── Step 1/3: Generating video ──")
    try:
        video_path = generate_video(question_data)
    except Exception:
        logger.exception("Video generation failed — skipping question %d", index)
        return True

    if dry_run:
        logger.info("── DRY RUN — skipping upload and post ──")
        logger.info("Caption:\n%s", caption)
        logger.info("Video saved at: %s", video_path)
        return True

    logger.info("── Step 2/3: Uploading to R2 ──")
    try:
        public_url = upload_to_r2(video_path)
    except Exception:
        logger.exception("R2 upload failed — skipping question %d", index)
        return True

    logger.info("── Step 3/3: Posting to Instagram ──")
    try:
        media_id = post_reel(public_url, caption, question_data)
        logger.info("Successfully posted reel! Media ID: %s", media_id)
    except Exception:
        logger.exception("Instagram posting failed — skipping question %d", index)
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

    parser = argparse.ArgumentParser(description="Instagram Quiz Reel Bot")
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    remaining = get_unposted_count()
    logger.info("Instagram Reel Bot started — %d unposted questions available", remaining)

    posted = 0
    for i in range(args.count):
        if _shutdown:
            logger.info("Shutting down gracefully after %d reel(s)", posted)
            break
        logger.info("━━━ Processing reel %d/%d ━━━", i + 1, args.count)
        if not process_one(dry_run=args.dry_run):
            break
        posted += 1

    action = "generated" if args.dry_run else "posted"
    logger.info("Done! %d reel(s) %s", posted, action)


if __name__ == "__main__":
    main()
