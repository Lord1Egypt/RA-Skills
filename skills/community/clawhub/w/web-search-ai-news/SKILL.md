---
slug: web_search_ai_news
name: Web Search AI News
description: 实时获取最新的人工智能行业新闻和动态
version: 1.0.0
tags:
  - news
  - ai
  - search
  - web
author: stringtwb1220
license: MIT
repository: https://github.com/stringtwb1220/web_search_ai_news
---

# Web Search AI News

实时获取最新的人工智能行业新闻和动态。

## Triggers

- "AI 新闻"
- "最新大模型消息"
- "查一下 AI 资讯"
- /ai news/i
- /latest (llm|AI|artificial intelligence) update/i

## Capability

```json
{
  "capability": "web_fetch",
  "parameters": {
    "urls": [
      "https://www.thepaper.cn/",
      "https://www.huxiu.com/",
      "https://www.tmtpost.com/"
    ],
    "maxChars": 10000
  }
}
```

## Post-Processing

获取新闻后，自动通过 SMTP 发送邮件至指定收件人。
邮件配置见 `~/.config/himalaya/config.toml`
