---
name: scrapling-safe
description: |
  Scrapling 安全技能 - 网页数据抓取工具
  支持 HTTP 请求、隐身抓取、浏览器自动化
  智能元素定位，抗反爬虫检测
  无需 API 配置，路径输出受限
---

# Scrapling 技能

使用 Scrapling 框架进行安全的网页数据抓取和内容提取。

## 安全说明

**仅用于合法用途**，严格遵守以下限制：

- ✅ **仅抓取公开网站**：遵守 robots.txt 和网站服务条款
- ✅ **路径输出受限**：结果文件只能保存到用户主目录
- ✅ **无危险函数**：不使用 eval/exec 等危险函数
- ✅ **严格的超时控制**：防止无限等待
- ✅ **频率限制**：自动添加请求延迟，避免对目标造成压力
- ❌ **禁止抓取私有内容**：仅抓取公开可访问页面
- ❌ **禁止大规模爬取**：默认并发限制为 1

## 核心功能

- 🕷️ **多种抓取模式**：HTTP/隐身/浏览器自动化
- 🎯 **智能元素定位**：自适应选择器，网站改版后仍有效
- 📄 **数据提取**：CSS/XPath/文本/正则搜索
- 💾 **结果保存**：保存到 JSON/TXT/MD 文件（路径受限）
- 🔍 **内容解析**：类似 Scrapy 的 API，易于使用

## 使用场景

- 抓取公开新闻和资讯
- 提取商品信息（电商网站）
- 收集公开数据（天气、股票等）
- 网站内容监控

## 触发词

- "scrapling 抓取..."
- "scrapling 提取..."
- "scrapling 爬取..."
- "scrapling 获取..."

## 快速开始

### 基本抓取

```bash
# HTTP 请求抓取
scrapling get 'https://example.com' --output ~/result.json

# 隐身模式抓取
scrapling stealthy 'https://example.com' --output ~/result.json

# 浏览器自动化（动态内容）
scrapling dynamic 'https://example.com' --output ~/result.json
```

### 指定选择器

```bash
# 使用 CSS 选择器
scrapling get 'https://quotes.toscrape.com' --css-selector '.quote' --output ~/quotes.json

# 提取特定字段
scrapling get 'https://quotes.toscrape.com' --css-selector '.quote .text' --output ~/text.txt
```

### 高级用法

```bash
# 隐身模式 + 解决 Cloudflare
scrapling stealthy 'https://nopecha.com/demo/cloudflare' --solve-cloudflare --output ~/result.json

# 并发抓取（限制为 1）
scrapling spider 'https://example.com' --concurrent 1 --output ~/crawl.json
```

## 安装要求

- Python 3.10+
- 需要安装 Scrapling: `pip install scrapling[fetchers]`
- 需要浏览器依赖：`scrapling install`

## 注意事项

- 需要本地安装 Scrapling 和相关依赖
- 默认请求延迟 1 秒，避免对目标造成压力
- 仅抓取公开可访问的页面
- 遵守 robots.txt 和网站服务条款
- 输出文件路径必须在用户主目录

## 版本历史

- **1.0.0** - 初始版本
