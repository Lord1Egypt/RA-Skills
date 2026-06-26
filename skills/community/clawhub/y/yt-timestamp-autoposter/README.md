# YouTube Timestamp Generator & Auto-Poster — First-Time Setup

This guide walks you through setting up the YouTube Data API so the `--post` flag can automatically append timestamps to your video descriptions on YouTube.

---

## Step 1 — Install Dependencies

```bash
pip install youtube-transcript-api google-generativeai google-auth-oauthlib google-api-python-client
```

---

## Step 2 — Enable the YouTube Data API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. In the left sidebar, navigate to **APIs & Services → Library**
4. Search for **YouTube Data API v3** and click **Enable**

---

## Step 3 — Create OAuth 2.0 Credentials

1. In the left sidebar, go to **APIs & Services → Credentials**
2. Click **Create Credentials → OAuth 2.0 Client ID**
3. If prompted, configure the **OAuth consent screen** first (select **External**, fill in the required app name and email fields, then save)
4. For application type, select **Desktop app**
5. Give it a name and click **Create**
6. Click **Download JSON** on the credentials that were just created
7. Rename the downloaded file to `credentials.json`
8. Place `credentials.json` in the `scripts/` directory of this project

---

## Step 4 — Run the Auth Flow for the First Time

Run the script with `--post` for the first time to trigger the OAuth browser flow:

```bash
python scripts/youtube_desc_generator.py --url "https://youtu.be/your-video-id" "$GEMINI_API_KEY" --post
```

- A browser window will open asking you to sign in to your Google account
- Grant the requested YouTube permissions
- After authorizing, a `token.pickle` file will be saved automatically in the `scripts/` directory
- This token is reused on all future runs — you will not need to sign in again unless it expires

---

## Step 5 — How to Use

There are two ways to use the tool: directly via the command line, or by describing what you want in natural language.

### From a YouTube URL

Generate timestamps for a specific video:

```bash
python scripts/youtube_desc_generator.py --url "https://youtu.be/hD1jOizSPnk" "$GEMINI_API_KEY"
```

Generate and automatically append the timestamps to that same video's description:

```bash
python scripts/youtube_desc_generator.py --url "https://youtu.be/hD1jOizSPnk" "$GEMINI_API_KEY" --post
```

### From Raw Transcript Text

Generate timestamps from a raw transcript string:

```bash
python scripts/youtube_desc_generator.py --transcript "0:00 Welcome..." "$GEMINI_API_KEY"
```

Generate and automatically append the timestamps to your latest YouTube upload's description:

```bash
python scripts/youtube_desc_generator.py --transcript "0:00 Welcome..." "$GEMINI_API_KEY" --post
```

### Auto-target Latest Video

Automatically fetch your most recent video, check for existing timestamps to avoid duplicate entries, download the transcript, generate SEO chapters, and post:

```bash
python scripts/youtube_desc_generator.py --latest "$GEMINI_API_KEY" --post
```

Your transcript string must follow this format — one line per entry, `MM:SS` timestamp followed by the caption text:

```
0:00 Welcome to this video about AI agents.
0:12 Today we're going to cover what an AI agent actually is.
1:00 Let me show you a live demo of an agent booking a flight.
```

### Via Natural Language

You can also describe what you want and the agent will run the correct command for you:

| What you say                                                                           | What runs                    |
| -------------------------------------------------------------------------------------- | ---------------------------- |
| "Create timestamps for my latest video"                                                | `--latest` mode, with `--post` |
| "Generate timestamps for this video: https://youtu.be/abc123"                          | `--url` mode, no post        |
| "Generate timestamps for this video and post it: https://youtu.be/abc123"              | `--url` mode, with `--post`  |
| "Generate SEO timestamps and post them back to this video: https://youtu.be/abc123"    | `--url` mode, with `--post`  |
| "Process this transcript text: 0:00 Welcome..."                                        | `--transcript` mode, no post |
| "Generate timestamps from my transcript text: 0:00 Welcome..."                         | `--transcript` mode, no post |
| "Process my transcript text and post it to my latest video: 0:00 Welcome..."           | `--transcript` mode, with `--post` |

**Quick rules:**

- "latest video" or similar in your message → `--latest` mode
- A YouTube URL in your message → `--url` mode
- A raw transcript text in your message → `--transcript` mode
- Words like "post", "update", "upload", or "push" → adds `--post` (Note: updating the latest video implies posting)
- `--url --post` updates **that specific video**
- `--transcript --post` and `--latest --post` updates your **latest upload**

---

## Notes

- **Quota**: The YouTube Data API has a free daily quota of 10,000 units. A single description update costs ~50 units, so the free tier is more than enough for regular use.
- **`token.pickle`**: Keep this file secure — it grants write access to your YouTube channel. Do not commit it to version control.
- **Token expiry**: If the token expires, delete `token.pickle` and re-run the script with `--post` to re-authenticate.
- **Revoking access**: You can revoke the app's access at any time from your [Google Account permissions](https://myaccount.google.com/permissions).
