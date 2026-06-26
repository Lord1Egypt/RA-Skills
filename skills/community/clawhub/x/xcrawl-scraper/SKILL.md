---
name: XCrawl Scraper
description: XCrawl - AI-Powered Web Scraping API / AI 驱动网页爬虫，支持结构化数据提取
homepage: https://github.com/zhangss110/xcrawl-scraper
metadata: {"openclaw":{"emoji":"🕷️","requires":{"bins":["python","pip"],"env":[]}}}
tags: latest=1.0.0,scraper=1.0.0,web-scraping=1.0.0,ai=1.0.0,json=1.0.0,markdown=1.0.0
---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge License-MIT-yellow?style=for-the-badge" alt="License">
</p>

<h1 align="center">🕷️ XCrawl Scraper / XCrawl 网页爬虫</h1>

<p align="center">
  <strong>AI-Powered Web Scraping API - 结构化数据提取利器</strong><br>
  <em>支持 Markdown、HTML、JSON、Screenshot 等多种格式输出</em>
</p>

---

## ✨ 功能特点 / Features

| 功能 | 说明 |
|------|------|
| 🏷️ **网页爬取** | 支持 Markdown、HTML、JSON、Screenshot |
| 🔍 **搜索** | 搜索引擎结果爬取 |
| 🗺️ **网站地图** | 自动发现站点所有页面 |
| 🕷️ **站点爬取** | 批量爬取整个站点 |
| 📊 **结构化数据** | JSON Schema 自动提取结构化数据 |
| 🌐 **代理支持** | 全球代理可选 |

---

## 📦 安装 / Installation

### 方式一：运行安装脚本

```bash
scripts\install.bat
```

### 方式二：手动安装

```bash
# 1. 安装依赖
pip install xcrawl

# 2. 配置 API Key
python scripts\xcrawl_scraper.py set-key YOUR_API_KEY
```

---

## ⚙️ 获取 API Key

1. 访问 https://xcrawl.com 注册账号
2. 获取 API Key
3. 配置:

```bash
python scripts\xcrawl_scraper.py set-key YOUR_API_KEY
```

---

## 📖 使用方法 / Usage

### 1. 爬取网页 (基本)

```bash
python scripts\xcrawl_scraper.py scrape https://example.com markdown
```

### 2. 爬取多个格式

```bash
python scripts\xcrawl_scraper.py scrape https://example.com markdown html links
```

### 3. 结构化数据提取 (JSON)

```bash
python scripts\xcrawl_scraper.py scrape https://example.com json "提取产品名称和价格"
```

### 4. 搜索

```bash
python scripts\xcrawl_scraper.py search "web scraping"
```

### 5. 网站地图

```bash
python scripts\xcrawl_scraper.py map https://example.com
```

### 6. 站点爬取

```bash
python scripts\xcrawl_scraper.py crawl https://example.com
```

---

## 📋 命令列表

| 命令 | 说明 |
|------|------|
| `scrape <URL> [formats...]` | 爬取网页 |
| `search <query>` | 搜索 |
| `map <URL>` | 网站地图 |
| `crawl <URL>` | 站点爬取 |
| `set-key <API_KEY>` | 设置 API Key |
| `config` | 显示配置 |

---

## 🔧 配置 / Configuration

配置文件: `scripts/config.json`

```json
{
  "apiKey": "YOUR_API_KEY",
  "apiUrl": "https://run.xcrawl.com",
  "timeout": 60,
  "defaultFormats": ["markdown"],
  "defaultProxy": ""
}
```

---

## 📝 示例输出

### Markdown 输出

```markdown
# Example Domain

This domain is for use in illustrative examples in documents.
```

### JSON 输出

```json
{
  "product_name": "iPhone 15 Pro",
  "price": 999,
  "currency": "USD"
}
```

---

## 📦 依赖

- Python >= 3.8
- xcrawl SDK

---

## 🤝 贡献 / Contributing

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

<p align="center">🕷️ Powered by XCrawl</p>
