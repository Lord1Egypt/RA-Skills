---
name: scout-anti-crawl-v3
description: 六层Fetcher自动降级，一条命令搞定99%网站反爬，零成本起步
identifier: scout-anti-crawl
version: "3.0.0"
author: 小指
category: web-scraping
allowed-tools: Bash
---

# Scout Anti-Crawl v3

六层 Fetcher 自动降级，一条命令搞定 99% 网站的反爬机制。

## 为什么需要

AI Agent 会写代码、用工具，但一碰到反爬网站就歇菜。Cloudflare、验证码、JS渲染，随便哪个都能把 Agent 卡死。这个 Skill 让 Agent 一条命令突破这些障碍。

## 快速开始

```bash
# 抓取静态页
scout.py https://example.com

# 抓取并提取纯文本
scout.py https://example.com --text

# 搜狗微信搜索
scout.py --search "AI视频"

# 保存到文件
scout.py https://example.com --save output.html

# 指定从第几层开始（跳过前几层）
scout.py https://example.com --min-layer 5
```

## 五层 Fetcher 详解

### 第一层：Fetcher（快速 HTTP）

- **适用场景**：静态页面、API 接口、简单博客
- **性能**：毫秒级响应
- **反爬能力**：自动请求头伪装、Cloudflare 绕过、自适应延迟
- **工具**：Scrapling `Fetcher`

### 第二层：DynamicFetcher（浏览器渲染）

- **适用场景**：SPA 单页应用、JS 动态加载内容、React/Vue 页面
- **性能**：1-3 秒（含浏览器启动）
- **反爬能力**：完整 Playwright 浏览器渲染
- **工具**：Scrapling `DynamicFetcher`

### 第三层：StealthyFetcher（隐身模式）

- **适用场景**：Cloudflare 保护、强反爬网站
- **性能**：3-5 秒
- **反爬能力**：
  - Canvas / WebGL / Font 指纹伪装
  - navigator.webdriver 隐藏
  - Cloudflare Turnstile 绕过
  - 随机浏览器指纹 + UA 轮换
- **工具**：Scrapling `StealthyFetcher`

### 第四层：Obscura（Rust 隐身浏览器）

- **适用场景**：reCAPTCHA v3 高防护、Cloudflare Turnstile、强反爬网站、微信公众号
- **性能**：85ms 页面加载，9MB 内存占用
- **反爬能力**：
  - Rust 原生浏览器引擎 + V8 JS 运行时
  - 内置隐身模式（`--stealth`）：Canvas / WebGL / AudioContext 指纹随机化
  - navigator.webdriver 隐藏，creepjs 识别率 0%
  - TLS 握手模拟 Chrome 145 完整特征
  - 内置 SSRF 防护 + 3520+ 追踪器域名屏蔽
- **工具**：Obscura（`~/.local/bin/obscura`，v0.1.9，Apache-2.0）
- **依赖**：无（独立二进制，76MB）

### 第五层：Olostep API（住宅代理云端浏览器）

- **适用场景**：CloudFront WAF 拦截、大学官网、强防护网站
- **性能**：5-10 秒（云端渲染+住宅代理）
- **反爬能力**：
  - 住宅代理出口（不易被识别）
  - 云端浏览器渲染
  - CloudFront / Cloudflare / Akamai WAF 绕过
  - Geo-targeted 地区级爬取
- **工具**：Olostep API（免费额度）
- **API**：`POST /v1/scrapes`（旧端点 `/v1/request` 已废弃）
- **配置**：API Key 在 `scout.py` 的 `fetch_olostep()` 函数中

## 核心逻辑：自动降级

```
scout.fetch(url)
    ├─ ① Fetcher(快速 HTTP) → 成功？返回结果
    ├─ 失败？→ ② DynamicFetcher(浏览器渲染) → 成功？返回结果
    ├─ 失败？→ ③ StealthyFetcher(隐身伪装) → 成功？返回结果
    ├─ 失败？→ ④ Obscura(Rust隐身浏览器) → 成功？返回结果
    ├─ 失败？→ ⑤ Olostep API(住宅代理兜底) → 成功？返回结果
    └─ 失败？→ ⑥ Firecrawl(AI智能抓取) → 成功？返回结果
                                                  失败？返回错误
```

## Olostep 配置

```python
# 已在 scout.py 的 fetch_olostep() 中内置
OLOSTEP_API_KEY = "olostep_gGm6Y10wZgQpHKQsmqoaZaU24SHKkfPHMNef"

# API 参考
curl -s -X POST "https://api.olostep.com/v1/scrapes" \
  -H "Authorization: Bearer $OLOSTEP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url_to_scrape": "https://example.com",
    "formats": ["html"],
    "wait_before_scraping": 3000
  }'
```

### 单独使用 Olostep

```python
from scout import fetch_olostep

html = fetch_olostep("https://example.com")
```

## 微信搜索功能

```python
from scout import search_wechat

results = search_wechat("AI视频", max_results=8)
for r in results:
    print(r["title"], r["account"], r["link"])
```

## 依赖

- Python 3.9+
- scrapling>=0.4.8 (自动包含 Playwright)
- cloudscraper (Cloudflare 绕过)
- ddddocr (验证码识别)
- requests (Olostep API)
- **Obscura**（Rust 隐身浏览器，`~/.local/bin/obscura`，v0.1.9）
- Playwright + Chromium (浏览器引擎)
- Clash 代理集群（57 节点 + 自建首尔翻墙）

### 第六层：Firecrawl（AI智能抓取）

- **适用场景**：需要干净Markdown输出、结构化数据提取、AI Agent自动抓取
- **性能**：3-10秒（云端API）
- **反爬能力**：
  - 自动处理JS渲染、反爬机制
  - 输出干净Markdown/JSON，LLM-ready
  - 支持定义JSON Schema提取结构化数据
  - Agent模式：不用给URL，说目标自动搜索+抓取
- **工具**：Firecrawl CLI（`firecrawl`）
- **配置**：无需API Key，每月免费1000次
- **GitHub**：https://github.com/firecrawl/firecrawl (149k⭐)

## 相关资源

- 主脚本：`skills/scout-anti-crawl/scout.py`
- Olostep：https://olostep.com（免费 500次/月）
- Scrapling：https://github.com/D4Vinci/Scrapling (32.9k⭐)
- Firecrawl：https://github.com/firecrawl/firecrawl (149k⭐)
