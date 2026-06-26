---
name: youdao-note
description: Use when the user wants to interact with YoudaoNote (有道云笔记) — listing, reading, creating, searching notes, clipping web pages, or saving Markdown/mindmap notes via the youdaonote CLI tool.
---

# YoudaoNote CLI

Command-line tool for 有道云笔记. Operate on notes without opening the app — list, read, create, search, clip, and save from the terminal or scripts.

## Setup

```sh
# Install (no Node.js required)
curl -fsSL https://artifact.lx.netease.com/download/youdaonote-cli/install.sh | bash

# Configure API Key (get from https://mopen.163.com/#/dashboard)
youdaonote config set apiKey YOUR_API_KEY

# Verify
youdaonote list
```

> API Key requires a phone number bound to your YoudaoNote account.

## Quick Reference

| Goal | Command |
|------|---------|
| List root directory | `youdaonote list` |
| List a folder | `youdaonote list -f <目录ID>` |
| Read a note | `youdaonote read <fileId>` |
| Create a note | `youdaonote create -n "标题" -c "内容"` |
| Create empty note | `youdaonote create -n "标题"` |
| Search notes | `youdaonote search 关键词` |
| Search (JSON output) | `youdaonote search "关键词" --json` |
| Recent 15 notes | `youdaonote recent` |
| Recent N notes | `youdaonote recent -l <N>` |
| Recent with content | `youdaonote recent -c` |
| Clip a webpage | `youdaonote clip "https://..."` |
| Clip to folder | `youdaonote clip "https://..." -f <目录ID>` |
| Save clip JSON | `youdaonote clip-save --file result.json` |
| Save note JSON | `youdaonote save --file note.json` |

## Save Formats

### clip-save JSON (HTML clipping from browser plugins)
```json
{
  "title": "笔记标题",
  "bodyHtml": "<p>正文内容</p>",
  "sourceUrl": "https://example.com",
  "images": []
}
```

### save JSON (Markdown, mindmap, etc.)
```json
{
  "title": "笔记.md",
  "type": "md",
  "content": "# 标题\n\n正文内容"
}
```

## Common Workflows

**Search and read in a script:**
```sh
FILE_ID=$(youdaonote search "关键词" --json | jq -r '.[0].id')
youdaonote read "$FILE_ID"
```

**Save a build report in CI:**
```sh
cat > note.json << 'EOF'
{ "title": "构建报告.md", "type": "md", "content": "# 构建成功\n\n时间：$(date)" }
EOF
youdaonote save --file note.json
```

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `API Key 未配置` | `youdaonote config set apiKey YOUR_KEY` |
| `clip-save` 报缺少必填字段 | JSON 需包含 `title`、`bodyHtml`、`sourceUrl` |
| `save` 报缺少必填字段 | JSON 需包含 `title`、`content` |
| `Unterminated string` JSON 解析失败 | 改用 `printf '%s\n' '...'` 或 `--file` 从文件读取 |
| Windows `JSON Parse error` | 使用 `--file` 读取文件；或改用 PowerShell |
| Windows `clip` 后出现命令错误 | URL 含 `&` 时必须用英文双引号括起整个 URL |
| Windows 保存后乱码 | 先执行 `chcp 65001`，或用 UTF-8 编辑器保存 JSON |
