# yinxiang-notes

Evernote China (印象笔记) integration skill for OpenClaw.

印象笔记（中国版）集成 skill，用于 OpenClaw。

## Features / 功能

| Feature | 功能 |
|---------|------|
| **List Notebooks** | 获取笔记本列表（支持显示笔记数量） |
| **List Tags** | 查看所有标签 |
| **Create Notes** | 创建笔记（支持标题、内容 ENML、笔记本、标签） |
| **Update Notes** | 更新笔记（标题、内容、添加/移除标签） |
| **Delete Notes** | 删除笔记（移至废纸篓，可恢复） |
| **Search Notes** | 搜索笔记（关键词、标题、日期等） |
| **Sync to Obsidian** | 增量同步到本地 Obsidian vault |
| **Trash Management** | 查看和清空废纸篓 |

## Prerequisites / 前置条件

1. **Developer Token**: https://app.yinxiang.com/api/DeveloperToken.action
2. **Python 3.7+**
3. **SDK**: `pip install evernote3 thrift html2text`

## Configuration / 配置

Create a `.env` file:

创建 `.env` 文件：

```
EVERNOTE_TOKEN=S=s16:U=xxx:E=xxx:C=xxx:P=xxx:A=en-devtoken:V=2:H=xxx
EVERNOTE_NOTESTORE_URL=https://app.yinxiang.com/shard/s16/notestore
```

## Quick Start / 快速开始

```bash
# List notebooks / 列出笔记本
python scripts/list_notebooks.py

# Create a note / 创建笔记
python scripts/create_note.py --title "My Note" --content "<en-note>Content</en-note>"

# Search notes / 搜索笔记
python scripts/search_notes.py "keyword"

# Sync to Obsidian / 同步到 Obsidian
python scripts/sync_to_obsidian.py
```

## Scripts / 脚本列表

| Script | 描述 |
|--------|------|
| `list_notebooks.py` | 列出所有笔记本 |
| `list_tags.py` | 列出所有标签 |
| `create_note.py` | 创建新笔记 |
| `update_note.py` | 更新笔记（标题/内容/标签） |
| `delete_note.py` | 删除笔记（移至废纸篓） |
| `search_notes.py` | 搜索笔记 |
| `sync_to_obsidian.py` | 增量同步到 Obsidian vault |
| `list_trash.py` | 查看废纸篓 |
| `empty_trash.py` | 永久删除废纸篓 |

## Sync to Obsidian / 同步到 Obsidian

Syncs notes to your local vault.

将笔记同步到本地 Obsidian vault（默认路径 `C:\Users\adun\Documents\印象笔记同步`）。

**Note types handled / 支持的笔记类型**:
- Attachments (files with extension) / 附件（带扩展名的文件）
- Embedded images / 内嵌图片
- Plain text notes / 纯文本笔记
- Web clips (converted to Markdown or stored as HTML) / 网页裁剪（转为 Markdown 或存储 HTML）

**Frontmatter added / 添加的 frontmatter**:
```yaml
---
title: Note Title
created: 2026-03-19 10:30:00
updated: 2026-03-19 14:22:00
source: Evernote
source_guid: xxx-xxx-xxx
notebook: Notebook Name
---
```

## License / 许可证

MIT
