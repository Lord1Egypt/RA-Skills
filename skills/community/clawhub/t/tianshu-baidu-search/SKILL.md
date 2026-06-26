---
name: tianshu-baidu-search
description: Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics.
metadata:
  openclaw:
    primaryEnv: BAIDU_API_KEY
    requires:
      env:
        - BAIDU_API_KEY
---

# 百度搜索 (tianshu-baidu-search)

使用百度 AI 搜索 API 进行网页搜索，Node.js 实现，无需 Python。

## 前置配置

- `BAIDU_API_KEY` - 从 https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey 获取

## 用法

```bash
node scripts/search.js '{"query":"人工智能"}'
node scripts/search.js '{"query":"最新新闻","freshness":"pd","count":20}'
```

## 参数

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| query | string | 是 | - | 搜索关键词 |
| count | int | 否 | 10 | 返回数量，1-50 |
| freshness | string | 否 | - | pd=24h, pw=7天, pm=31天, py=365天，或 YYYY-MM-DDtoYYYY-MM-DD |
