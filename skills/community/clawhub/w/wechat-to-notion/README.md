# wechat-to-notion

[中文文档](README.zh-CN.md)

Save WeChat official account articles to a Notion database. Automatically extracts title, cover image, and body content (paragraphs, headings, images, code blocks, lists), then uses AI to generate keywords, a review comment, and a star rating.

## Features

- **Article Fetching** — Parses WeChat article HTML, extracts rich text (bold/italic), code blocks, lists, and images
- **Smart Analysis** — AI extracts 3-5 core keywords, evaluates readability and value, assigns a 1-5 star rating
- **Featured Tag** — Articles rated 3 stars or above are automatically tagged "Featured" for easy filtering
- **Notion Sync** — Auto-detects database fields, writes content blocks in batches of 100, posts comment to the Comments panel
- **Field Adaptive** — Matches fields by type (not name), compatible with Notion databases in any language

## Quick Start

### 1. Get a Notion API Key

1. Go to [My Integrations](https://notion.so/my-integrations) → **+ New integration** → copy the key (starts with `ntn_`)
2. Open your target Notion database → **...** → **Connect to** → select your integration

### 2. Create a Notion Database

The database needs the following fields (names can be customized — the script matches by type):

| Field Type | Purpose | Example Name |
|-----------|---------|-------------|
| Title | Article title | Title |
| URL | Article link | URL |
| Date | Read time | Read Time |
| Select | Star rating | Rating |
| Multi-select | Keyword tags | Tags |

Suggested select options: ⭐, ⭐⭐, ⭐⭐⭐, ⭐⭐⭐⭐, ⭐⭐⭐⭐⭐

### 3. Usage

```bash
# Set API Key
export NOTION_API_KEY="ntn_xxx"

# Fetch article
python3 scripts/fetch_wechat.py <wechat_article_url> > /tmp/wx_article.json

# Save to Notion
python3 scripts/save_to_notion.py \
  /tmp/wx_article.json \
  <notion_database_url> \
  <wechat_article_url> \
  "2026-03-17T10:00:00+08:00" \
  "Claude Code,MCP,Agentic Workflow" \
  "Well-structured, solid content density, great for devs wanting a quick start" \
  4
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| article_json | Yes | Output file path from fetch_wechat.py |
| notion_url | Yes | Notion database URL |
| article_url | Yes | Original WeChat article URL |
| read_time | No | ISO 8601 datetime (defaults to current time) |
| keywords | No | Comma-separated keywords |
| comment | No | One-sentence review (posted to Comments panel) |
| rating | No | 1-5 star rating (>=3 auto-adds "Featured" tag) |

## Design

This project is primarily built as an [OpenClaw](https://github.com/nicholasgriffintn/OpenClaw) skill — `SKILL.md` defines the complete workflow, and OpenClaw handles environment variable injection and toolchain checks automatically.

However, the scripts have zero framework dependencies — they only need `python3` and `curl`. You can integrate them into any AI agent platform (Claude Code, Cursor, Windsurf, etc.) as long as the agent can read instructions from `SKILL.md` and execute shell commands.

### As an OpenClaw Skill

After installation, simply send a WeChat article link in a conversation to trigger the automated pipeline: fetch → AI analysis (keywords + comment + rating) → save to Notion.

```bash
openclaw config set skills.entries.wechat-to-notion.NOTION_API_KEY "ntn_xxx"
```

### As a Generic Agent Skill

Clone this repo into your agent's working directory, ensure `NOTION_API_KEY` is available as an environment variable, and have the agent follow the three-step workflow in `SKILL.md` (fetch → analyze → save). No additional adaptation needed.

## Project Structure

```
├── SKILL.md                    # OpenClaw skill definition
├── README.md                   # English
├── README.zh-CN.md             # Chinese
└── scripts/
    ├── fetch_wechat.py         # WeChat article fetching and parsing
    └── save_to_notion.py       # Notion writer (field detection, batch writes, comments)
```

## License

MIT
