#!/usr/bin/env python3
"""
Batch subtitle preprocessing script.
Removes subtitle metadata and writes one plain-text file per section.

Usage:
1. Edit the SECTIONS and LEVEL_DIRS definitions below.
2. Run the script.

Output:
  _preprocessed/section-<slug>.txt
"""

import os
import re

# ============ Configuration ============

COURSE_DIR = "<COURSE_DIR>"
LEVEL_DIRS = {
    "L1": os.path.join(COURSE_DIR, "<Level 1>"),
    "L2": os.path.join(COURSE_DIR, "<Level 2>"),
}

SECTIONS = {
    "section-01": {"level": "L1", "videos": [(1, "Video Name")]},
}

# ============ Core helpers ============

def strip_srt(srt_path):
    with open(srt_path, encoding="utf-8") as f:
        text = f.read()
    lines = text.split("\n")
    result = []
    for line in lines:
        line = line.strip()
        if re.match(r"^\d+$", line):
            continue
        if re.match(r"^\d{2}:\d{2}:\d{2}", line):
            continue
        if not line:
            continue
        result.append(line)
    return " ".join(result)

def find_srt(level_dir, video_num):
    for filename in sorted(os.listdir(level_dir)):
        if not filename.endswith((".srt", ".vtt")):
            continue
        base = os.path.splitext(filename)[0]
        base_clean = re.sub(r"\.(en|zh|cn|en-US|zh-CN)$", "", base)
        if base_clean.startswith(f"{video_num}. ") or base_clean.startswith(f"{video_num} "):
            return os.path.join(level_dir, filename)
    return None

def slugify(name):
    name = re.sub(r"[^\w\s-]", "", name.lower())
    return re.sub(r"[-\s]+", "-", name).strip("-")

# ============ Main ============

def main():
    output_dir = os.path.join(COURSE_DIR, "_preprocessed")
    os.makedirs(output_dir, exist_ok=True)

    for section_key, section_info in SECTIONS.items():
        level_dir = LEVEL_DIRS[section_info["level"]]
        texts = []

        for video_num, video_name in section_info["videos"]:
            srt_path = find_srt(level_dir, video_num)
            if not srt_path:
                print(f"WARNING: No subtitle found for video {video_num} in {level_dir}")
                continue
            plain_text = strip_srt(srt_path)
            texts.append(f"== Video {video_num}: {video_name} ==\n{plain_text}")
            print(f"  OK: {video_num}. {video_name} ({len(plain_text)} chars)")

        slug = slugify(section_key)
        output_path = os.path.join(output_dir, f"{slug}.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(texts))
        print(f"Section written: {output_path} ({len(texts)} videos)")

if __name__ == "__main__":
    main()
