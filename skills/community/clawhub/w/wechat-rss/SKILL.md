---
name: wechat-rss
description: 通过 wcrss.com API 获取并展示微信公众号的最新文章。当用户请求查看微信公众号文章、获取公众号最新发布内容、阅读微信RSS订阅或浏览公众号内容时使用此技能。该技能会从环境变量 WCRSS_API_KEY 中读取 API Key，并调用 wcrss.com 的接口来获取文章数据。
---

# WeChat RSS Skill

Fetch and display the latest articles from WeChat public accounts using the wcrss.com API.

## Prerequisites

Before using this skill, the user must:

1. Register an account at https://wcrss.com/
2. Add favorite public accounts at https://wcrss.com/publishers
3. Generate an API key at https://wcrss.com/settings
4. Save the API key as an environment variable `WCRSS_API_KEY`

## Python Scripts

This skill uses Python scripts for data fetching:

- **Location:** `scripts/wechat_rss.py` (relative to skill directory)
- **Commands:**
  - `python scripts/wechat_rss.py fetch <recentDays> <num>` - Fetch articles (auto-cached for 1 hour)
  - `python scripts/wechat_rss.py get <index>` - Get single article by index
  - `python scripts/wechat_rss.py count` - Get total articles count

## Workflow for Agent

### Step 1: Fetch Articles List

Execute the Python script to fetch articles:

```bash
python scripts/wechat_rss.py fetch 3 10
```

### Step 2: Get Total Articles Count

```bash
python scripts/wechat_rss.py count
```

### Step 3: Process Each Article

For each article index from 0 to (count-1), call:

```bash
python scripts/wechat_rss.py get <index>
```

This returns:
```json
{
  "title": "文章标题",
  "author": "公众号名称",
  "content_html": "<p>HTML内容...</p>",
  "url": "https://example.com/s/article",
  "publish_time": "%Y-%m-%d %H:%M",
  "description": "文章简介"
}
```

### Step 4: Summarize Each Article

For each article, use the LLM to summarize the `content_html` into key points (bullet list).

**LLM Prompt:**
```
请从以下文章内容中提取关键要点，以条目的形式列出：

标题：{title}
作者：{author}
内容：{content_html}
时间：{publish_time}

请提取3-8个核心要点，每个要点用一句话概括。
```

### Step 5: Display Results

For each article, display in this format:

```
【{序号}】{标题}
作者：{公众号名称}  {时间}
文章要点：
- 要点1
- 要点2
- 要点3
原文链接：{url}
---
```

## Error Handling

- If "WCRSS_API_KEY environment variable not set" error occurs, guide the user to configure the API key
- If API returns an error, display the error message to the user
- If no articles are found, inform the user and suggest checking their followed publishers
