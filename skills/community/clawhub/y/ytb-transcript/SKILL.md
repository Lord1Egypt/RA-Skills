---
name: ytb-transcript
description: Fetch YouTube video transcripts, subtitles, and generate summaries. Use when the user wants to extract text from a YouTube video, download subtitles (similar to downsub.com), get timestamped transcripts, or get AI-generated summaries of video content. Supports raw transcript extraction, timestamped subtitles, and structured key point summaries. Ideal for research, academic study, lecture note-taking, content analysis, or processing long videos without watching them.
---

# YTB Transcript

## Overview

This skill fetches transcripts and subtitles from YouTube videos and can generate intelligent summaries.

Use this skill for:
- Extracting text content from YouTube videos
- Downloading subtitles (downsub.com style)
- Getting timestamped transcripts
- Generating summaries of video content

## How to Use

Provide a YouTube URL or video ID. The skill will:

1. Extract the video ID from the URL
2. Attempt to fetch the transcript using available services
3. If requested, generate a summary of the content
4. Return clean, usable output

### Examples

**Get transcript:**
- "Get the transcript from https://youtu.be/xxxxxx"
- "Extract subtitles from this video: [url]"

**Get summary:**
- "Summarize this YouTube video: [url]"
- "What are the key points from this lecture?"

**Combined request:**
- "Get the transcript and summarize this video: [url]"

## Available Functions

### Transcript Fetching
- Returns full transcript text
- Can include timestamps when available
- Supports multiple languages (prioritizes Chinese/English)

### Summarization
- Generates concise or detailed summaries
- Can focus on key arguments, technical content, or main ideas
- Adjustable summary length

## Notes

- Works best with videos that have subtitles (auto-generated or uploaded)
- For videos without subtitles, it may fall back to metadata-based summarization
- Long videos may take longer to process
- Output is clean markdown/text suitable for research or note-taking

## Resources

See `references/methods.md` for implementation details and supported services.
See `scripts/fetch.py` for the core fetching logic.