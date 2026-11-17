#!/usr/bin/env python3
"""
Screenshot planning script.
Determines screenshot timestamps from video duration and emits ffmpeg commands.

Usage:
1. Edit the SECTIONS and LEVEL_DIRS definitions below.
2. Run the script.

Outputs:
  _screenshot_plan.json
  _batch_screenshots.sh
"""

import json
import os
import re
import subprocess

# ============ Configuration ============

COURSE_DIR = "<COURSE_DIR>"
LEVEL_DIRS = {
    "L1": os.path.join(COURSE_DIR, "<Level 1 dir>"),
    "L2": os.path.join(COURSE_DIR, "<Level 2 dir>"),
}

SECTIONS = {
    "S01": {
        "title": "<Section Title>",
        "level": "L1",
        "videos": [(1, "Video Name")],
    },
}

ASSET_DIR = "assets/<course-slug>/"

# ============ Screenshot strategy ============

def frames_for_duration(seconds, video_name=""):
    name_lower = video_name.lower()
    if any(keyword in name_lower for keyword in ["intro", "overview", "wrap-up", "summary", "recap"]):
        return 0
    if seconds < 30:
        return 1
    if seconds < 120:
        return 2
    return 3

def interpolate_timestamps(duration, frame_count):
    if frame_count == 0:
        return []
    if frame_count == 1:
        return [duration * 0.3]
    step = duration / (frame_count + 1)
    return [step * (i + 1) for i in range(frame_count)]

def get_video_duration(video_path):
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        video_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

def slugify(name):
    name = re.sub(r"[^\w\s-]", "", name.lower())
    return re.sub(r"[-\s]+", "-", name).strip("-")

# ============ Main ============

def main():
    plan = {}
    ffmpeg_commands = []

    for section_id, section_info in SECTIONS.items():
        level_dir = LEVEL_DIRS[section_info["level"]]
        section_plan = []

        for video_num, video_name in section_info["videos"]:
            video_path = None
            for filename in os.listdir(level_dir):
                if filename.endswith(".mp4") and (
                    filename.startswith(f"{video_num}. ") or filename.startswith(f"{video_num}.")
                ):
                    video_path = os.path.join(level_dir, filename)
                    break

            if not video_path:
                print(f"WARNING: Video {video_num} not found in {level_dir}")
                continue

            duration = get_video_duration(video_path)
            frame_count = frames_for_duration(duration, video_name)
            timestamps = interpolate_timestamps(duration, frame_count)
            slug = slugify(video_name)
            labels = ["overview", "detail", "result"][:frame_count]

            shots = []
            for timestamp, label in zip(timestamps, labels):
                filename = f"{slug}-{label}.jpg"
                shots.append({"timestamp": timestamp, "label": label, "filename": filename})
                ffmpeg_commands.append(
                    f'ffmpeg -y -ss {timestamp:.1f} -i "{video_path}" -frames:v 1 "{ASSET_DIR}{filename}"'
                )

            section_plan.append(
                {
                    "video_num": video_num,
                    "video_name": video_name,
                    "duration": duration,
                    "slug": slug,
                    "frame_count": frame_count,
                    "shots": shots,
                }
            )

        plan[section_id] = {"title": section_info["title"], "videos": section_plan}

    with open(os.path.join(COURSE_DIR, "_screenshot_plan.json"), "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)
    with open(os.path.join(COURSE_DIR, "_batch_screenshots.sh"), "w", encoding="utf-8") as f:
        f.write("#!/bin/bash\nset -e\n\n" + "\n".join(ffmpeg_commands) + "\n")

    total = sum(video["frame_count"] for section in plan.values() for video in section["videos"])
    print(f"Plan written: {total} total screenshots")

if __name__ == "__main__":
    main()
