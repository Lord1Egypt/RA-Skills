---
name: youtube-trending
description: "Fetch and display the top trending YouTube videos globally or by country/category. Use when the user asks for trending YouTube videos, what's popular on YouTube, top YouTube videos today, or YouTube charts."
metadata:
  {
    "openclaw":
      {
        "emoji": "▶️",
        "requires": { "bins": ["python3"], "env": ["YOUTUBE_API_KEY"] },
        "install":
          [
            {
              "id": "python3",
              "kind": "system",
              "bins": ["python3"],
              "label": "Python 3 (stdlib only, no pip required)",
            },
          ],
      },
  }
---

# YouTube Trending

Fetch the top trending YouTube videos using the official YouTube Data API v3. Requires a free API key (10,000 units/day free — each trending fetch costs 1 unit).

## Setup: get a free API key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project (or select an existing one)
3. Enable **YouTube Data API v3** in the API Library
4. Go to **Credentials → Create Credentials → API key**
5. Set the environment variable for your platform (see below)

### Setting the environment variable

**macOS / Linux (bash/zsh):**
```bash
export YOUTUBE_API_KEY=your_key_here
```
To persist across sessions, add that line to `~/.zshrc` or `~/.bashrc`.

**Windows — Command Prompt:**
```cmd
set YOUTUBE_API_KEY=your_key_here
```

**Windows — PowerShell:**
```powershell
$env:YOUTUBE_API_KEY = "your_key_here"
```
To persist in PowerShell across sessions, add it to your `$PROFILE`.

## Usage

**macOS / Linux:**
```bash
python3 scripts/fetch-youtube-trending.py           # top 25, global
python3 scripts/fetch-youtube-trending.py FR        # France
python3 scripts/fetch-youtube-trending.py US 50     # top 50, US
python3 scripts/fetch-youtube-trending.py US 25 10  # Music
python3 scripts/fetch-youtube-trending.py US 25 20  # Gaming
python3 scripts/fetch-youtube-trending.py US 25 25  # News & Politics
```

**Windows (Command Prompt or PowerShell):**
```cmd
python scripts/fetch-youtube-trending.py
python scripts/fetch-youtube-trending.py FR
python scripts/fetch-youtube-trending.py US 50
python scripts/fetch-youtube-trending.py US 25 10
```

> On Windows, `python3` may not be in PATH — use `python` instead. Both work if Python 3 is installed.

## Arguments

| Position | Default   | Description                                  |
|----------|-----------|----------------------------------------------|
| 1        | _(none)_  | Country code — omit for global chart         |
| 2        | `25`      | Number of videos (max 50)                    |
| 3        | _(none)_  | Category ID — omit for all categories        |

## Category IDs

| ID | Name                  | ID | Name                  |
|----|-----------------------|----|-----------------------|
| 1  | Film & Animation      | 22 | People & Blogs        |
| 2  | Autos & Vehicles      | 23 | Comedy                |
| 10 | Music                 | 24 | Entertainment         |
| 15 | Pets & Animals        | 25 | News & Politics       |
| 17 | Sports                | 26 | Howto & Style         |
| 20 | Gaming                | 27 | Education             |
| 28 | Science & Technology  |    |                       |

## Output

For each video: rank, title, channel, duration, publish date, views, likes, comments, and a direct YouTube link.

## Data source

- **API**: `https://www.googleapis.com/youtube/v3/videos?chart=mostPopular`
- **Parts fetched**: `snippet`, `statistics`, `contentDetails`
- **Quota cost**: 1 unit per request (free tier: 10,000 units/day)
- **No pip dependencies**: uses only Python stdlib (`urllib`, `json`, `re`)

## Workflow for the AI agent

1. Check `YOUTUBE_API_KEY` is set; if not, guide the user through the platform-specific setup above
2. Run `python3 scripts/fetch-youtube-trending.py [REGION] [COUNT] [CATEGORY]` (use `python` on Windows if `python3` is not in PATH)
3. Present the results; offer to search for more details on a specific video using WebSearch

## Guardrails

- Never fabricate view counts or video titles — all data comes from the API response.
- If the API returns a 403, the key is likely invalid or the quota is exhausted for the day.
- The "global" chart (no region) reflects YouTube's default ranking, which is heavily weighted toward English-language content.
