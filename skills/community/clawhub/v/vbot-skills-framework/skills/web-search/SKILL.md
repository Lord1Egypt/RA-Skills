---
name: web-search
description: Use when user asks to search the web, find online info, or lookup something that needs current data.
triggers: ["搜索", "search", "联网", "查找", "online"]
version: 1.0.0
---

# 🔍 Web Search Skill

> Search the web and return real-time information

## Usage

When user wants to search:
1. Use `tianji-yuanbao-standard-search` skill for search
2. Parse results and summarize key points
3. Return with sources when possible

## Example Triggers

- "搜索最新的 AI 新闻"
- "search for X"
- "帮我查一下这个..."
- "联网查找..."

## Response Format

```
📊 Search Results for: [query]

1. [Title](URL)
   Brief description...

2. ...

💡 Key findings:
- Point 1
- Point 2
```

## Tips

- Be specific in search queries
- Include date/time if user asks for "latest"
- Verify results are relevant before presenting
