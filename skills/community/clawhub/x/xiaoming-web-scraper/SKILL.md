---
name: web-scraper-pro
description: 网页数据爬虫 - 数据抓取、表格导出、定时采集
---

# Web Scraper Pro

网页数据抓取工具，支持定时采集和数据导出。

## 功能

- ✅ 网页数据抓取
- ✅ 表格导出 (CSV/Excel)
- ✅ 定时采集
- ✅ 图片下载
- ✅ API 调用

## 使用

```bash
# 抓取网页数据
clawhub scrape fetch --url https://example.com --selector ".product"

# 导出表格
clawhub scrape table --url https://example.com --format csv

# 定时采集
clawhub scrape schedule --url https://example.com --cron "0 */6 * * *"
```

## 定价

| 版本 | 价格 | 功能 |
|------|------|------|
| 免费版 | ¥0 | 100 页/月 |
| Pro 版 | ¥89 | 无限抓取 |
| 订阅版 | ¥25/月 | Pro+ 云存储 |
