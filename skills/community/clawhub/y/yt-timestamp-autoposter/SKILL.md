---
name: yt-timestamp-autoposter
description: Generate SEO-optimized YouTube timestamps from a YouTube URL or a raw transcript string, then optionally append them to the description of that specific video or your latest upload. Use when you need to create chapters for a YouTube video. Also use when the user asks to generate timestamps, append timestamps to YouTube, or process transcript text.
---

# YouTube Timestamp Generator & Auto-Poster

Transforms a YouTube URL or a raw transcript string into SEO-optimized timestamps (chapters) powered by Gemini. Optionally appends the result directly to the description of a specific YouTube video or your latest upload via the YouTube Data API.

## ⚠️ Requirements Checklist

Before using this skill, ensure you have:

- [ ] **Python 3** installed
- [ ] **Dependencies installed**: `pip install youtube-transcript-api google-generativeai google-auth-oauthlib google-api-python-client`
- [ ] **Gemini API Key** available to pass as an argument
- [ ] **`credentials.json`** placed in `scripts/` *(only required for `--post` — download from Google Cloud Console as an OAuth 2.0 Desktop App client)*

## Features

- 🕐 **SEO Timestamps**: Generates 0:00-based chapters with keyword-rich, scannable labels
- 🔗 **Three Input Modes**: Works from a YouTube URL, a raw transcript string, or auto-targets your latest video
- 🚀 **Smart Auto-Poster**: URL mode appends to that specific video; transcript and latest modes append to your latest upload
- 🛡️ **Duplicate Prevention**: The `--latest` mode checks for existing timestamps before attempting to generate new ones
- 🔑 **Keyword Optimization**: Natural integration of primary, secondary, and LSI keywords from the transcript
- 🧹 **Clean Output**: Returns only the final timestamps — no extra headings or commentary

## Quick Start

### Mode 1 — YouTube URL
Fetches the transcript from the video, generates SEO timestamps, and optionally appends them to the description of **that specific video**.

```bash
# Generate only (view output)
python scripts/youtube_desc_generator.py --url "<youtube_url>" "<gemini_api_key>"

# Generate and post to that video
python scripts/youtube_desc_generator.py --url "<youtube_url>" "<gemini_api_key>" --post
```

### Mode 2 — Raw Transcript Text

Reads a raw transcript string, generates SEO timestamps, and optionally appends them to the description of your **latest YouTube upload**.

```bash
# Generate only (view output)
python scripts/youtube_desc_generator.py --transcript "0:00 Welcome..." "<gemini_api_key>"

# Generate and post to latest video
python scripts/youtube_desc_generator.py --transcript "0:00 Welcome..." "<gemini_api_key>" --post
```

### Mode 3 — Latest Video
Automatically fetches your most recent video, checks if timestamps already exist (to prevent duplicates), downloads the transcript, generates SEO timestamps, and optionally appends them to the description.

```bash
# Generate and post timestamps for your latest video (if they don't already exist)
python scripts/youtube_desc_generator.py --latest "<gemini_api_key>" --post
```

**Examples:**

```bash
python scripts/youtube_desc_generator.py --url "https://youtu.be/abc123" "$GEMINI_API_KEY"
python scripts/youtube_desc_generator.py --url "https://youtu.be/abc123" "$GEMINI_API_KEY" --post
python scripts/youtube_desc_generator.py --transcript "0:00 Welcome..." "$GEMINI_API_KEY" --post
```

## Raw Transcript Text Format

When using `--transcript`, the transcript must be a string with timestamps in `MM:SS` format, separated by newlines:

```
0:00 Welcome to this video about AI agents.
0:12 Today we're going to cover what an AI agent actually is.
1:00 Let me show you a live demo of an agent booking a flight.
...
```

## Natural Language Command Mapping

When the user speaks naturally, map their intent to the correct command using the table below. Always extract the YouTube URL or transcript text from their message and substitute it into the command.

| What the user says                                                                     | Command to run                                                                                      |
| -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| "Create timestamps for my latest video"                                                | `python scripts/youtube_desc_generator.py --latest "$GEMINI_API_KEY" --post`                          |
| "Generate timestamps for this video: https://youtu.be/abc123"                          | `python scripts/youtube_desc_generator.py --url "https://youtu.be/abc123" "$GEMINI_API_KEY"`        |
| "Create SEO chapters from this YouTube link: https://youtu.be/abc123"                  | `python scripts/youtube_desc_generator.py --url "https://youtu.be/abc123" "$GEMINI_API_KEY"`        |
| "Give me the timestamps for this video: https://youtu.be/abc123"                       | `python scripts/youtube_desc_generator.py --url "https://youtu.be/abc123" "$GEMINI_API_KEY"`        |
| "Generate timestamps for this video and post it: https://youtu.be/abc123"              | `python scripts/youtube_desc_generator.py --url "https://youtu.be/abc123" "$GEMINI_API_KEY" --post` |
| "Generate SEO timestamps and post them back to this video: https://youtu.be/abc123"   | `python scripts/youtube_desc_generator.py --url "https://youtu.be/abc123" "$GEMINI_API_KEY" --post` |
| "Process this transcript text: 0:00 Welcome..."                                        | `python scripts/youtube_desc_generator.py --transcript "0:00 Welcome..." "$GEMINI_API_KEY"`                |
| "Generate timestamps from my transcript text: 0:00 Welcome..."                         | `python scripts/youtube_desc_generator.py --transcript "0:00 Welcome..." "$GEMINI_API_KEY"`                |
| "Process my transcript text and post it to my latest video: 0:00 Welcome..."                            | `python scripts/youtube_desc_generator.py --transcript "0:00 Welcome..." "$GEMINI_API_KEY" --post`         |
| "Generate timestamps from my transcript and upload to YouTube: 0:00 Welcome..."        | `python scripts/youtube_desc_generator.py --transcript "0:00 Welcome..." "$GEMINI_API_KEY" --post`         |

### Decision Rules

Use these rules to determine which command to run when the intent is ambiguous:

- **"latest video" or similar** → always use `--latest` mode
- **URL present** → always use `--url` mode
- **Transcript text present** → always use `--transcript` mode
- **"post", "update", "upload", "push"** anywhere in the message → add `--post` flag (Note: commands like "create timestamps for my latest video" imply updating it, so `--post` is added)
- **No `--post`** → generate and print only, do not touch YouTube
- **`--transcript --post`** and **`--latest --post`** → always targets the **latest upload** on the channel
- **`--url --post`** → always targets **that specific video**

## Generated Output

The script returns a single clean block — no labels or extra text:

- **SEO-Optimized Timestamps** — YouTube chapters starting at `0:00` with keyword-rich labels and SEO suffix tags (e.g. `(Tutorial)`, `(Overview)`, `(2026)`)

> **Important:** Output only the final timestamps. Do not include any introductory sentences, headings, labels, preamble, or commentary before or after the output.

## How It Works

**URL mode:**

1. Extracts the video ID from the provided YouTube URL
2. Fetches the English transcript via `youtube-transcript-api`
3. Formats the transcript with `MM:SS` timestamps
4. Sends a prompt to Gemini for timestamps
5. Prints the timestamps
6. _(With `--post`)_ Authenticates via OAuth2 and appends the new timestamps to **that specific video's** description

**Transcript mode:**

1. Reads the provided raw transcript text string
2. Sends a prompt to Gemini for timestamps
3. Prints the timestamps
4. _(With `--post`)_ Authenticates via OAuth2, finds your **latest upload**, and appends the new timestamps to its description

## OAuth Setup (for `--post` only)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable the **YouTube Data API v3**
3. Create **OAuth 2.0 credentials** (Desktop App type)
4. Download the file as `credentials.json` and place it in `scripts/`
5. On first run with `--post`, a browser window will open for you to authorize access
6. A `token.pickle` file will be saved automatically for future runs

## Troubleshooting

**No transcript available (URL mode):**

- The video may have transcripts disabled or no English captions
- Switch to `--transcript` mode with a manually prepared transcript string

**Transcript text not loading (transcript mode):**

- Ensure the text format is correct
- Each line should follow `MM:SS text` format

**Gemini API errors:**

- Verify your API key is valid and has access to `gemini-3.1-flash-lite-preview`
- Check your quota at [Google AI Studio](https://aistudio.google.com/)

**`--post` not updating the video:**

- Ensure `credentials.json` is in the `scripts/` directory
- Delete `token.pickle` and re-authenticate if credentials have expired
- Confirm the YouTube Data API v3 is enabled in your Google Cloud project

**Wrong video appended to in transcript mode:**

- Transcript mode always targets your most recent upload — make sure the correct video is your latest
- If you need to target a specific video, use `--url` mode instead

## Privacy & Safety

⚠️ **Important:** The `--post` flag will append timestamps to a video's description automatically without manual confirmation in the CLI.

- The script always shows you the target video title being updated
- OAuth credentials are stored locally in `token.pickle` — keep this file secure
- Revoke access anytime via your [Google Account permissions](https://myaccount.google.com/permissions)
