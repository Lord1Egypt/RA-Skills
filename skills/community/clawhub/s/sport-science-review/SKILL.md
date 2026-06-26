---
name: generate-daily-sports-update
description: Automated sports science intelligence engine — fetches 55+ sources (PubMed, expert blogs, wearable tech), filters noise, translates to Chinese, and syncs to Feishu/Notion.
metadata:
  openclaw.homepage: https://github.com/w2478328197-arch/sports-science-daily
  user-invocable: true
requires.bins:
  - python3
requires.env:
  - FEISHU_APP_ID
  - FEISHU_APP_SECRET
  - FEISHU_RECEIVE_ID
---

# Sports Science Daily — AI Agent Skill

An automated intelligence engine that aggregates **55+ global sports science sources** into a single daily report, with smart filtering, auto-translation, and multi-platform sync.

## What It Does

1. **Fetches** peer-reviewed papers from **23 PubMed journals** (BJSM, Sports Medicine, JSCR, MSSE, etc.)
2. **Crawls** RSS feeds from **14 expert blogs/podcasts** (Huberman, Attia, Nuckols, Dr. Mike, NSCA, etc.)
3. **Monitors** **18 industry sources** (The Quantified Scientist, DC Rainmaker, Oura, Garmin, ScienceDaily, ACSM, etc.)
4. **Filters** noise using a 4-layer keyword system (positive/research/strong/negative keywords + trusted source whitelist)
5. **Translates** all content to Chinese (or any target language) via Google Translate API
6. **Sorts** each section by date (newest first)
7. **Deduplicates** against local history to prevent repeat content
8. **Syncs** the final report as a Feishu Cloud Document with notification card, and optionally to Notion

## Prerequisites

- **Python 3.8+** with `feedparser` and `requests` installed (`pip3 install -r requirements.txt`)
- **Feishu App Credentials** (for cloud document sync):
  - `FEISHU_APP_ID`: Feishu app ID
  - `FEISHU_APP_SECRET`: Feishu app secret
  - `FEISHU_RECEIVE_ID`: Target user/chat ID for message card
- **(Optional) Notion Integration** for Notion page sync:
  - `NOTION_TOKEN` and `NOTION_PAGE_ID`

## Instructions

1.  **Navigate to the project directory**:
    Ensure you are in the `sports-science-daily` project root.

2.  **Run the update**:
    ```bash
    python3 main.py --days 2
    ```

3.  **Available options**:

    | Flag | Default | Description |
    |------|---------|-------------|
    | `--days N` | 7 | Lookback period in days |
    | `--no-history` | off | Force re-fetch all items (ignore dedup) |
    | `--no-bloggers` | off | Skip blogger feeds, only industry + PubMed |
    | `--lang LANG` | zh-CN | Output language (en, es, ja, etc.) |

4.  **Output**:
    - Local Markdown file: `YYYY-MM-DD_运动科学日报.md`
    - Feishu Cloud Document (auto-created with shareable link)
    - Feishu message card sent to configured recipient
    - Updated `processed_history.json` for deduplication

5.  **"No New Content" scenario**:
    If output shows "🎉 没有发现新内容", increase `--days` or use `--no-history`.

## Project Architecture

```
main.py                 # CLI entry point
src/
├── config.py           # All sources, journals, blocklists
├── crawler.py          # RSS + PubMed API fetching
├── formatter.py        # Markdown generation + keyword filtering
├── translator.py       # Google Translate API
├── history.py          # Deduplication management
└── exporters/
    ├── feishu.py       # Feishu cloud doc sync + message card
    └── notion.py       # Notion page sync
```

## Security & Privacy

- **External APIs**: PubMed (eutils.ncbi.nlm.nih.gov), Google Translate, Feishu OpenAPI, Notion API, various RSS feeds
- **Local files**: Reads/writes `processed_history.json` and `.md` reports
- **No PII exposure**: Only fetches public research data and news feeds
