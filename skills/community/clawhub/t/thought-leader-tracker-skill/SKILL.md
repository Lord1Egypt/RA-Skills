---
name: thought-leader-tracker
description: Daily automated collection of podcasts, interviews, and videos from thought leaders across YouTube, Apple Podcasts, and Spotify. Generates Markdown reports with content summaries, key points, and common theme analysis. Use when tracking thought leader content, creating daily digests, analyzing industry trends, or monitoring specific experts' new releases.
---

# Thought Leader Tracker

Automated system for collecting and analyzing content from thought leaders across multiple platforms.

## Quick Start

```bash
# Collect content from last 7 days
~/.openclaw/skills/thought-leader-tracker/thought-leader-tracker.sh collect

# Collect content from last 30 days
~/.openclaw/skills/thought-leader-tracker/thought-leader-tracker.sh collect 30

# List tracked thought leaders
~/.openclaw/skills/thought-leader-tracker/thought-leader-tracker.sh list
```

## Configuration

Edit `config.json` to customize:

### Add New Thought Leader

```json
{
  "name": "Your Name",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "platforms": ["youtube", "apple-podcasts", "spotify"]
}
```

### Default Thought Leaders

- Boris Cherny (Performance, React, JavaScript)
- 李飞飞 Fei-Fei Li (AI, Computer Vision)
- Elen Verna (Product Management, SaaS)
- Peter Steinberger (Software Development)
- Dan Koe (Creator Economy)
- Demis Hassabis (DeepMind, AI, AGI)

## Output Format

Reports are saved to `daily-logs/` with:

- **Title** - Content title
- **Link** - Direct URL to content
- **Publish Date** - When content was released
- **Summary** - Content description
- **Key Points** - Extracted main points
- **Common Themes** - Topics mentioned by 2+ thought leaders

## API Setup (Production)

For full functionality, configure:

1. **YouTube Data API**: Set `YOUTUBE_API_KEY` environment variable
2. **Spotify API**: Configure OAuth2 credentials

Current implementation uses available public APIs (iTunes Search) and placeholders for authenticated services.

## Automation

Add to crontab for daily collection:

```bash
# Daily at 8 AM
0 8 * * * ~/.openclaw/skills/thought-leader-tracker/thought-leader-tracker.sh collect 7
```

## File Structure

```
thought-leader-tracker/
├── SKILL.md
├── thought-leader-tracker.sh    # Main CLI script
├── config.json                  # Configuration
├── scripts/
│   └── collector.js             # Content collection logic
└── daily-logs/                  # Generated reports
    └── daily-report-YYYY-MM-DD-7d.md
```
