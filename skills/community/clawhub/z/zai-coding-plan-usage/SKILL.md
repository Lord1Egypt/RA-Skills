---
name: zai-coding-plan-usage
description: Query Z.ai (智谱) Coding Plan usage and quota limits. Track token consumption, MCP usage, and subscription status. Use when user asks about "智谱用量"、"ZAI usage"、"coding plan usage"、"quota"、"智谱配额"。
---

# Z.ai Coding Plan Usage Query

Query Z.ai (智谱 AI) Coding Plan usage and quota limits.

## Usage

Just say:
- "智谱用量查询"
- "Check ZAI usage"
- "coding plan usage"

## Script

```bash
node ~/.openclaw/workspace/skills/zai-coding-plan-usage/scripts/query-usage.mjs
```

## API Endpoints

| API | Endpoint | Description |
|-----|----------|-------------|
| Model usage | `/api/monitor/usage/model-usage` | Model call statistics |
| Tool usage | `/api/monitor/usage/tool-usage` | Tool call statistics |
| Quota limit | `/api/monitor/usage/quota/limit` | Quota limits |

## Notes

- API Key is automatically read from OpenClaw config or environment variables
- Works only in environments with Z.ai API configured
