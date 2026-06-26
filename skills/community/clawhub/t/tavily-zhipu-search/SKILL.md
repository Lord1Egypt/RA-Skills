---
name: web-search
description: 统一网络搜索（Tavily 优先 + 智谱兜底）。当用户需要搜索最新新闻、实时信息、查询网络资料时使用此 skill。优先 Tavily（分钟级实时），失败自动回退智谱 MCP web_search_prime（Coding Plan 免费额度）。
---

# Web Search（统一搜索）

Tavily 优先，智谱兜底。一个命令搞定。

## 使用

```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "搜索关键词"
python3 ~/.openclaw/skills/web-search/scripts/search.py "关键词" --days=1
```

## 回退逻辑

1. **Tavily**（需 `TAVILY_API_KEY`）→ 实时，分钟级更新，含 AI 摘要
2. **智谱 Zhipu**（需 `ZHIPU_API_KEY`）→ Coding Plan 免费搜索额度
3. 两者都不可用 → 报错

## 环境变量

| 变量 | 用途 | 必需 |
|------|------|------|
| `TAVILY_API_KEY` | Tavily 搜索 API | 推荐配置 |
| `ZHIPU_API_KEY` | 智谱 Coding Plan | 自动从 openclaw.json 读取 |
