# Soulsync — Personalize Your OpenClaw Agent

**Make your AI agent actually know you.** Soulsync collapses weeks of "getting to know you" into minutes through natural conversation and optional data imports.

## The Problem

A fresh OpenClaw agent is generic. It doesn't know your name, your job, how you like to communicate, or what you care about. It takes days or weeks of chatting before it feels personal. Most people give up before that happens.

## The Solution

Soulsync detects your current setup and adapts:

- **New users** → Full guided soulsyncing conversation (5 minutes)
- **Partial setup** → Fills in the gaps, doesn't re-ask what it knows
- **Power users** → Connects data sources for deeper personalization

## Features

### 🗣️ Natural Conversation Engine
Not a survey. Not a form. A real conversation that picks up on your personality from *how* you answer, not just what you answer.

### 📧 Data Importers (Optional)
Connect accounts to skip the interview. All processing happens locally — raw data is never stored.

| Source | What It Learns | Auth Required |
|--------|---------------|---------------|
| **Gmail** | Communication style, key contacts, schedule patterns | Google OAuth |
| **Google Calendar** | Lifestyle patterns, work/life balance, schedule density | Google OAuth |
| **GitHub** | Technical skills, languages, project types | Token or public |
| **Twitter/X** | Interests, tone, engagement style | None (via Nitter) |
| **Facebook** | Interests, groups, social connections, posting style | Data export (JSON) |
| **Instagram** | Visual style, hashtags, engagement, interests | Data export (JSON) |
| **Spotify** | Music taste → personality traits | Spotify API key |
| **Contacts** | Relationship network, social style | Google OAuth or .vcf |
| **Apple** | Safari bookmarks, iCloud contacts, ecosystem signals | macOS or .vcf export |
| **Reddit** | True interests, opinions, communities, communication style | None (public) |
| **YouTube** | Watch history, subscriptions, content preferences, learning style | Google Takeout |
| **LinkedIn** | Career trajectory, skills, education, professional network | Data export |
| **Local System** | Shell history, installed apps, git repos, browser bookmarks | None (local scan) |

### 🔒 Privacy First
- All data processed by your local model (or your configured cloud model)
- Raw emails/tweets never leave your machine
- Only synthesized personality files are kept
- Raw import data deleted after processing

### 📝 What It Generates

| File | Purpose |
|------|---------|
| `SOUL.md` | Agent personality, communication style, boundaries |
| `USER.md` | Your name, background, interests, preferences |
| `MEMORY.md` | Seed memories from imports and conversation |

## Quick Start

```bash
# Install
npx clawhub@latest install soulsync

# Use — just chat with your agent
"Hey, let's get to know each other"

# Or explicitly
/soulsync
```

The skill auto-detects empty SOUL.md/USER.md and offers to help.

## How It Works

```
1. Detector scans your workspace → determines your level (new/partial/established)
2. Agent adapts conversation depth to what's needed
3. Optional: connect accounts for richer data
4. Synthesizer merges everything → generates personalized files
5. You review and approve before anything is written
```

## Requirements

- OpenClaw (any version)
- Python 3.10+
- Optional: Google OAuth credentials for Gmail/Calendar/Contacts
- Optional: GitHub token for private repo analysis
- Optional: Spotify API credentials

## Data Sources Setup

### Gmail & Calendar
Reuses existing OpenClaw Gmail OAuth if available. Otherwise:
1. Create OAuth credentials at [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Save `credentials.json` to your workspace
3. First run will prompt for browser auth

### GitHub
Uses your git credential store automatically. Or set `GITHUB_TOKEN` env var.

### Twitter/X
No setup needed — uses public Nitter instances. Works with any public Twitter profile.

### Spotify
1. Create an app at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Set `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` env vars

### Contacts
Uses Google People API (same OAuth as Gmail) or import a `.vcf` file.

## Examples

**Brand new user:**
> Agent: "Hey — I'm brand new here and so are you. Let's fix that. A few questions that'll help me actually be useful. Should take about 5 minutes."

**Returning user with gaps:**
> Agent: "I know you're ocbenji, you're into Bitcoin and AI, Central timezone. But I don't really know how you like to communicate or what your boundaries are. Want to fill that in?"

**Power user wanting deeper personalization:**
> Agent: "Your profile looks solid. I could connect to your email and GitHub to learn more automatically. Everything stays local."

## Contributing

Issues and PRs welcome. Built by [@ocbenji](https://github.com/ocbenji).

## License

MIT
