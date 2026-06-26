---
name: wechat-mp-to-notion
description: Fetch WeChat public account (微信公众号) articles from mp.weixin.qq.com links and save them into Notion as structured pages. Use when the user wants to archive a 微信公众号 article to Notion, save a WeChat mp article into a Notion page/database, or convert a public WeChat article into a readable Notion document.
---

# WeChat MP article → Notion

Save a public WeChat article into Notion.

## What this skill does

- Fetch article HTML from `https://mp.weixin.qq.com/s/...`
- Extract title / author / publish date
- Parse article body into readable text blocks
- Preserve image positions with external image URLs where possible
- Create a new Notion page under a target page or in a target database

## Use

Run the script:

```bash
python3 /root/.openclaw/workspace/skills/wechat-mp-to-notion/scripts/save_wechat_mp_to_notion.py <wechat_url> <notion_parent_id> [--parent-type page|database]
```

Examples:

```bash
python3 /root/.openclaw/workspace/skills/wechat-mp-to-notion/scripts/save_wechat_mp_to_notion.py "https://mp.weixin.qq.com/s/xxxx" 32c51492e44780c48647f03febbc6c84
python3 /root/.openclaw/workspace/skills/wechat-mp-to-notion/scripts/save_wechat_mp_to_notion.py "https://mp.weixin.qq.com/s/xxxx" c5f3656c2e8741e88f53a00faf66355e --parent-type database
```

## Notes

- Require `NOTION_API_KEY`
- The target Notion page/database must be shared with the `openclaw` integration
- Prefer `page` parent when archiving long-form articles
- Prefer `database` parent when the user explicitly wants one row per article
- If the article is very long, the script chunks content into multiple append requests
