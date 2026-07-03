---
name: searxng-search
version: "1.0.0"
author: adeeptools
description: >
  SearXNG 元搜索联网搜索技能。通过自建 SearXNG 元搜索引擎聚合百度、Bing 等多个搜索引擎的结构化结果，返回标题、摘要、来源链接。比 HTML 爬虫方案更稳定，通过正式 JSON API 获取搜索结果。适用于需要联网搜索信息、查询资料、查新闻、了解最新动态的场景。
platforms: [windows, macos]
metadata:
  hermes:
    tags: [search, web-search, searxng, meta-search, chinese, baidu, bing]
    config:
      searxng_endpoint:
        type: string
        default: "http://175.24.233.186:8890"
        description: "SearXNG 实例地址，用户可自定义为自建实例"
  author: "adeeptools"
  category: "information"
  capabilities:
    - "web.search.searxng"
    - "web.search.multi-engine"
    - "web.search.quick"
  permissions:
    - "network.web"
---

# SearXNG 元搜索联网搜索

本技能用于普通联网搜索。它通过自建的 SearXNG 元搜索引擎聚合百度、Bing 等多个搜索引擎的结果，返回结构化 JSON（标题、链接、摘要、来源引擎）。不需要打开智能浏览器，不需要用户登录，也不依赖浏览器插件桥。

相比 `baidu-mobile-search` 的 HTML 爬虫方案，SearXNG 通过正式 JSON API 获取结果，更稳定、更不容易被反爬封锁。

## 何时使用

用户提出以下需求时，**优先使用本技能**（优先级高于 baidu-mobile-search）：

- 搜索某个关键词、人物、公司、产品、新闻、政策、资料。
- 查询最新公开信息、网络资料、公开网页线索。
- 需要先判断有哪些可靠来源，再决定是否打开详情页。
- 需要同时从多个搜索引擎获取结果。

如果 SearXNG 实例不可用或返回空结果，可降级使用 `baidu-mobile-search` 作为备选。
如果需要登录态、点击网页筛选、处理复杂网页交互、进入多个详情页逐步读取，再改用 `smart-browser` 智能网页助手。

## 命令

搜索关键词（默认使用百度+Bing引擎）：

```bash
python "${HERMES_HOME:-$HOME/.hermes}/skills/searxng-search/scripts/searxng_search.py" "<关键词>"
```

限制结果数量：

```bash
python "${HERMES_HOME:-$HOME/.hermes}/skills/searxng-search/scripts/searxng_search.py" "<关键词>" --limit 10
```

指定搜索引擎：

```bash
python "${HERMES_HOME:-$HOME/.hermes}/skills/searxng-search/scripts/searxng_search.py" "<关键词>" --engines baidu,bing
```

输出 JSON：

```bash
python "${HERMES_HOME:-$HOME/.hermes}/skills/searxng-search/scripts/searxng_search.py" "<关键词>" --json
```

指定 SearXNG 实例地址（也可通过 SEARXNG_ENDPOINT 环境变量设置）：

```bash
python "${HERMES_HOME:-$HOME/.hermes}/skills/searxng-search/scripts/searxng_search.py" "<关键词>" --endpoint http://175.24.233.186:8890
```

## 回复要求

- 先根据 `RESULTS_JSON` 或 `RESULTS` 总结，不要编造搜索结果里没有的信息。
- 对事实类、新闻类、政策类回答，至少引用 2 个搜索结果来源；只有一个可靠结果时要说明来源有限。
- 结果中的 `source` 字段标明了来源引擎（如 baidu、bing），可以据此判断结果的可信度。
- 如果输出 `SEARXNG_SEARCH_STATUS: EMPTY`，告诉用户当前没有搜索结果，建议换关键词或稍后重试。
- 如果输出 `SEARXNG_SEARCH_STATUS: ERROR`，简要说明连接失败，可降级使用 `baidu-mobile-search`。
- 如果有 `UNRESPONSIVE_ENGINES`，部分引擎超时但仍有其他引擎返回结果，正常使用即可。
- 如果有 `SUGGESTIONS`，可以参考建议关键词进一步搜索。

## 推荐流程

普通搜索任务：

```text
searxng_search.py "<关键词>" -> 阅读 RESULTS/RESULTS_JSON -> 引用来源总结
```

SearXNG 不可用时降级：

```text
searxng_search.py "<关键词>" -> ERROR -> baidu_mobile_search.py "<关键词>" -> 总结
```

需要详情页确认：

```text
searxng_search.py "<关键词>" -> 选择最相关来源 -> smart-browser goto "<结果链接>" -> extract -> 总结
```
