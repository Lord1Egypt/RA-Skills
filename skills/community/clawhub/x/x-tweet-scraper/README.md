# X.com 全量推文采集技能 / X.com Comprehensive Tweet Scraper

**Tags**: `#twitter-scraper` `#x-tweet-collector` `#playwright-automation` `#web-scraping` `#data-collection` `#social-media-analytics` `#x-api-scraping` `#browser-automation` `#tweet-archive` `#python-scraper`

---

## 中文说明

### 简介
通过 Playwright 浏览器自动化，三种方案采集 X.com（Twitter）用户的公开推文历史。全部使用真实浏览器环境，绕过反爬限制。

### 方案
| 方案 | 覆盖量 | 限流 | 适用场景 |
|------|--------|------|---------|
| 自动搜索（推荐） | ~2000+ | 低 | 全量采集 |
| GraphQL API | ~900 | 高 | 快速获取最新 |
| DOM 滚动 | ~1400 | 最低 | Profile 翻页 |

### 前置条件
- Python 3.10+, `pip install playwright`, `python -m playwright install chromium`
- Windows 需设置 `$env:PYTHONIOENCODING="utf-8"`
- 从浏览器导出 X.com 登录 Cookie

### 使用
```powershell
# 自动搜索（推荐）
python -u scripts/scrape_x_auto.py --username 目标用户 --seed 已有数据.json

# GraphQL API
python -u scripts/scrape_x_v9.py --username 目标用户 --batch --pages 50

# DOM 滚动
python -u scripts/scrape_x_scroll.py --username 目标用户 --seed 已有数据.json
```

详细文档请参阅 `SKILL.md` 和 `references/workflow.md`。

---

## English Description

### Overview
Three Playwright-based strategies for scraping public tweet history from X.com (Twitter) users. All use real browser environments to bypass anti-scraping protections.

### Strategies
| Strategy | Coverage | Rate Limit | Use Case |
|----------|----------|-----------|----------|
| Auto-Search (Recommended) | ~2000+ | Low | Full collection |
| GraphQL API | ~900 | High | Fast latest fetch |
| DOM Scroll | ~1400 | Lowest | Profile scrolling |

### Prerequisites
- Python 3.10+, `pip install playwright`, `python -m playwright install chromium`
- Windows: `$env:PYTHONIOENCODING="utf-8"`
- Export X.com login cookies from browser

### Usage
```powershell
# Auto-Search (Recommended)
python -u scripts/scrape_x_auto.py --username target_user --seed existing_data.json

# GraphQL API
python -u scripts/scrape_x_v9.py --username target_user --batch --pages 50

# DOM Scroll
python -u scripts/scrape_x_scroll.py --username target_user --seed existing_data.json
```

See `SKILL.md` and `references/workflow.md` for full documentation.
