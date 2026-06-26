---
name: web-search-minimax
description: 网络搜索技能，使用 Minimax Coding Plan Search API 进行网络搜索
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["node"]}}}
---

# Web Search

使用 Minimax Coding Plan Search API 进行网络搜索，返回搜索结果和相关搜索建议。

## 使用方法

```bash
node {baseDir}/scripts/search.cjs "搜索关键词"
```

## 示例

```bash
# 基本搜索
node {baseDir}/scripts/search.cjs "今天天气怎么样"

# 搜索编程问题
node {baseDir}/scripts/search.cjs "Python 教程"

# 搜索最新新闻
node {baseDir}/scripts/search.cjs "AI 发展动态"
```

## 数据来源

API Key 从环境变量读取：
- 环境变量：`MINIMAX_API_KEY`
- API Host：固定为 `https://api.minimaxi.com`
- API 端点：`/v1/coding_plan/search`
- 请求参数：`q` (查询词)

## 返回结果格式

- **organic**: 搜索结果列表，每条包含 title、link、snippet、date
- **related_searches**: 相关搜索建议列表

## 使用场景

- 查询实时信息
- 查找技术文档
- 获取新闻资讯
- 搜索教程资源
