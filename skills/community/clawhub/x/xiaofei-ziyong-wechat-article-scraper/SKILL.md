---
name: WeChat Article Scraper
description: 微信公众号文章抓取工具。从 mp.weixin.qq.com 抓取公开文章（文字+图片+视频），解析内容块顺序，下载图片，按原顺序写入飞书知识库。
identifier: wechat-article-scraper
version: 2.0.0
emoji: 📱
author: xiao
tags: [wechat, china, scraping, article, feishu]
requires:
  bins:
    - python3
    - google-chrome
  env: []
primaryEnv: null
---

# WeChat Article Scraper v2.0

微信公众号文章抓取 + 飞书导入工具。

## 工作流程

```
1. Chrome headless 抓取完整 HTML（绕过微信反爬检测）
2. 解析 HTML，提取有序内容块（文字/图片/GIF视频）
3. 下载所有文章图片到本地
4. 创建飞书知识库文档
5. 写入文字内容
6. 插入所有图片（仅支持末尾追加，这是飞书 API 限制）
7. 用户在飞书编辑器中手动拖动图片到正确位置
```

## 核心脚本

### scrape.py — 纯抓取（不写飞书）
```bash
python3 ~/.openclaw/skills/wechat-article-scraper/scripts/scrape.py <文章链接>
```
输出 JSON：title / author / content / word_count / url

### scrape_and_import.py — 完整流程
```bash
python3 ~/.openclaw/skills/wechat-article-scraper/scripts/scrape_and_import.py <文章链接> [--cache-dir /path] [--dry-run]
```
- `--dry-run`：仅解析内容，不写飞书
- 自动下载图片到缓存目录
- 输出内容块结构和摘要

## 内容块解析逻辑

1. 定位 `id="js_content"` 区域
2. 用正则提取所有 `data-src` 图片（保持文章顺序）
3. 每两张图片之间的 HTML 片段 → 清洗成纯文字
4. GIF 图片识别为视频预览（不下载）
5. 跳过底部干扰内容（赞赏/留言/推荐阅读）

## 飞书写入流程（必须按此顺序）

```
feishu_create_doc          → 创建空白文档
feishu_update_doc(mode=overwrite)  → 写入所有文字内容
feishu_doc_media(insert)  → 逐一插入所有图片（末尾追加）
```

## ⚠️ 关键限制

**图片只能追加到文档末尾，无法插入中间位置。**

原因：飞书 `doc_media/insert` API 不支持 `block_id` / `position` 参数，只能在文档末尾追加图片 block。

解决方案：
1. 先写完所有文字（图片占位符用括号注明位置，如"[图1：xxx]"）
2. 再统一 insert 所有图片到末尾
3. 用户打开飞书文档，**手动拖动图片**到对应文字旁边

这是**飞书官方 API 限制**，非工具实现问题。

## 图片顺序对应（文章块结构）

脚本会输出每个内容块的类型和预览文字，对应关系如下：

| 块序号 | 类型 | 说明 |
|--------|------|------|
| N | text | 纯文字段落 |
| N | image | 文章图片（img_XXX.png） |
| N | video | GIF动态图=视频预览（不下载） |

插入图片时按 `img_001.png` ~ `img_NNN.png` 文件名顺序对应文章中的图片顺序。

## 环境要求

- `google-chrome` 已安装在 `/usr/bin/google-chrome`
- 反检测参数绕过微信 UA 检测：
  - `--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."`
  - `--disable-blink-features=AutomationControlled"`
  - `--virtual-time-budget=20000`（等待 JS 完全渲染）
