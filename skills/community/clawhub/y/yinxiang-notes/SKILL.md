---
name: yinxiang-notes
description: 印象笔记（中国版）集成 skill。使用 Developer Token 在印象笔记中创建、整理和搜索笔记。支持笔记本列表、创建笔记、更新笔记内容/标签、移动笔记到废纸篓、查看/清空废纸篓、搜索内容、增量同步到 Obsidian vault。适用于使用 app.yinxiang.com 的用户。
---

# 印象笔记集成

## 快速开始

### 前置条件

1. **Developer Token**：从 https://app.yinxiang.com/api/DeveloperToken.action 获取
2. **Python 环境**：需要 Python 3.7+
3. **SDK 安装**：
   ```bash
   pip install evernote3 thrift html2text
   ```

### 配置

在 `.env` 文件中设置：
```
EVERNOTE_TOKEN=S=s16:U=xxx:E=xxx:C=xxx:P=xxx:A=en-devtoken:V=2:H=xxx
EVERNOTE_NOTESTORE_URL=https://app.yinxiang.com/shard/s16/notestore
```

## 核心功能

### 1. 获取笔记本列表

```bash
python skills/yinxiang-notes/scripts/list_notebooks.py
python skills/yinxiang-notes/scripts/list_notebooks.py --verbose  # 显示每个笔记本的笔记数量
```

### 2. 获取标签列表

```bash
python skills/yinxiang-notes/scripts/list_tags.py
```

### 3. 创建笔记

```bash
python skills/yinxiang-notes/scripts/create_note.py --title "标题" --content "<en-note>内容</en-note>"
# 指定笔记本
python skills/yinxiang-notes/scripts/create_note.py --title "标题" --content "<en-note>内容</en-note>" --notebook "笔记本名"
# 添加标签
python skills/yinxiang-notes/scripts/create_note.py --title "标题" --content "<en-note>内容</en-note>" --tags "标签1,标签2"
```

ENML 格式说明：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note>
    笔记内容...
    <en-todo checked="false">待办事项</en-todo>
</en-note>
```

### 4. 更新笔记

```bash
# 更新标题
python skills/yinxiang-notes/scripts/update_note.py --guid "笔记GUID" --title "新标题"
# 更新内容
python skills/yinxiang-notes/scripts/update_note.py --guid "笔记GUID" --content "<en-note>新内容</en-note>"
# 添加标签
python skills/yinxiang-notes/scripts/update_note.py --guid "笔记GUID" --add-tags "标签1,标签2"
# 移除标签
python skills/yinxiang-notes/scripts/update_note.py --guid "笔记GUID" --remove-tags "标签3"
# 组合操作
python skills/yinxiang-notes/scripts/update_note.py --guid "笔记GUID" --title "新标题" --add-tags "标签1"
```

### 5. 删除笔记（移至废纸篓）

```bash
# 预览（不实际删除）
python skills/yinxiang-notes/scripts/delete_note.py --guid "笔记GUID"
# 确认删除（移至废纸篓，可在客户端恢复）
python skills/yinxiang-notes/scripts/delete_note.py --guid "笔记GUID" --confirm
```

**删除行为说明**：
- `delete_note.py` 使用 `deleteNote` API，将笔记移至废纸篓，可在印象笔记客户端中恢复
- 清空废纸篓后笔记才永久删除（见下方"清空废纸篓"）

### 6. 搜索笔记

```bash
python skills/yinxiang-notes/scripts/search_notes.py "关键词"
python skills/yinxiang-notes/scripts/search_notes.py "标题:关键词"
python skills/yinxiang-notes/scripts/search_notes.py "any:关键词1 关键词2"
```

搜索语法：
- `关键词` — 在标题和正文中搜索
- `标题:关键词` — 仅搜索标题
- `创建时间:2024-01-01` — 按创建时间筛选
- `any:关键词1 关键词2` — 匹配任一关键词

### 7. 同步到 Obsidian（增量同步）

将印象笔记增量同步到本地 Obsidian vault，保持笔记本层级结构。

**目标 vault**：`C:\Users\adun\Documents\印象笔记同步`

```bash
# 同步全部笔记本
python skills/yinxiang-notes/scripts/sync_to_obsidian.py

# 只同步指定笔记本
python skills/yinxiang-notes/scripts/sync_to_obsidian.py --notebook "笔记本名"
python skills/yinxiang-notes/scripts/sync_to_obsidian.py -n "笔记本名"
```

**同步规则**：

| 笔记类型 | 判断条件 | 处理方式 |
|----------|----------|----------|
| 📎 附件笔记 | 资源有 fileName+扩展名 | enml_to_markdown + 附件 section |
| 🖼 内嵌图片笔记 | 有 en-media 但无 fileName | html2text 转 Markdown + 附件 section |
| 📝 纯文本笔记 | 无大量 HTML 标签和 en-media | 直接转为 Markdown |
| 📄 网页裁剪（短） | HTML ≥3个标签且 < 200KB | html2text 转为 Markdown |
| 🔗 网页裁剪（长） | HTML ≥3个标签且 ≥ 200KB 且纯 HTML（无用户手写内容） | 存 HTML 进 `_clips/` |

**附件存储**：每个笔记本有独立的附件和裁剪目录
```
印象笔记同步/
├── 笔记本A/
│   ├── 笔记.md
│   ├── _attachments/   ← 该笔记本附件（hash 去重）
│   └── _clips/         ← 该笔记本 HTML 裁剪（≥5KB）
├── 笔记本B/
│   ├── 笔记.md
│   ├── _attachments/
│   └── _clips/
└── .obsidian/
```

**同步后笔记的 frontmatter**：
```yaml
---
title: 笔记标题
created: 2026-03-19 10:30:00
updated: 2026-03-19 14:22:00
source: Evernote
source_guid: xxx-xxx-xxx
notebook: 笔记本名
type: webclip  # 仅网页裁剪（≥200KB）和内嵌图片笔记有此字段
---
```

**特性**：
- 增量同步：仅同步新增和变化的笔记
- 断点续传：遇到 API 频率限制自动保存进度
- 每次最多同步 50 条，避免触发限流
- 支持命令行参数控制同步行为（`--notebook` 指定笔记本）
- 使用 html2text 库进行 HTML 转 Markdown 转换

### 8. 查看废纸篓

```bash
python skills/yinxiang-notes/scripts/list_trash.py
```

### 9. 清空废纸篓（永久删除）

```bash
python skills/yinxiang-notes/scripts/empty_trash.py
```

⚠️ **警告**：此操作会永久删除废纸篓中的所有笔记，**无法恢复**！

## 完整脚本列表

| 脚本 | 功能 |
|------|------|
| `list_notebooks.py` | 获取笔记本列表（支持 --verbose 显示笔记数） |
| `list_tags.py` | 获取标签列表 |
| `create_note.py` | 创建笔记 |
| `update_note.py` | 更新笔记（标题/内容/标签） |
| `delete_note.py` | 删除笔记（移至废纸篓） |
| `search_notes.py` | 搜索笔记 |
| `sync_to_obsidian.py` | 增量同步印象笔记到 Obsidian vault |
| `list_trash.py` | 查看废纸篓中的笔记 |
| `empty_trash.py` | 清空废纸篓（永久删除） |

## API 端点

| 环境 | NoteStore URL |
|------|---------------|
| 生产环境 | https://app.yinxiang.com/shard/s16/notestore |
| 沙盒环境 | https://sandbox.yinxiang.com/shard/s1/notestore |

## 错误处理

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| EDAMUserException (errorCode=2) | Token 无效或过期 | 重新申请 Developer Token |
| EDAMNotFoundException | 资源不存在 | 检查笔记 GUID 或笔记本名 |
| EDAMSystemException (errorCode=19) | API 频率限制 | 等待限流窗口后重试，脚本会自动处理 |

## 注意事项

- Token 仅显示一次，请妥善保存
- **API 频率限制**：Evernote API 有每小时调用次数限制，同步脚本内置限流保护（每次获取笔记间隔 1 秒），避免触发限制
- **删除**：调用 `deleteNote` 移至废纸篓；调用 `expungeNote` 或清空废纸篓会永久删除
- **网页裁剪（≥200KB）**：Obsidian 中点击笔记内的嵌入链接查看原始 HTML，建议安装 HTML Reader 插件以获得更好渲染效果
