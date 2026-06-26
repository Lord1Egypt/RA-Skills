# smart-research

> 多引擎搜索 + 多级降级抓取 + 结构化研究结果 — 零 API Key

[![OpenClaw 兼容](https://img.shields.io/badge/OpenClaw-Compatible-brightgreen)](https://github.com/openclaw)
[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue)](#license)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue)](#requirements)

---

## 功能特点

- **多引擎并行搜索** — 同时查询 3 个搜索引擎（百度 via baidusearch、DuckDuckGo Lite HTML、Bing）
- **多级降级抓取** — 自动在 5 种抓取策略间降级：crawl4ai → Jina Reader → markdown.new → defuddle → Playwright
- **4 种便捷 Action** — `research`、`search`、`fetch`、`deep_search`，覆盖不同使用场景
- **结构化输出** — 干净的 JSON，包含标题、URL、摘要、来源和置信度评分
- **零 API Key** — 完全基于免费公开服务构建
- **智能限流** — 内置延迟和代理轮换，避免被封禁
- **隐私优先** — 不收集数据，不上报任何遥测信息

---

## 快速开始

### 1. 安装依赖

```bash
cd ~/.openclaw/skills/smart-research
uv pip install --system -r requirements.txt
```

### 2. 安装 Playwright 浏览器（可选，建议安装）

```bash
uv run playwright install chromium
```

### 3. 运行测试

```bash
python3 scripts/smart_research.py '{"action":"search","query":"测试","num_results":3}'
```

### 4. 4 种 Action 说明

| Action | 说明 |
|--------|------|
| `search` | 多引擎搜索，返回结构化结果 |
| `fetch` | 抓取单个 URL，自动多级降级 |
| `research` | 深度研究：搜索 → 取前 N 条 → 抓取摘要 |
| `deep_search` | 全引擎扫射，并行搜索后合并去重 |

---

## 架构说明

```
用户请求 (action + query/URL)
         │
         ▼
   ┌─────────────────────────────────┐
   │      smart_research.py          │
   │      (入口文件，参数解析)         │
   └───────────────┬─────────────────┘
                   │
      ┌────────────┴────────────┐
      │                         │
      ▼                         ▼
  搜索引警 (10+ 并行)        抓取策略 (5级降级)
      │                         │
      │  ┌─────────────────────▼──────────────────────┐
      │  │  降级链顺序:                               │
      │  │  1. crawl4ai (无头浏览器, 15s)             │
      │  │  2. Jina Reader (r.jina.ai, 10s)          │
      │  │  3. markdown.new (markdown.new/{url}, 8s) │
      │  │  4. defuddle (defuddle.md/{url}, 8s)      │
      │  │  5. Playwright (完整JS渲染, 30s)          │
      │  └────────────────────────────────────────────┘
      │
      ▼
  结果聚合与去重
         │
         ▼
   结构化 JSON 输出
```

---

## 使用示例

### 1. `search` — 多引擎搜索

```bash
python3 scripts/smart_research.py '{
  "action": "search",
  "query": "OpenClaw 智能体框架",
  "num_results": 5
}'
```

**示例输出：**
```json
{
  "status": "success",
  "action": "search",
  "query": "OpenClaw 智能体框架",
  "total_results": 12,
  "results": [
    {
      "title": "OpenClaw - 智能体编排框架",
      "url": "https://github.com/openclaw/openclaw",
      "snippet": "一个多智能体编排系统...",
      "source": "bing",
      "engine": "multi",
      "confidence": 0.95
    }
  ]
}
```

---

### 2. `fetch` — 抓取单个 URL

```bash
python3 scripts/smart_research.py '{
  "action": "fetch",
  "url": "https://example.com/article",
  "max_chars": 5000
}'
```

**示例输出：**
```json
{
  "status": "success",
  "action": "fetch",
  "url": "https://example.com/article",
  "title": "文章标题",
  "content": "文章全文内容...",
  "fetched_from": "jina_reader",
  "char_count": 4850
}
```

---

### 3. `research` — 深度研究

```bash
python3 scripts/smart_research.py '{
  "action": "research",
  "query": "2026年最新AI Agent发展趋势",
  "num_results": 5,
  "deep": true
}'
```

**示例输出：**
```json
{
  "status": "success",
  "action": "research",
  "query": "2026年最新AI Agent发展趋势",
  "summary": "来自5个来源的关键发现...",
  "sources": [
    {
      "title": "...",
      "url": "https://...",
      "summary": "..."
    }
  ],
  "engines_used": ["baidu", "bing", "google"]
}
```

---

### 4. `deep_search` — 全引擎深度搜索

```bash
python3 scripts/smart_research.py '{
  "action": "deep_search",
  "query": "Python 异步编程最佳实践",
  "num_results": 10
}'
```

**示例输出：**
```json
{
  "status": "success",
  "action": "deep_search",
  "query": "Python 异步编程最佳实践",
  "total_results": 38,
  "deduplicated": 12,
  "results": [...],
  "engines_queried": ["baidu", "bing", "google", "duckduckgo", "sogou", "so360", "naver"],
  "search_time_ms": 2340
}
```

---

## 配置说明

本工具开箱即用，**无需任何 API Key**。以下环境变量为可选配置：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `HTTP_PROXY` | _(无)_ | HTTP 代理 URL（如 `http://127.0.0.1:7890`） |
| `HTTPS_PROXY` | _(无)_ | HTTPS 代理 URL |
| `NO_PROXY` | _(无)_ | 逗号分隔的跳过代理的 hosts |
| `SMART_RESEARCH_TIMEOUT` | `30` | 单个 URL 抓取超时（秒） |
| `SMART_RESEARCH_USER_AGENT` | _(内置)_ | 自定义 User-Agent |
| `PLAYWRIGHT_HEADLESS` | `true` | 是否以无头模式运行 Playwright |

### 使用代理示例

```bash
export HTTPS_PROXY="http://127.0.0.1:7890"
python3 scripts/smart_research.py '{"action":"search","query":"测试"}'
```

---

## 降级链

抓取 URL 时，系统按以下顺序尝试各方法，直到某个成功为止：

| 优先级 | 方法 | 适用场景 | 优点 | 缺点 |
|--------|------|----------|------|------|
| 1 | **Playwright** | JavaScript 渲染页面 | 完整JS支持，还原度高 | 慢，依赖重 |
| 2 | **Jina Reader** | 清洁的 Markdown 提取 | 快速，提取质量高 | 依赖外部服务 |
| 3 | **DuckDuckGo HTML** | 通过代理快速获取 HTML | 适合被墙的站点 | JS支持有限 |
| 4 | **直接 requests** | 简单静态页面 | 最快，开销最小 | 容易被封 |
| 5 | **textise dot iitty** | 最终兜底方案 | 在其他方案都失败时可能成功 | 仅获取纯文本 |

---

## 隐私声明

- **不收集数据** — 本工具不收集、存储或传输任何个人数据。
- **无遥测上报** — 不含任何分析、崩溃报告或外部遥测功能。
- **本地执行** — 所有处理均在本地机器完成。
- **搜索查询** — 搜索词直接发送到您指定的搜索引擎，受其各自的隐私政策约束。
- **外部链接** — 抓取的网页内容受目标网站服务条款和隐私政策约束。

---

## 故障排除

### Q: 需要 API Key 吗？
A: 不需要。所有服务均为免费方案，无需任何 API Key。

### Q: 支持哪些网站？
A: 支持所有公开网页。微信文章、Cloudflare 防护站点、需登录站点可能需要特殊处理或无法正常工作。

### Q: 搜索结果为空怎么办？
A: 可能原因：
- 网络连接问题 — 检查您的网络
- 触发限流 — 稍后再试或设置代理
- 搜索引擎封禁了您的 IP — 尝试使用代理
- 搜索词太模糊 — 尝试更具体的关键词

### Q: Playwright 抓取出超时
A: Playwright 是最重的抓取方式，超时后系统会自动降级到更轻量的方法。您也可以手动增加超时时间：`{"action":"fetch","url":"...","timeout":60}`。

### Q: 如何使用代理？
A: 运行前设置 `HTTPS_PROXY` 环境变量：
```bash
export HTTPS_PROXY="http://127.0.0.1:7890"
python3 scripts/smart_research.py '{"action":"search","query":"测试"}'
```

### Q: 抓取的内容乱码 / 编码错误
A: 工具会尝试自动检测编码。如遇编码问题，请在 GitHub Issues 页面反馈。

### Q: 可以在 Python 脚本中调用吗？
A: 可以。导入并使用核心函数：
```python
import json
import sys
sys.path.insert(0, 'scripts')
from smart_research import run_smart_research

result = run_smart_research({"action": "search", "query": "你的搜索词"})
print(json.dumps(result, indent=2, ensure_ascii=False))
```

---

## 免责声明

**免责声明**：
本项目 99% 由 AI 自动生成，使用前请自行评估项目可行性。

---

## License

本项目采用 **MIT No Attribution License (MIT-0)** 授权 — 详见 [LICENSE](LICENSE) 文件。

```
MIT No Attribution

Copyright 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
```
