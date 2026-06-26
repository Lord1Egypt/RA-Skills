---
name: tavily-search-darry
description: "Tavily 搜索 API 集成 | Tavily Search API Integration. 高质量网络搜索、新闻聚合、信息调研 | High-quality web search, news aggregation, research. 触发词：搜索、search、tavily、新闻."
metadata:
  openclaw:
    emoji: "🔍"
    category: "search"
    tags: ["search", "tavily", "web-search", "news", "research"]
    requires:
      bins: ["bash"]
---

# Tavily Search

Tavily 是一个专业的搜索 API，提供高质量、快速、结构化的搜索结果。

## 功能

### 网络搜索
- **智能搜索** - LLM 优化的搜索结果
- **内容提取** - 自动提取网页内容摘要
- **相关性评分** - 每个结果带有相关性分数

### 新闻搜索
- **时间过滤** - 按天、周、月、年过滤
- **域名过滤** - 指定搜索特定网站
- **深度搜索** - basic/advanced 搜索模式

### 研究工具
- **crawl** - 网页爬取
- **extract** - 内容提取
- **research** - 深度研究

## 使用方式

### 基本搜索

```bash
./search/scripts/search.sh '{"query": "AI 最新进展", "max_results": 10}'
```

### 新闻搜索

```bash
./search/scripts/search.sh '{"query": "科技新闻", "time_range": "week", "max_results": 10}'
```

### 域名过滤

```bash
./search/scripts/search.sh '{"query": "机器学习", "include_domains": ["arxiv.org", "github.com"]}'
```

## 子技能

- `search` - 网络搜索
- `crawl` - 网页爬取
- `extract` - 内容提取
- `research` - 深度研究

## 认证

使用 Tavily API Key 或 OAuth 认证。

获取 API Key: https://tavily.com

---

*Tavily Search, 智能搜索* 🔍
