---
name: siyuan-agent
description: Interact with SiYuan notes via direct HTTP API. Use when reading, writing, searching, or managing SiYuan blocks, documents, notebooks, attributes, assets, or executing SQL queries.
author: eloklam
metadata:
  requiredEnvs:
    - SIYUAN_TOKEN
  primaryCredential: SIYUAN_TOKEN
---

# siyuan-agent (Direct HTTP)

Standalone CLI for [SiYuan](https://ld246.com/) — direct HTTP API access, no npm dependencies.

## Setup

1. Enable SiYuan API token: SiYuan → Settings → About → API token
2. Set the token:

```bash
export SIYUAN_TOKEN=your_token_here
export SIYUAN_BASE=http://127.0.0.1:6806   # optional, default shown
```

(Add these to your `~/.bashrc` or `~/.zshrc` to persist.)

**You don't need to use the CLI yourself.** Just tell your agent to read this SKILL.md — it will use this tool automatically.

## Commands

### Read
| Command | Description |
|---|---|
| `search query=<kw>` | Full-text search |
| `searchByNotebook query=<kw> notebook=<id>` | Search in specific notebook |
| `getDoc id=<blockID>` | Get document |
| `getBlock id=<blockID>` | Get single block |
| `getChildren id=<blockID>` | Get child blocks |
| `backlinks id=<blockID>` | Find backlinks |
| `outline id=<blockID>` | Get document outline |
| `sql "SELECT ..."` | Execute SELECT-only SQL |
| `exportMd id=<docID>` | Export doc to markdown |
| `call path=/api/... '{}'` | Any API endpoint directly |

### Write (requires write=true)
| Command | Description |
|---|---|
| `insertBlock parentID=<id> data="<content>" write=true` | Insert block |
| `updateBlock id=<id> data="<content>" write=true` | Update block |
| `deleteBlock id=<id> write=true` | Delete block |

## SQL Safety

The `sql` command only allows SELECT statements. Non-SELECT queries are rejected with an error.

## Write Protection

Write operations (`insertBlock`, `updateBlock`, `deleteBlock`) require `write=true`.
The `call` command requires `write=true` for non-read paths (export, asset upload are treated as write paths).

## Hard-Blocked Paths

These notebook operations are blocked and cannot be called:
- `/api/notebook/createNotebook`
- `/api/notebook/removeNotebook`
- `/api/notebook/renameNotebook`
- `/api/notebook/closeNotebook`
- `/api/notebook/saveNotebookConf`

## Usage Examples

```bash
# Search
node siyuan.js search query=keyword

# Read a block
node siyuan.js getBlock id=20260321111240-o5xe15o

# Get document
node siyuan.js getDoc id=20260321111240-o5xe15o

# Get child blocks
node siyuan.js getChildren id=20260321111240-o5xe15o

# SQL query
node siyuan.js sql "SELECT id, type, content FROM blocks WHERE content LIKE '%keyword%' LIMIT 5"

# Write operation
node siyuan.js updateBlock id=20260321111240-o5xe15o data="New content" write=true

# Direct API call
node siyuan.js call path=/api/notebook/lsNotebooks '{}'
```

## Files

```
siyuan.js   — CLI entry point (native fetch, no deps)
lib/api.js  — HTTP API caller
```
