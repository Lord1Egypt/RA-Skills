"""
Archive transcription results as dated Markdown files.
"""

import os
import re
from datetime import datetime, timedelta


def sanitize_filename(title: str, max_len: int = 30) -> str:
    """
    Sanitize a title for use in a filename:
    - Remove special characters that are invalid in filenames
    - Truncate to max_len
    - Replace spaces with dashes for URL-friendliness
    """
    # Remove dangerous characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '', title)
    # Replace spaces with dashes
    sanitized = sanitized.replace(' ', '-')
    # Truncate
    if len(sanitized) > max_len:
        sanitized = sanitized[:max_len].rstrip('-')
    return sanitized or "transcript"


def archive(transcript_text: str, title: str, summary: str, source: str,
            start_time: datetime = None, archive_dir: str = "archive") -> str:
    """
    Write a complete transcription archive file.

    Args:
        transcript_text: Full transcript with timestamps
        title: Generated title from LLM
        summary: Generated summary from LLM
        source: Audio source ("blackhole" or "mic")
        start_time: When transcription started (auto-generated if None)
        archive_dir: Base archive directory

    Returns:
        Path to the created archive file
    """
    now = start_time or datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    safe_title = sanitize_filename(title)
    filename = f"{date_str}-{time_str.replace(':', '')}-{safe_title}.md"

    # Build path: archive/YYYY/MM/filename.md
    year = now.strftime("%Y")
    month = now.strftime("%m")
    file_path = os.path.join(archive_dir, year, month, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Calculate end time (approximate from transcript line count)
    line_count = transcript_text.strip().count('\n') + 1 if transcript_text.strip() else 0
    duration_min = max(1, round(line_count * 1.5))  # ~1.5s per transcription interval
    end_time = now + timedelta(minutes=duration_min)
    end_time_str = end_time.strftime("%H:%M")

    content = f"""\
---
title: "{title}"
date: {date_str}
time: "{time_str} - {end_time_str}"
source: {source}
duration: {duration_min}m
---

## 摘要

{summary}

## 完整转录

```
{transcript_text}
```
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path
