---
name: youtube-summary
version: "1.0.7"
description: |
  Fetch a YouTube video transcript and provide a structured summary.
  Usage: /youtube-summary <youtube-url> [--lang <language>]
argument-hint: "/youtube-summary https://youtube.com/watch?v=VIDEO_ID --lang italian"
allowed-tools:
  - Bash
  - Write
  - AskUserQuestion
homepage: https://github.com/ivanopassari/youtube-summary-skill
repository: https://github.com/ivanopassari/youtube-summary-skill
author: ivanopassari
license: MIT
user-invocable: true
disable-model-invocation: true
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins:
        - uv
    files:
      - "fetch_transcript.py"
    homepage: https://github.com/ivanopassari/youtube-summary-skill
    tags:
      - youtube
      - transcript
      - summary
      - productivity
---

# YouTube Summary Skill

You are tasked with fetching a YouTube video transcript and producing a structured summary.

## Steps

1. **Parse arguments**: Read `$ARGUMENTS`. Extract the YouTube URL and an optional language flag (`--lang <language>`). If no URL is provided, use the AskUserQuestion tool to ask the user for it. If no `--lang` flag is provided, default to **English**.

2. **Fetch the transcript**: Run the following command via Bash:
   ```bash
   uv run --no-project --with youtube-transcript-api python -c "import sys,pathlib,runpy; h=pathlib.Path.home(); c=sorted(h.glob('.claude/plugins/cache/youtube-summary-skill/**/fetch_transcript.py')); s=c[-1] if c else h/'.claude/skills/youtube-summary-skill/fetch_transcript.py'; sys.argv=[str(s)]+sys.argv[1:]; runpy.run_path(str(s),run_name='__main__')" "$URL"
   ```
   Replace `$URL` with the actual YouTube URL.

3. **Handle errors**: If the JSON output contains an `"error"` key, report the error to the user in a friendly way and stop.

4. **Summarize**: Using the transcript text, produce a structured summary **in the chosen language** with this format:

   ### Video Summary

   **Overview**
   A brief introductory paragraph summarizing the video's topic and main message.

   **Key Points**
   - Bullet points covering the main concepts discussed in the video
   - Each point should be concise but informative

   **Notable Quotes**
   > Notable quotes or significant phrases from the video (if any stand out)

   Translate section headings to match the chosen language (e.g., "Panoramica", "Punti chiave", "Citazioni notevoli" for Italian). If the transcript is in a different language than the chosen one, still produce the summary in the chosen language.

5. **Offer to save**: After presenting the summary, ask the user if they want to save it as a Markdown file. If yes, write it using the Write tool to a reasonable filename based on the video ID (e.g., `youtube_summary_<video_id>.md`).

## Security & Permissions

**What this skill does:**
- Runs a local Python script via `uv` to fetch YouTube video transcripts using the `youtube-transcript-api` library
- Uses YouTube's public transcript/caption data (no API key required)
- Optionally saves the generated summary as a local Markdown file

**What this skill does NOT do:**
- Does not access your YouTube account or any authenticated data
- Does not upload, post, or modify any content on YouTube
- Does not send data to any third-party service
- Does not store or cache any credentials
- Cannot be invoked autonomously by agents (disable-model-invocation: true)

**Bundled scripts:** `fetch_transcript.py` (transcript fetcher)

**Dependencies (managed by uv):** `youtube-transcript-api`

Review the script before first use to verify behavior.
