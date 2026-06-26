# YouTube Outlier Skill

Finds trending or outlier videos by niche on YouTube, analyzes their metadata and main points, and writes results to a Google Sheet. Optionally, posts a summary to Discord when complete.

## Features
- Scan for YouTube channels/videos by niche (e.g., "AI news").
- Identify outlier videos: much higher views than a channel's average.
- Filter: only videos in the last month or with recent comments.
- Extract title, description, thumbnail URL, tags, hashtags, transcript/main points, keywords.
- Write results as rows to a Google Sheet (customizable columns).
- Post a summary table to a Discord channel automatically.
- Run via OpenClaw trigger (Discord slash command or CLI).

## Setup
1. Place this skill folder in your OpenClaw workspace under `skills/`.
2. Copy `.env.example` to `.env` and fill in your API keys/config values.
3. Ensure your Google Sheet is shared with your service account email (see GOOGLE_SHEETS_CREDENTIALS_JSON).
4. (If using Discord): Add the Discord bot and obtain its token + channel ID.
5. Install dependencies: `npm install` (in this folder), if required for direct lib usage.

## Usage
Trigger from Discord or CLI with a "niche":

```
/ytoutlier niche:"AI news"
```

or

```
openclaw invoke youtube-outlier-skill --niche="AI news, bitcoin, productivity"
```

## Development
- Written in TypeScript for full type safety and OpenClaw integration.
- Extend to save screenshots, process thumbnails, or invoke other agent skills as needed.

## Author
Skill scaffold for Danny by Soma 🧘‍♂️ with OpenClaw.
