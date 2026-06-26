---
name: torrent-downloader
description: >
  Search magnet links for movies/TV shows and download via qBittorrent.
  Automatically scores and ranks results by subtitle availability and resolution.
  Triggers: download movie, download TV show, magnet download, BT download, torrent download, find resources,
  下载电影, 下载剧, 磁力下载, BT下载, 种子下载, 帮我下, 找资源.
metadata:
  openclaw:
    emoji: "🧲"
    requires:
      bins: ["python3"]
---

# Torrent Downloader

Search magnet links for movies and TV shows, auto-rank by quality, and push to qBittorrent for download.

## Prerequisites

- **qBittorrent** with Web UI enabled (default: `http://localhost:8080`)
- **Python 3** (no extra packages needed — uses only stdlib)

## Configuration

Set these environment variables (or edit the scripts directly):

| Variable | Default | Description |
|----------|---------|-------------|
| `QBT_URL` | `http://localhost:8080` | qBittorrent Web UI URL |
| `QBT_USER` | `admin` | qBittorrent username |
| `QBT_PASS` | `adminadmin` | qBittorrent password |

## Workflow

1. Search magnet links using keyword
2. Auto-score results (built-in Chinese subtitles > external subs; 1080P/4K preferred)
3. Pick the best result and push to qBittorrent
4. Report download status to user

## Search

```bash
python3 {baseDir}/scripts/search_magnet.py "keyword" [--prefer-4k] [--limit N]
```

- Default preference: 1080P. Add `--prefer-4k` for 4K priority.
- Scoring: built-in Chinese subtitles (+100) > external subtitles (+50); 4K (+80/40) > 1080P (+60/30)
- Output: JSON with `results[].magnet`, `results[].title`, `results[].score`

## Download

```bash
python3 {baseDir}/scripts/qbt_download.py "<magnet_url>" [--category CATEGORY]
```

## Check Download Status

```bash
python3 {baseDir}/scripts/qbt_download.py --status
```

## Agent Behavior Rules

- After search, **pick the highest-scored result and start download** — don't show the search list to user
- After download starts, tell user: title, file size, resolution info
- If no results found, retry with English title
- Honor user's resolution preference when specified
