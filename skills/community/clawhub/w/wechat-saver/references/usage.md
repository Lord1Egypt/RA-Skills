# WeChat Saver 使用指南

## 快速开始

### 1. 安装依赖

```bash
pip install requests readability-lxml beautifulsoup4 lxml
```

### 2. 测试运行

```bash
# 查看帮助
~/.claude/skills/wechat-saver/scripts/wechat_to_md.py --help

# 测试一篇公开文章
~/.claude/skills/wechat-saver/scripts/wechat_to_md.py \
  https://mp.weixin.qq.com/s/xxx
```

## 输出说明

### 目录结构
```
~/Documents/Obsidian Vault/00-Inbox/
├── 文章标题/
│   ├── images/           # 图片目录
│   │   ├── image_001.jpg
│   │   └── image_002.png
│   └── 文章标题.md       # Markdown 文件
```

### Markdown 格式
```markdown
---
title: 文章标题
source: https://mp.weixin.qq.com/s/xxx
created: 2026-04-05 12:00:00
tags: [wechat, article]
---

正文内容...

---
📌 原文链接：https://mp.weixin.qq.com/s/xxx
📅 抓取时间：2026-04-05 12:00:00
```

## 常见问题

### 依赖安装失败
```bash
# 使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple \
  requests readability-lxml beautifulsoup4 lxml
```

### 图片下载失败
微信有防盗链，部分图片可能无法下载。脚本会自动跳过失败图片，不影响文章保存。

### 输出目录有空格
```bash
# 使用引号或转义
~/.claude/skills/wechat-saver/scripts/wechat_to_md.py \
  -o "~/Documents/Obsidian Vault/00-Inbox" \
  <url>
```
