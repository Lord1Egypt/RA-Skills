---
name: tavily-insight
description: 增强型 AI 搜索与深度洞察引擎。除了搜索，还能进行情绪分析和情报汇总。
homepage: https://tavily.com
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["node"],"env":["TAVILY_API_KEY"]},"primaryEnv":"TAVILY_API_KEY"}}
---

# Tavily Insight Engine (洞察引擎)

这是对标准 Tavily 搜索的创意升级，专为需要“深度理解”而不仅仅是“数据搬运”的 AI 代理设计。

## 1. 基础搜索 (Search)
```bash
node {baseDir}/scripts/search.mjs "量子计算的商业化进展" --deep
```

## 2. 互联网情绪风向标 (Vibe Check) 🆕
分析当前互联网对某个话题的“体感温度”。
```bash
node {baseDir}/scripts/vibe.mjs "Apple Vision Pro"
```

## 3. 任务简报 (Mission Brief) 🆕
将长网页转化为结构化的情报简报，自动识别关键角色和影响。
```bash
node {baseDir}/scripts/brief.mjs "https://example.com/tech-news"
```

## 选项说明
- `-n <count>`: 结果数量 (默认 5)
- `--deep`: 开启深度研究模式
- `--topic <news|general>`: 搜索类别
- `--days <n>`: 搜索最近 n 天的新闻

> **注意**: 必须在环境变量中配置 `TAVILY_API_KEY`。