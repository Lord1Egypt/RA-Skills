# youtube-outlier-skill

Finds outlier/trending YouTube videos by niche keyword, analyzes main concepts, and stores to Google Sheet. Posts summary to Discord.

## Parameters Supported
- `niche` (single or comma-separated list)

## Usage
Via Discord or API call:

```
/ytoutlier AI news
```

## Discord Command Registration
Add to your Discord/OpenClaw config, or copy below to your skill manifest:

```yaml
commands:
  - name: ytoutlier
    description: Find trending YouTube outlier videos in a niche.
    usage: /ytoutlier <niche>
    handler: youtube-outlier-skill
```

## Requirements
- Google Sheets API credentials (edit access to your target sheet)
- Discord bot token and channel ID
- YouTube Data API key (if not handled by youtube-api-skill)

## Environment variables
See `.env.example` for all required variables.

---

Skill created for Danny by Soma 🧘‍♂️ (OpenClaw)
