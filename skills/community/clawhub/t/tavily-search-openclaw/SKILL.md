---
name: tavily-search-openclaw
version: 1.0.0
homepage: https://github.com/ryan-wuxl/tavily-search
description: Tavily AI Search API integration for OpenClaw. Provides web search capabilities using Tavily's AI-powered search engine.
metadata:
  {
    "openclaw":
      {
        "requires": { "python": ["tavily-python"] },
        "env": ["TAVILY_API_KEY"],
      },
  }
---

# Tavily Search Skill

使用 Tavily AI 搜索引擎进行网络搜索。

## 配置

在 `~/.openclaw/openclaw.json` 中添加：

```json
"tavily": {
  "enabled": true,
  "apiKey": "your-api-key"
}
```

或在环境变量中设置：
```bash
export TAVILY_API_KEY=tvly-xxx
```

## 使用方法

```python
from tavily import TavilyClient

tavily_client = TavilyClient(api_key="your-api-key")
response = tavily_client.search("搜索内容")
```

## API 参数

- `query`: 搜索查询字符串
- `search_depth`: 搜索深度 ("basic" 或 "advanced")
- `include_answer`: 是否包含 AI 生成的答案 (True/False)
- `include_images`: 是否包含图片 (True/False)
- `max_results`: 最大结果数量 (默认 5)

## 示例

```python
response = tavily_client.search(
    query="OpenClaw 是什么？",
    search_depth="advanced",
    include_answer=True,
    max_results=10
)
```
