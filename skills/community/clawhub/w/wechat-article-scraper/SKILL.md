---
name: wechat-article-scraper
description: 在搜狗微信搜索指定关键词，抓取相关文章（标题、摘要、发布日期、来源公众号），生成PDF报告。触发场景：用户要求"搜索微信文章 关键字 数量"
---

# 微信公众号文章抓取

## 功能概述

通过搜狗微信搜索指定关键词，抓取最新文章，生成带本地PDF的行业报告。

## 触发方式

用户说：
- "搜索微信文章 脑机接口"
- "搜索微信文章 人工智能 5"
- "搜索微信文章 光伏 10"

---

## 完整工作流程

### 第1步：搜索文章

```bash
cd ~/.openclaw/workspace
python3 ~/.openclaw/workspace/skills/wechat-article-scraper/scripts/wechat_search.py <关键词> [数量]
```

- 输出：`articles.json`
- 包含字段：title, text, url, date, source
- 默认搜索90天内文章

---

### 第2步：生成摘要（聊天窗口）

⚠️ **重要：summary必须在聊天窗口用当前会话模型生成！**

1. 读取 `articles.json` 中的文章
2. 用当前模型逐篇生成100-200字摘要
3. 写入 `articles_new.json`（包含title, text, url, date, source, summary字段）

---

### 第3步：抓取原文PDF

```bash
cd ~/.openclaw/workspace
python3 ~/.openclaw/workspace/skills/wechat-article-scraper/scripts/wechat_fetch.py <关键词>
```

- 输出：`wechat_pages/` 目录下的PDF文件
- 每篇文章保存为独立的PDF，保留完整样式

---

### 第4步：生成行业报告

```bash
cd ~/.openclaw/workspace
python3 ~/.openclaw/workspace/skills/wechat-article-scraper/scripts/wechat_pdf.py <关键词>
```

- 输出：`<关键词>_行业动态.pdf`

报告包含：
- 标题、日期
- 行业动态精选（每篇文章）：
  - 文章标题
  - 来源公众号 | 发布日期
  - 摘要（LLM生成，100-200字）
  - 链接1：**微信原文（有时效限制）** → 原始微信文章链接
  - 链接2：**点我看原文(PDF)** → 本地PDF文件

---

## 脚本说明

### scripts/wechat_search.py

- 输入：关键词、数量（默认10）
- 输出：`articles.json`
- 功能：使用 Playwright 访问搜狗微信搜索，解析搜索结果并抓取文章正文

### scripts/wechat_fetch.py

- 输入：关键词
- 输出：`wechat_pages/*.pdf`
- 功能：读取 `articles_new.json`，抓取每篇文章原文保存为PDF

### scripts/wechat_pdf.py

- 输入：关键词
- 输出：`<关键词>_行业动态.pdf`
- 功能：读取 `articles_new.json`，生成带双链接的行业报告PDF

---

## 依赖

```bash
# 安装 Python 依赖
pip install playwright requests

# 安装 Playwright 浏览器
playwright install chromium
```

---

## 注意事项

1. **摘要必须用LLM生成** - 不能在pdf.py中自动生成
2. **链接格式** - 微信原文（有时效限制）+ 点我看原文(PDF)
3. **日期过滤** - 目前默认搜索90天内文章，暂无14天过滤选项
