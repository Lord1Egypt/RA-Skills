---
name: yuque
description: >
  语雀 (Yuque) 知识库管理。搜索、阅读、创建、编辑语雀文档，管理知识库和目录。
  Use when: user mentions 语雀/Yuque, or wants to search/read/create/edit documents,
  manage knowledge bases, organize notes on Yuque, upload articles to Yuque.
---

This skill enables AI agents to interact with Yuque (语雀) — a Chinese knowledge management platform — through its OpenAPI. It works across Claude Code, opencode, openclaw, and any agent with shell access.

## Quick Start

Install this skill, then tell your AI agent:

> 帮我配置语雀 API，我的 token 是 xxxxxxxx

The agent will automatically create `config.json` and verify connectivity.

### How to get your API Token

1. Login to [Yuque](https://www.yuque.com)
2. Click Avatar → Settings (设置) → Developer (开发者) → Personal Access Token (个人访问令牌)
3. Create a new token, copy it

## Setup Details

Authentication requires a Yuque API token. The scripts look for it in this order:

1. **config.json** (preferred): Create `config.json` in this skill's root directory:
   ```json
   {
     "api_token": "your-yuque-api-token",
     "base_url": "https://www.yuque.com"
   }
   ```
   See `config.example.json` for the template.

2. **Environment variable** (fallback): `export YUQUE_TOKEN="your-token"`

When the user provides their API token, create `config.json` by copying `config.example.json` and filling in the token, then run `python scripts/get_user.py` to verify. If verification succeeds, show the user's name to confirm.

Verify setup: `python scripts/get_user.py`

## Scripts

All scripts are in the `scripts/` directory. They use only Python standard library (zero dependencies). Output is JSON to stdout, errors go to stderr.

### Search & Read (RAG)

| Script | Usage | Description |
|--------|-------|-------------|
| `search.py` | `python scripts/search.py "keyword"` | Search docs or repos |
| `get_doc.py` | `python scripts/get_doc.py --repo REPO --doc DOC` | Get full document content |
| `list_docs.py` | `python scripts/list_docs.py --repo REPO` | List all docs in a repo |
| `doc_versions.py` | `python scripts/doc_versions.py --doc DOC` | Document version history |

### Create & Edit

| Script | Usage | Description |
|--------|-------|-------------|
| `create_doc.py` | `python scripts/create_doc.py --repo REPO --title "Title" --body-file file.md` | Create a document |
| `update_doc.py` | `python scripts/update_doc.py --repo REPO --doc DOC --body-file file.md` | Update a document |
| `delete_doc.py` | `python scripts/delete_doc.py --repo REPO --doc DOC` | Delete a document |

### Knowledge Base

| Script | Usage | Description |
|--------|-------|-------------|
| `list_repos.py` | `python scripts/list_repos.py` | List user's repos |
| `create_repo.py` | `python scripts/create_repo.py --name "Name" --slug slug` | Create a new repo |

### Table of Contents

| Script | Usage | Description |
|--------|-------|-------------|
| `get_toc.py` | `python scripts/get_toc.py --repo REPO` | Get repo TOC tree |
| `update_toc.py` | `python scripts/update_toc.py --repo REPO --action appendNode ...` | Update TOC structure |

### User

| Script | Usage | Description |
|--------|-------|-------------|
| `get_user.py` | `python scripts/get_user.py` | Get current user info |

## Workflows

### Search & Read (RAG)

When the user asks to find or read content from Yuque:

1. Search: `python scripts/search.py "keyword"` — returns titles, IDs, and summaries
2. Present the search results to the user as a numbered list
3. Once the user selects a document, fetch the full content:
   `python scripts/get_doc.py --repo REPO_ID --doc DOC_ID`
4. The response `data.body` field contains the markdown content. If `body` is empty, use `body_html` or `body_lake` as fallback.

### Write & Upload

When the user asks to write content and upload it to Yuque (e.g., "write a dev doc and upload to Yuque"):

1. Write the content locally as a markdown file (e.g., `/tmp/yuque_doc.md`)
2. Find the target repo: `python scripts/list_repos.py` — ask the user which repo to use
3. Upload: `python scripts/create_doc.py --repo REPO_ID --title "Title" --body-file /tmp/yuque_doc.md`
4. The response includes the document URL in `data.slug` — combine with repo namespace to form the full URL

### Edit Existing Document

When the user asks to update an existing Yuque document:

1. Find the doc: `python scripts/search.py "doc title"` or `python scripts/list_docs.py --repo REPO_ID`
2. Read current content: `python scripts/get_doc.py --repo REPO_ID --doc DOC_ID`
3. Modify the content locally
4. Update: `python scripts/update_doc.py --repo REPO_ID --doc DOC_ID --body-file /tmp/updated.md`

### Organize Notes

When the user asks to organize or restructure their knowledge base:

1. View current structure: `python scripts/get_toc.py --repo REPO_ID`
2. Plan the reorganization based on user instructions
3. Apply changes: `python scripts/update_toc.py --repo REPO_ID --action appendNode --action-mode child --doc-ids DOC_ID`
4. Use `--action removeNode` to remove nodes, `--action editNode` to rename

## Script Details

### Body input for create/update

Documents support three ways to provide body content:
- `--body "inline content"` — for short content
- `--body-file /path/to/file.md` — for files (recommended for long content)
- Pipe via stdin: `echo "content" | python scripts/create_doc.py ...`

### Pagination

List endpoints support `--offset` and `--limit` parameters. Default limit is 100.

### Repository identifiers

The `--repo` parameter accepts either:
- Numeric ID: `--repo 12345`
- Namespace path: `--repo group_login/book_slug` (more readable)

### Document format

Default format is `markdown`. All scripts default to creating/updating in markdown format. Use `--format html` or `--format lake` if needed.

## User Intent Mapping

| User says | Action |
|-----------|--------|
| "搜索/查找语雀上关于 X 的文档" | `search.py "X"` → `get_doc.py` |
| "读取/打开这篇语雀文档" | `get_doc.py --repo R --doc D` |
| "写一篇文档上传到语雀" | Write locally → `list_repos.py` → `create_doc.py` |
| "更新/修改语雀上的文档" | `search.py` → `get_doc.py` → edit → `update_doc.py` |
| "列出我的知识库" | `list_repos.py` |
| "查看知识库目录" | `get_toc.py --repo R` |
| "整理/重新组织笔记" | `get_toc.py` → `update_toc.py` |
| "创建新的知识库" | `create_repo.py --name "X" --slug x` |
| "删除这篇文档" | `delete_doc.py --repo R --doc D` |
| "查看文档历史版本" | `doc_versions.py --doc D` |
