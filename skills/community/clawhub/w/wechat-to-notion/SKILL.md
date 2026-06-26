---
name: wechat-to-notion
description: Save WeChat public account articles to a Notion database. Use when user sends a mp.weixin.qq.com link and wants to save/archive it to Notion. Fetches title, cover image, body content (paragraphs, headings, images, code blocks, lists) and writes them as Notion blocks.
metadata:
  {
    "openclaw": {
      "emoji": "📰",
      "requires": { "env": ["NOTION_API_KEY"], "bin": ["python3", "curl"] },
      "primaryEnv": "NOTION_API_KEY"
    }
  }
---

# wechat-to-notion

Save a WeChat article to Notion in three steps: fetch → analyze → save.

## Configuration Check (Do This First)

Check if the Notion API key is configured:

```bash
echo ${NOTION_API_KEY:0:8}...
```

**If missing**, tell the user:

> You haven't configured a Notion API key yet:
> 1. Go to https://notion.so/my-integrations → **+ New integration** → copy the key (starts with `ntn_`)
> 2. Open your Notion database → **...** → **Connect to** → select your integration
> 3. Set the key in your OpenClaw config — **do not paste it into chat**:
>    ```
>    openclaw config set skills.entries.wechat-to-notion.NOTION_API_KEY "ntn_xxx"
>    ```
>    OpenClaw will inject it as `NOTION_API_KEY` automatically.

⚠️ Never ask the user to send the API key as a chat message — it will be exposed in conversation logs.

## Setup (One-time)

Ask if the user has an existing Notion database. If yes, use it directly. If no, ask for a parent page URL and create one:

```bash
curl -s -X POST https://api.notion.com/v1/databases \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"type": "page_id", "page_id": "<parent_page_id>"},
    "title": [{"type": "text", "text": {"content": "WeChat Articles"}}],
    "properties": {
      "Title": {"title": {}},
      "URL": {"url": {}},
      "Read Time": {"date": {}},
      "Rating": {"select": {"options": [
        {"name": "⭐", "color": "gray"},
        {"name": "⭐⭐", "color": "gray"},
        {"name": "⭐⭐⭐", "color": "yellow"},
        {"name": "⭐⭐⭐⭐", "color": "orange"},
        {"name": "⭐⭐⭐⭐⭐", "color": "red"}
      ]}},
      "Tags": {"multi_select": {}},
      "Notes": {"rich_text": {}}
    }
  }'
```

> Match field names to the user's language (e.g. Chinese users get Chinese field names).

## Workflow

### Step 1: Fetch article

```bash
python3 {skillDir}/scripts/fetch_wechat.py <wechat_url> > /tmp/wx_article.json
```

### Step 2: Analyze (inline — reason directly, no subprocess)

Use the `read` tool to load `/tmp/wx_article.json`. Read the `title` and text content from `blocks`, then produce two outputs by reasoning directly:

**Keywords (3–5):**
- Only extract core concepts: the specific technologies, products, or domain terms that define what this article is actually about
- Omit generic/broad terms (e.g. "AI", "efficiency", "productivity", "tools", "development")
- Comma-separated, preserve original casing

**Rating (1–5 stars):**
Based on readability and value, give a star rating:
- ⭐ (1): waste of time — clickbait, no substance, or unreadable
- ⭐⭐ (2): below average — padded, shallow, or poorly organized
- ⭐⭐⭐ (3): decent — has useful content but nothing exceptional
- ⭐⭐⭐⭐ (4): good — well-written, actionable, worth bookmarking
- ⭐⭐⭐⭐⭐ (5): excellent — insightful, well-structured, a must-read in its domain

3 stars and above automatically get a "Featured" tag.

**Comment (1 sentence, written in the user's language):**
Evaluate the article's **readability** and **value**, not summarize its content. Focus on:
- Is it well-structured and easy to follow, or rambling and padded?
- Does it deliver actionable insight, or is it surface-level fluff?
- Who would actually benefit from reading this?
- Example: "Well-structured, flows from theory to hands-on smoothly — ideal for devs wanting to get started with MCP (refreshingly no filler)"
- Example: "Clickbait title, buries the lead under three screens of preamble — the core point could fit in a single tweet"
- Keep it under 35 words. Be direct — praise or criticize with specifics, no hedging.

### Step 3: Save to Notion

```bash
python3 {skillDir}/scripts/save_to_notion.py \
  /tmp/wx_article.json \
  <notion_db_url> \
  <wechat_url> \
  <read_time_iso8601+08:00> \
  "<kw1>,<kw2>,<kw3>" \
  "<comment>" \
  <rating>
```

- `read_time`: current time in the user's local timezone as ISO 8601 with offset, e.g. `2026-03-12T14:00:00+08:00`
- `keywords`: comma-separated string
- `comment`: the single-sentence comment from Step 2
- `rating`: integer 1–5 (star rating); 3+ automatically adds "Featured" to tags

The script auto-detects field names from the database schema by type (`title`, `url`, `date`, `select`, `multi_select`), writes all content blocks in batches of 100, and posts the comment to the Notion Comments panel.

## Notes

- Cover image: extracted from `og:image` meta tag, inserted as the first block
- Rich text (bold/italic), code blocks, and lists are preserved by `fetch_wechat.py`
- Read time defaults to current system time with local UTC offset if omitted
- The comment appears in the Notion Comments panel, not in the page body
- Field names are language-agnostic — the script maps by type, not by name
