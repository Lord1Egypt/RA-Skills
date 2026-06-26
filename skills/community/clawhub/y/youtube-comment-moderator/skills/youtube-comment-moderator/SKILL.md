---
name: youtube-comment-moderator
description: >
  AI-powered YouTube comment moderation. Fetches comments, classifies them
  (spam, question, praise, hate, neutral, constructive), drafts replies,
  and deletes spam. Works with any YouTube channel via OAuth.
  Use when moderating YouTube comments, setting up auto-replies, analyzing
  comment sentiment, managing spam, or building a comment moderation pipeline.
---

# YouTube Comment Moderator

Classify, reply to, and delete YouTube comments automatically using Gemini Flash + YouTube Data API v3.

## Setup (Agent-Driven)

When a user wants to set up YouTube moderation, walk them through this conversationally. Do not tell them to run shell commands.

### 1. Collect Channel Info

Ask: "What's your YouTube channel URL or channel ID?"

Resolve it:
```bash
source .env
python3 scripts/fetch_comments.py --channel-id <ID> --max-videos 1 --max-comments 0
```
This validates the channel exists. If they give a URL like `youtube.com/@handle`, extract the handle and look up the channel ID via the API.

### 2. Check Environment Keys

Four keys are needed. Check which are missing:
```bash
echo "YOUTUBE_API_KEY=${YOUTUBE_API_KEY:+SET}" 
echo "GEMINI_API_KEY=${GEMINI_API_KEY:+SET}"
echo "YT_MOD_CLIENT_ID=${YT_MOD_CLIENT_ID:+SET}"
echo "YT_MOD_CLIENT_SECRET=${YT_MOD_CLIENT_SECRET:+SET}"
```

For any missing keys, tell the user what to do (not how to run scripts):

- **YOUTUBE_API_KEY**: "Go to [Google Cloud Console → Credentials](https://console.cloud.google.com/apis/credentials), create an API key, and add `YOUTUBE_API_KEY=...` to your `.env` file."
- **GEMINI_API_KEY**: "Go to [Google AI Studio](https://aistudio.google.com/apikey), create a key, and add `GEMINI_API_KEY=...` to your `.env` file."
- **YT_MOD_CLIENT_ID + YT_MOD_CLIENT_SECRET**: These require OAuth setup. Walk them through `references/oauth-setup.md` conversationally, or summarize: "In Google Cloud Console, enable YouTube Data API, create an OAuth consent screen (External, Testing mode), add yourself as test user, create a Web Application OAuth client with redirect URI `http://127.0.0.1:8976/callback`, then add the Client ID and Client Secret to your `.env`."

After they confirm keys are added, restart the gateway so env vars reload.

### 3. OAuth Authorization

Generate the auth URL and send it to the user:
```bash
source .env && python3 scripts/setup.py --auth-url
```

Tell them: "Open this link, sign in with the Google account that owns your YouTube channel, and click Allow. Your browser will redirect to a page that won't load — that's expected. Copy the entire URL from your browser's address bar and paste it back here."

When they paste the URL:
```bash
source .env && python3 scripts/setup.py --exchange-code "<PASTED_URL>"
```

### 4. Configure

Ask them conversationally:
- "What moderation mode? **Auto** (replies and deletes automatically), **Approval** (drafts everything for your review), or **Monitor** (classify and report only)?"
- "How do you typically talk to your audience? Casual? Professional? Funny?" (this sets voice_style)
- "Any common questions you get? I can pre-load answers so replies are accurate." (optional FAQ)

Then create the config:
```bash
python3 scripts/setup.py --create-config \
  --channel-id <ID> \
  --channel-name "<NAME>" \
  --mode <approval|auto|monitor> \
  --voice "<VOICE_STYLE>"
```

### 5. Test

Run a dry run and show them the results:
```bash
source .env && python3 scripts/moderate.py --all-videos --dry-run
```

Summarize: "Found X videos, Y new comments. Here's what I'd do: Z spam deleted, W questions answered, etc." Show a few examples.

### 6. Go Live

Once they approve:
```bash
source .env && python3 scripts/moderate.py --all-videos
```

Optionally set up a cron job to run every 15-30 minutes for ongoing moderation.

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `setup.py` | Setup wizard (interactive or `--auth-url` / `--exchange-code` / `--create-config`) |
| `moderate.py` | Main pipeline: fetch → classify → act. Also: `--stats`, `--queue`, `--approve`, `--all-videos` |
| `fetch_comments.py` | Standalone comment fetcher (API key only) |
| `classify_comments.py` | Standalone classifier (JSON in → JSON out) |
| `db.py` | SQLite persistence layer |

## Moderation Modes

- **monitor** — classify + report only (no OAuth needed)
- **approval** — drafts replies and queues deletions for review (`--queue` to see, `--approve` to execute)
- **auto** — auto-replies to questions, auto-deletes spam/hate

## Classification Categories

| Category | Auto Action | Description |
|----------|-------------|-------------|
| spam | delete | Promotional links, scam offers, bot text, self-promo |
| question | reply | Genuine question about video/creator/topic |
| praise | thank | Positive feedback, compliments |
| hate | delete | Hateful, abusive, harassing content |
| neutral | skip | Generic reactions, timestamps |
| constructive | flag | Thoughtful criticism, suggestions |

## Architecture

- **State:** SQLite (`data/youtube-comment-moderator/moderator.db`)
- **Classification:** Gemini 2.0 Flash (~$0.001/comment)
- **Read:** YouTube Data API v3 (API key)
- **Write:** YouTube Data API v3 (OAuth)
- **Deduplication:** comment_id primary key, already-processed comments skipped

## Environment Variables

Required:
- `YOUTUBE_API_KEY` — YouTube Data API v3 key (free, 10K units/day)
- `GEMINI_API_KEY` — Gemini Flash for classification

For write operations (reply/delete):
- `YT_MOD_CLIENT_ID` — Google OAuth client ID
- `YT_MOD_CLIENT_SECRET` — Google OAuth client secret

Optional overrides:
- `YT_MOD_DB` — SQLite DB path (default: `data/youtube-comment-moderator/moderator.db`)
- `YT_MOD_OAUTH` — OAuth token path (default: `skills/youtube-comment-moderator/oauth.json`)
- `YT_MOD_CONFIG` — Config path (default: `skills/youtube-comment-moderator/config.json`)

## OAuth Setup Details

See [references/oauth-setup.md](references/oauth-setup.md) for the full step-by-step Google Cloud setup guide with screenshots-level detail and troubleshooting.
