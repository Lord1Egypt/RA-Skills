---
name: web-intel
description: "网络搜索与信息提取统一入口。整合 content-extraction、Jina Reader、Firecrawl、web-access CDP。自动选最经济工具链。可被 BMW（brand-marketing-workflow）、wealth 子代理等直接调用。"
version: 1.0.0
level: L1
tags: [browser, search, extraction, routing, economics, bmw, wealth, finance]
---

# Web Intel — 统一网络检索层

## 职责边界

本技能是**路由层**，不重写任何已有工具。调度链：

```
web-intel
  ├── content-extraction/scripts/extract_router.py  (URL 分类)
  ├── r.jina.ai                                       (轻量全文提取)
  ├── firecrawl CLI                                   (搜索 + 抓取)
  └── web-access CDP Proxy (localhost:3456)           (登录态/反爬)
```

## 三档模式

| 模式 | 场景 | Token 消耗 | 延迟 |
|------|------|-----------|------|
| **fast** | 只需标题+摘要，快速定位 | ~200-500 | <2s |
| **standard** | 需完整页面正文 | ~500-2000 | 2-8s |
| **deep** | 登录内容 / JS重渲染 / 反爬站点 | ~2000-8000 | 10-30s |

## 决策树

### A. 搜索任务（给关键词）

```
[fast]    firecrawl search "query" --limit 5
          → 返回 title + url + snippet

[standard] firecrawl search + Jina 提取 top-1 全文
           → tool: firecrawl_search+jina

[deep]    firecrawl search --scrape --limit 5
          → 反爬/登录页面可升级到 web-access CDP
```

### B. 提取任务（给 URL）

```
Step 0: extract_router.py 判断 URL 类型
  → 微信/飞书/YouTube → 委托 skills/content-extraction（专用 handler）
  → 通用网页 → 继续

[fast]    curl https://r.jina.ai/<url>
[standard] Jina 优先；失败 → firecrawl scrape
[deep]    web-access CDP（localhost:3456）优先；降级 Jina → firecrawl scrape
```

### C. 证券/财经（--type finance）

```
fast:     firecrawl search "$TICKER 财报/行情/股价" --limit 5
standard: 同 fast + Jina 提取 top-1（东方财富/雪球）
deep:     → skills/stock-research-engine（完整基本面分析）
```

### D. 竞品研究（--type competitor，BMW 使用）

```
fast:     firecrawl search "品牌名 营销/产品/用户反馈" --limit 5
standard: fast + Jina 提取各结果全文
deep:     firecrawl search --scrape；需要 CDP 的站点走 web-access
```

## 调用约定（供其他技能/子代理）

```bash
# 搜索
python3 ~/.openclaw/workspace/skills/web-intel/scripts/web_intel.py \
  --query "比亚迪Q1财报" --mode fast --type finance

# URL 提取
python3 ... --url https://example.com --mode standard

# 竞品研究（BMW 调用）
python3 ... --query "小米SU7营销策略" --mode standard --type competitor
```

**标准输出（JSON stdout）**：
```json
{
  "query": "...",
  "mode": "fast",
  "type": "finance",
  "tool_used": "firecrawl_search",
  "results": [{"title": "...", "url": "...", "snippet": "..."}],
  "full_content": null,
  "web_access_available": true,
  "latency_ms": 1200
}
```

## web-access CDP 集成说明

web-access 通过 CDP Proxy（localhost:3456）直连用户 Chrome，天然携带登录态。

**启动 CDP Proxy**（deep 模式前置）：
```bash
bash ~/.openclaw/workspace/skills/web-access/scripts/check-deps.sh
```

**web-intel 在 deep 模式下自动检测 CDP 可用性**（`web_access_available` 字段）。CDP 可用时优先用于提取；不可用时降级到 Jina/Firecrawl。

## 不包含的能力（直接引用现有技能）

| 需求 | 使用技能 |
|------|---------|
| 微信公众号提取 | skills/content-extraction（handler=browser） |
| 飞书文档提取 | skills/content-extraction（handler=feishu） |
| YouTube 转录 | skills/content-extraction（handler=transcript） |
| 浏览器交互/表单 | skills/browser + browser-use |
| 个股深度研究 | skills/stock-research-engine |
| 本地记忆搜索 | skills/search-memory |
| CDP 站点经验库 | skills/web-access/references/site-patterns/ |
