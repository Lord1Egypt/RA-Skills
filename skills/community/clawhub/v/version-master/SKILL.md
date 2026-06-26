---
name: version-master
version: "2.1.1"
description: "Intelligent single-file version management. Save, restore, diff, and clean file snapshots with per-file version history. Activate when users need version control, file snapshot management, or project state recovery."

keywords: ["version snapshot", "version control", "snapshot save", "version restore", "version diff", "快照保存", "版本管理", "版本恢复", "版本对比"]
---

# Version-Master 2.1.0

## Purpose

Version-Master 2.1.0 is a **single-file level** version management skill. Unlike full-workspace snapshots, it maintains **independent version history for each file**, so users can clearly see what changes each document has gone through.

## Core Features

1. **Single-file versioning** - Each file maintains its own version history independently
2. **Complete content saving** - Saves actual file content (text and binary), supports full restoration
3. **Smart summaries** - Automatically extracts descriptive summaries from file content (e.g., document titles)
4. **Content deduplication** - Automatically skips unchanged files to avoid meaningless versions
5. **Safe restoration** - Auto-backs up current file before restoring, supports rollback
6. **Version diff** - Compare differences between versions of the same file

## When to Use

Activate this skill when the user's request involves any of these scenarios:

1. **Save file version** / 保存文件版本 - User says "save this file's version", "save current changes"
2. **View version history** / 查看版本历史 - User says "what versions does this file have", "show version history"
3. **Restore old version** / 恢复旧版本 - User says "restore to v2", "go back to previous version"
4. **Diff versions** / 对比版本差异 - User says "compare v1 and v2", "show me what changed"
5. **Clean versions** / 清理版本 - User says "delete old versions"

## How to Use

After loading this skill, the AI uses version management features by calling `scripts/version_tool.py`.

### Core Features

#### 1. Save Version

```python
# Save a specific file
save_version(file_path="ai_news_20260324.md", message="Added 11th news item")
```

**Key Parameters:**
- `file_path`: File path (relative to workspace). Optional, but AI should auto-detect from context.
- `message`: Version description. AI should auto-generate meaningful descriptions based on user actions.

**AI Auto-Detection Rules / AI 自动判断规则:**
- User explicitly specifies a filename → Save that file / 用户明确指定文件名 → 保存该文件
- User says "save it" and context shows a recently edited/generated file → AI auto-fills the file path / 用户说"保存一下"且上下文中有刚编辑/生成的文件 → AI 自动填入该文件路径
- Cannot determine → Ask the user which file to save / 无法判断 → 向用户询问要保存哪个文件
- **NEVER** call without file_path expecting batch save / **禁止**不带 file_path 直接调用并期望批量保存

#### 2. List Versions

```python
# List all files with version history
list_versions()

# List version history of a specific file
list_versions(file_path="ai_news_20260324.md")
```

**Output Example:**
```
ai_news_20260324.md (3 versions)
  v3 - Added 11th news item | 2026-03-25 08:08
  v2 - Added 6 tech news items | 2026-03-25 08:05
  v1 - Initial version, 10 AI news items | 2026-03-25 08:03

interesting_news.md (1 version)
  v1 - Tech, sports, military highlights | 2026-03-25 08:10
```

#### 3. Restore Version (requires user confirmation / 需要用户确认)

```python
# Restore to a specific version
restore_version(file_path="ai_news_20260324.md", version=2, confirm=True)

# Restore to the latest version
restore_version(file_path="ai_news_20260324.md", confirm=True)
```

**Restoration Features:**
- Auto-backs up current file to `.version_backup/`
- Fully restores file content (text and binary)

#### 4. Diff Versions

```python
# Compare two versions of the same file
diff_versions(file_path="ai_news_20260324.md", version1=1, version2=3)

# Compare current file with a historical version
diff_versions(file_path="ai_news_20260324.md", version2=2)
```

#### 5. Clean Versions

```python
# Delete all versions of a file
clean_versions(file_path="test.txt", confirm=True)

# Delete a specific version of a file
clean_versions(file_path="test.txt", version=1, confirm=True)
```

### Safety Rules / 安全规则

The following operations require explicit user confirmation:

1. **Version restore** / 版本恢复 - Will overwrite current file content
2. **Version delete** / 版本删除 - Permanently deletes snapshot data

Before calling these operations, the AI must:
1. Show operation details and risks / 显示操作详情和风险
2. Wait for explicit user confirmation / 等待用户明确确认
3. Set `confirm=True` parameter / 设置 `confirm=True` 参数

**Path Security / 路径安全：**
All `file_path` parameters are validated server-side to stay within the workspace boundary. Paths containing `../` or absolute paths outside the workspace are rejected with an error. The AI must **never** pass system-level paths (e.g., `../../etc/passwd`, `C:\Windows\...`) as `file_path`.

## Technical Implementation

### Storage Architecture

```
~/.workbuddy/versions/version-master/
├── index.json                                    # Global index (file → version mapping)
├── 20260325084235_ai_news_20260324-md/           # One directory per file (prefixed with workspace ID)
│   ├── v1.json                                  # Version 1 (text content embedded in JSON)
│   ├── v1.md                                    # Version 1 binary reference file (if any)
│   ├── v2.json                                  # Version 2
│   └── v3.json                                  # Version 3
└── 20260325084235_interesting_news-md/
    └── v1.json
```

**Design Notes:**
- All workspaces share the same storage directory, version snapshots are accessible across workspaces
- Directory names are prefixed with workspace directory name (e.g., `20260325084235`) for readability and disambiguation
- `.` in filenames is replaced with `-`, path separators replaced with `_` to ensure unique keys
- **Text files**: Content embedded directly in JSON
- **Binary files**: Copied to version directory (e.g., `v1.png`), JSON stores only a file reference (no base64)
- `index.json` can be auto-rebuilt from disk `v*.json` files if corrupted or lost

**Global Index Structure (index.json):**
```json
{
  "files": {
    "20260325084235_ai_news_20260324-md": {
      "rel_path": "ai_news_20260324.md",
      "next_version": 4,
      "versions": [
        {
          "version": 1,
          "timestamp": "2026-03-25T08:03:00",
          "content_hash": "abc123...",
          "file_size": 2928,
          "summary": "Initial version, 10 AI news items",
          "version_file": "20260325084235_ai_news_20260324-md/v1.json"
        }
      ]
    }
  }
}
```

### Version File Structure (v1.json)
```json
{
  "version": 1,
  "timestamp": "2026-03-25T08:03:00",
  "content_hash": "abc123...",
  "file_size": 2928,
  "summary": "Initial version, 10 AI news items",
  "message": "Initial version",
  "content": {
    "type": "text",
    "content": "# AI News Briefing\n\n..."
  }
}
```

### File Structure
```
version-master/
├── SKILL.md              # Skill documentation
├── requirements.txt      # Dependencies
└── scripts/
    ├── __init__.py
    └── version_tool.py   # Core implementation
```

## AI Usage Guide

### Key Principles

1. **Smart file_path detection** / 智能判断 file_path - AI should auto-detect which file to save based on context. When user says "save it", save the file just edited/generated; when user specifies a filename, save that file; when uncertain, ask the user.
2. **Auto-generate message** / 自动生成 message - AI should auto-generate meaningful version descriptions (e.g., "Added section 3", "Fixed typo").
3. **List before save** / 先 list 后 save - Check existing version history before saving to avoid duplicating identical content.
4. **Clear version display** / 清晰展示版本关系 - Display versions grouped by file with clear version numbers and change descriptions.

### Example Workflow

```
User: "帮我把 ai_news.md 保存一下" / "Save ai_news.md for me"
AI:
  1. Call list_versions(file_path="ai_news.md") to check existing versions
  2. Analyze current file content changes
  3. Call save_version(file_path="ai_news.md", message="Added 3 new news items")
  4. Show result: "ai_news.md saved as v3"

User: "恢复到上一个版本" / "Restore to previous version"
AI:
  1. Check version history, confirm current is v3, previous is v2
  2. Prompt user: "About to restore ai_news.md to v2 (Added 3 news items → Initial version). Confirm?"
  3. After user confirms, call restore_version(file_path="ai_news.md", version=2, confirm=True)
```
