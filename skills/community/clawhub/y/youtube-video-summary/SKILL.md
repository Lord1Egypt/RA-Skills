---
name: youtube-summary
description: Automatically fetch YouTube video subtitles and generate concise summaries. Use when you need to summarize a YouTube video, get key points from a talk, or extract main ideas from long videos without watching. Supports different summary lengths and multiple languages.
---

# YouTube Summary

Automatically get subtitles from any public YouTube video and generate a clean, structured summary with key points. Saves hours of watching long videos when you just need the main ideas.

## Core Capabilities

### 1. Get full subtitles from any public YouTube video
- Works with videos that have auto-generated captions
- Supports multiple languages
- Outputs clean formatted text

### 2. Generate concise summaries
- Extracts all key points and main arguments
- Adjusts summary length based on your needs (short/medium/detailed)
- Structures output with bullet points for easy reading

### 3. Export results
- Save summary as markdown or text file
- Copy-paste ready for note-taking

## Quick Start

Given a YouTube URL:

1. **Extract video ID** from the URL
   - `https://www.youtube.com/watch?v=dQw4w9WgXcQ` → ID: `dQw4w9WgXcQ`
   - `https://youtu.be/dQw4w9WgXcQ` → ID: `dQw4w9WgXcQ`

2. **Fetch subtitles** using the Python script:
   ```python
   from scripts.youtube_subtitles import get_youtube_subtitles
   subtitles = get_youtube_subtitles(video_id)
   ```

3. **Generate summary** with the AI model using the subtitle text

4. **Format and present** the result with:
   - Video title and link
   - Executive summary (1-paragraph overview)
   - Key points (bulleted list)
   - Detailed notes (optional)

## Usage Examples

**Example request:** "Summarize this YouTube video: https://www.youtube.com/watch?v=xyz"

**Expected output:**
```
# Video Summary: [Title]
Source: https://www.youtube.com/watch?v=xyz

## Executive Summary
One paragraph overview of the entire video's main message.

## Key Points
- Point 1: Main argument or finding
- Point 2: Second important topic
- Point 3: Key takeaway
- ...

## Detailed Notes (optional for longer videos)
More detailed breakdown...
```

## Language Support

- The script automatically gets the available subtitle tracks
- Default to first available track (usually the video's original language)
- Can specify preferred language (e.g., "summarize in English" or "summarize in Chinese")

## Scripts

### `scripts/youtube_subtitles.py`
Python utility to fetch subtitles from YouTube using youtube-transcript-api.

**Usage:**
```bash
python scripts/youtube_subtitles.py <video-id> [language-code]
```

**Requirements:**
```
pip install youtube-transcript-api
```

### `scripts/summarize.py`
Helper script to format subtitles for summarization.

## When to use this skill

✅ **Use when:**
- You want the main ideas from a long YouTube video without watching
- You need to take notes from a lecture or talk
- You want to share key points from a video with others
- You're doing research and need to process multiple videos quickly

❌ **Don't use when:**
- The video is private and has no public captions
- The video has no captions/subtitles at all
- You need a full word-for-word transcription (this skill focuses on summarization)
