---
name: youtube-chapter-generator
description: >
  Auto-generate YouTube video chapters from subtitles. Parses VTT/SRT files,
  identifies topic transitions, and produces timestamped chapter markers.
  Triggers: "youtube chapters", "视频章节", "youtube分段".
version: 1.0.0
tags:
  - latest
  - youtube
  - video
  - automation
---

# YouTube Chapter Generator

Auto-generate YouTube video chapters from subtitles. Parses VTT/SRT files, identifies topic transitions, and produces timestamped chapter markers.

## Usage

```bash
# Download subtitles first
yt-dlp --write-sub --write-auto-sub \
  --sub-lang "zh-Hans,zh,en" \
  --convert-subs vtt \
  --skip-download \
  -o "/tmp/%(id)s" \
  "https://www.youtube.com/watch?v=VIDEO_ID"

# Generate chapters from subtitle file
python3 generate_chapters.py "/tmp/VIDEO_ID.zh-Hans.vtt"
```

## Chapter Generation Logic

```python
import re

def parse_vtt_timestamps(vtt_content):
    """Extract timestamps and text from VTT file"""
    timestamps = []
    for match in re.finditer(r'(\d{2}:\d{2}:\d{2})\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}', vtt_content):
        timestamps.append(match.group(1))
    return timestamps

def generate_chapters(vtt_file, min_gap_seconds=30):
    """Generate chapters from VTT subtitle file"""
    with open(vtt_file) as f:
        content = f.read()
    
    timestamps = parse_vtt_timestamps(content)
    if len(timestamps) < 2:
        return []
    
    # Find natural breaks (gaps > min_gap_seconds)
    chapters = []
    last_ts = timestamps[0]
    
    for ts in timestamps[1:]:
        gap = parse_ts(ts) - parse_ts(last_ts)
        if gap >= min_gap_seconds:
            chapters.append(last_ts)
            last_ts = ts
    
    chapters.append(timestamps[-1])
    return chapters

def parse_ts(ts_str):
    """Parse HH:MM:SS to seconds"""
    parts = ts_str.split(":")
    return int(parts[0])*3600 + int(parts[1])*60 + int(parts[2])

# Output format: "00:00 Introduction\n00:45 Main Topic\n..."
```

## YouTube Chapter Requirements

- Minimum 3 chapters for YouTube to auto-display
- First chapter must start at 0:00
- Chapters must be at least 10 seconds apart
- Maximum 12 chapters recommended

## Tags

`youtube` `chapters` `video` `timestamps` `subtitles` `automation`
