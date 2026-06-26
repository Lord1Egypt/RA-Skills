---
name: update-md
description: Create or update project documentation in Markdown. Use when building a new project doc set, updating existing docs after a deploy or feature change, or establishing a doc structure for a new project. Covers doc splitting, update rules, naming conventions, and the standard file map pattern used across all projects (TPMS, TonicLab, etc.).
---

# update-md

## Core Principles

1. **Split, don't consolidate** — One file per concern. Never dump everything into one doc.
2. **Overview is always the entry point** — Every project has a `PROJECT-OVERVIEW.md` that's lean and links to everything else.
3. **按需讀取** — Detail files are only read when needed; keep them out of the overview.
4. **Update rules are mandatory** — Every doc set must define when each file should be updated.
5. **Deploy = Update docs** — Docs update immediately after every deploy. No exceptions.

## Standard Doc Set Structure

Every project follows this pattern:

```
PROJECT-OVERVIEW.md     ← 精簡總覽，每 session 必讀
PROJECT-DEPLOY.md       ← 部署、Docker、Nginx、SSL、環境變數
PROJECT-APPS.md         ← 功能規格（如有多個 app/module）
PROJECT-DB.md           ← 數據庫 schema 及連接設定
PROJECT-HISTORY.md      ← 版本日誌，每次 deploy 後更新
```

Add or remove files based on project complexity. See `references/doc-templates.md` for file templates.

## OVERVIEW.md Must-Haves

- Project name, domain/URL, status, VM/hosting info
- Feature/tool status table (✅ / 🔄 / ⏳ / ❌)
- Doc map table (file → content)
- **Update rules table** (change type → files to update)
- Current version number

## Update Rules (include in every OVERVIEW.md)

| 改動類型 | 需要更新 |
|----------|----------|
| 新功能 / 改功能 | OVERVIEW（狀態）+ APPS |
| 新版本發布 | HISTORY + OVERVIEW（版本號）|
| 部署/基礎設施改動 | DEPLOY |
| DB schema 改動 | DB |

## Status Symbols

Use consistently across all docs:

- ✅ 完成
- 🔄 進行中
- ⏳ 待開始
- ❌ 取消 / 廢棄

## When Updating Docs

1. Identify which files are affected by the change (use the update rules table)
2. Update only those files — don't touch unrelated docs
3. Update version number in OVERVIEW if it's a release
4. Add entry to HISTORY with date, version, and bullet points

## Creating a New Doc Set

1. Create `PROJECT-OVERVIEW.md` first — establish the doc map before writing detail files
2. Add detail files as needed (DEPLOY, APPS, DB, HISTORY)
3. Add the doc map to the project's `AGENTS.md` so agents know which files exist
4. Reference `references/doc-templates.md` for boilerplate

See `references/doc-templates.md` for ready-to-use file templates.
