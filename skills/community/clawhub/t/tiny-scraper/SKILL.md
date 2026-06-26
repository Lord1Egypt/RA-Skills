---
name: TinyScraper
description: 简单静态网站镜像爬虫。给定 URL 下载整个域名下的 HTML、JS、CSS 和静态资源到本地，支持离线浏览。
---

# TinyScraper - 静态网站镜像工具

> 纯 Python3 标准库，无额外依赖

## 📁 目录结构

```
TinyScraper/
├── SKILL.md
├── bin/
│   └── tinyscraper       # CLI 入口
├── lib/
│   └── crawler.py        # 核心爬虫逻辑
├── conf/
│   └── .tinyscraper.conf # 配置文件
├── assets/

├── scripts/
│   └── test_crawler.py   # 自动化测试
└── references/
    └── SPEC.md           # 格式标准文档
```

## 🎯 Skill 职责

将目标网站完整镜像到本地，包括：
- HTML 页面（保持目录结构）
- JS、CSS、图片、字体等静态资源
- HTML/CSS 中的相对路径自动重写
- 外部链接保留原值，不处理

## 🔖 触发场景

- 用户要求"下载网站"、"镜像网站"、"离线保存网页"
- 用户提供 URL 并要求"爬取整个网站"
- 用户要求"抓取网站所有资源"

## 📋 执行步骤

### 1. 确认目标
- 检查 URL 是否为简单静态网站（SPA / JS 驱动类网站不适合）
- 使用 `--dry-run` 预览爬取范围

### 2. 启动爬取
```bash
tinyscraper "https://example.com"
```

### 3. 监控进度
- 实时显示：已爬页面数、资源数、待爬队列长度
- 失败 URL 记录到日志

### 4. 完成后
- 镜像保存于：`tmp/mirrors/{domain}/`
- 可用浏览器直接打开 `index.html` 离线浏览

## ⚙️ 命令详解

```bash
# 完整镜像
tinyscraper "https://example.com"

# 预览模式（只列出 URL，不下载）
tinyscraper "https://example.com" --dry-run

# 清理已下载的镜像
tinyscraper -d example.com

# 显示帮助
tinyscraper -h
```

## 📦 输出标准

### 目录结构
```
tmp/mirrors/{domain}/
├── index.html
├── page/
│   └── index.html
├── assets/
│   ├── style.css
│   └── script.js
├── images/
│   └── logo.png

```

### 路径规范
| URL | 本地路径 |
|-----|---------|
| `/` | `index.html` |
| `/about` | `about/index.html` |
| `/page?id=1` | `page/index.html` |
| `/style.css?v=1.2` | `style.css`（去重） |
| `/page#section` | `#` 锚点去除，视为同一文件 |

### 资源重写规则
- HTML 内所有同域 `href`/`src` → 相对路径
- CSS 内所有 `url()` → 相对路径
- 外部链接（其他域名）→ 保留原值不变
- `mailto:`/`tel:`/`javascript:` → 保留原值不处理



### 日志输出
```
[STEP] 🌐 开始镜像: https://example.com
[STEP] 📁 保存目录: tmp/mirrors/example.com
[INFO] 保存页面: https://example.com -> .../index.html
[INFO] 保存资源: https://example.com/style.css -> .../style.css
[STEP] 爬取 (1): https://example.com/about
[INFO] 进度: 已爬 3 页面, 12 资源, 5 待爬
...
[INFO] ==================================================
[INFO] 镜像完成!
[INFO]   页面: 15
[INFO]   资源: 48
[INFO]   失败: 2
[INFO]   目录: tmp/mirrors/example.com
```

## ⚠️ 局限性

- 仅支持简单静态网站（SPA/React/Vue 等 JS 驱动类不适用）
- 外部域名资源（如 CDN 上的 JS）不会下载

- 需目标网站允许爬取（robots.txt 规则被忽略）
