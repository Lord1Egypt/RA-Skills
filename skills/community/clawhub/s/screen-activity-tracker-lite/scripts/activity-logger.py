#!/usr/bin/env python3
"""
Local-only activity logger. Writes to markdown files, no SiYuan dependency.
Usage: python3 activity-logger.py <screenshot_path> <date> <time> <description>
"""

import os
import sys
import json
import shutil
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "..", "config.json")


def load_config():
    config = {
        "output_dir": os.path.expanduser("~/screen-activity"),
        "mlx_url": "",
        "interval_minutes": 5,
        "keep_days": 7,
    }
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                user_cfg = json.load(f)
            config.update(user_cfg)
            if "output_dir" in config:
                config["output_dir"] = os.path.expanduser(config["output_dir"])
        except (json.JSONDecodeError, IOError):
            pass
    return config


def ensure_dirs(output_dir, date_str):
    daily_dir = os.path.join(output_dir, "screenshots", date_str)
    os.makedirs(daily_dir, exist_ok=True)
    return daily_dir


def write_log(output_dir, date_str, time_str, description, screenshot_rel_path=None):
    """Append an entry to today's markdown file."""
    md_path = os.path.join(output_dir, f"{date_str}.md")

    # Create file with header if new
    is_new = not os.path.exists(md_path)
    if is_new:
        with open(md_path, "w") as f:
            f.write(f"# {date_str} 屏幕活动记录\n\n")

    # Build entry
    entry = f"- **{time_str}** {description}\n"
    if screenshot_rel_path:
        # Use relative path from the markdown file's location
        entry += f"  ![截图]({screenshot_rel_path})\n"
    entry += "\n"

    with open(md_path, "a") as f:
        f.write(entry)

    return md_path


def cleanup_old_screenshots(output_dir, keep_days):
    """Remove screenshot directories older than keep_days."""
    if keep_days <= 0:
        return  # Keep forever

    screenshots_dir = os.path.join(output_dir, "screenshots")
    if not os.path.exists(screenshots_dir):
        return

    cutoff = datetime.now() - timedelta(days=keep_days)
    for item in os.listdir(screenshots_dir):
        item_path = os.path.join(screenshots_dir, item)
        if not os.path.isdir(item_path):
            continue
        try:
            item_date = datetime.strptime(item, "%Y-%m-%d")
            if item_date < cutoff:
                shutil.rmtree(item_path)
                print(f"   清理旧截图: {item}")
        except ValueError:
            pass


def main():
    if len(sys.argv) < 4:
        print("Usage: python3 activity-logger.py <screenshot_path> <date> <time> <description>")
        sys.exit(1)

    screenshot_path = sys.argv[1]
    date_str = sys.argv[2]
    time_str = sys.argv[3]
    description = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else ""

    config = load_config()
    output_dir = config["output_dir"]
    keep_days = config.get("keep_days", 7)
    screenshot_rel = None
    screenshot_dir = ensure_dirs(output_dir, date_str)

    # Copy screenshot into daily folder
    if screenshot_path and screenshot_path != "NONE" and os.path.exists(screenshot_path):
        ext = os.path.splitext(screenshot_path)[1] or ".png"
        clean_time = time_str.replace(":", "")
        dest_name = f"{date_str.replace('-', '')}_{clean_time}{ext}"
        dest_path = os.path.join(screenshot_dir, dest_name)
        shutil.copy2(screenshot_path, dest_path)
        # Relative path for markdown link
        screenshot_rel = f"screenshots/{date_str}/{dest_name}"

    # Write to markdown
    md_path = write_log(output_dir, date_str, time_str, description, screenshot_rel)
    print(f"OK | {date_str} {time_str} | {description} | {md_path}")

    # Cleanup old screenshots
    cleanup_old_screenshots(output_dir, keep_days)


if __name__ == "__main__":
    main()
