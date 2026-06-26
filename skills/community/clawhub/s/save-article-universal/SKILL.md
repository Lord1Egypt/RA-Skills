---
name: save-article-universal
description: 通用微信公众号文章保存工具。支持多种笔记应用（Obsidian、Miaoyan、Notion 等），自动抓取文章、生成摘要、保存为 Markdown。
---

# Save Article Universal

通用微信公众号文章保存工具，自动抓取文章、生成摘要、保存到各种笔记应用。

## 功能

- 🔄 自动抓取微信文章内容
- 📝 智能生成要点摘要
- 💾 支持多种笔记应用（Obsidian、Miaoyan、Notion、本地文件夹）
- ⚙️ 完全可配置

## 支持的笔记应用

| 应用 | 说明 |
|------|------|
| 本地文件夹 | 保存到任意目录 |
| Obsidian | 保存到 Vault 目录 |
| Miaoyan | 保存到 iCloud 笔记 |
| Notion | 同步到 Notion 数据库 |

## 使用方式

### 命令行

```bash
python3 save_article.py "https://mp.weixin.qq.com/s/xxx"
python3 save_article.py "链接" --output "/path/to/folder"
python3 save_article.py "链接" --method obsidian
```

### 配置文件

复制 `config.json.example` 为 `config.json` 并修改配置。

## 依赖

- Python 3.7+
- curl

安装依赖：`pip install requests`（可选，用于 Notion）
