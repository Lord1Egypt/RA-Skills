---
name: tavily-research-pro
description: Professional AI-powered search and deep research engine. Features multi-dimensional data aggregation, semantic analysis, and automated report generation for structured information gathering.
homepage: https://tavily.com
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["node"],"env":["TAVILY_API_KEY"]},"primaryEnv":"TAVILY_API_KEY"}}
---

# Tavily Research Pro (科研洞察引擎)

Professional-grade tool designed for researchers and analysts to gather high-quality, structured information from the web.

## 🛡️ Privacy & Data Security (隐私与安全说明)

To comply with security audits and ensure data transparency, please note:
* **Data Transmission**: This skill transmits user-provided search queries and specified target URLs to `api.tavily.com` for processing and information extraction.
* **Credential Protection**: The `TAVILY_API_KEY` is accessed exclusively from your local environment variables and is never stored, logged, or shared with any third party other than the official Tavily API endpoint.
* **Compliance**: This tool is intended for searching and analyzing publicly available web data for research purposes only.

---

## 核心功能 (Core Features)

### 1. 结构化搜索 (Structured Search)
Deep research mode for high-accuracy information retrieval.
```bash
node {baseDir}/scripts/search.mjs "Quantum computing commercialization" --deep
```

## 2. 公开信息语义分析 (Public Sentiment Analysis) 🆕
分析当前互联网对某个话题的“体感温度”。
```bash
node {baseDir}/scripts/sentiment.mjs "Apple Vision Pro"
```

## 3. 自动化研究简报 (Automated Research Report) 🆕
将长网页转化为结构化的情报简报，自动识别关键角色和影响。
```bash
node {baseDir}/scripts/report.mjs "[https://example.com/tech-news](https://example.com/tech-news)"
```

## 参数说明 (Options)
-n <count>: Number of results (default 5).

--deep: Enable advanced deep research mode.

--topic <news|general>: Specify search category.

--days <n>: Limit news search to the last n days.

Environment Requirement: A valid TAVILY_API_KEY must be configured in your environment.