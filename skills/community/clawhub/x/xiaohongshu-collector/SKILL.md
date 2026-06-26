---
name: xiaohongshu-collector
description: Work on Xiaohongshu post/comment collection, cookie handling, refresh flows, and browser plugin integration in the forbidden_company repo.
---

# Xiaohongshu Collector

## Overview

Use this skill when working on Xiaohongshu collection in `forbidden_company`, especially for post bodies, comment pagination, cookie updates, single-URL refreshes, or browser-plugin integration.

## What To Use

Prefer the existing repo implementation instead of inventing a new flow:
- `scripts/collect_xiaohongshu.py`
- `scripts/admin_server.py`
- `scripts/run_xiaohongshu_collection.sh`
- `browser-extension/xhs-collector/`
- `docs/xiaohongshu-collector.md`
- `docs/xhs-plugin-api.md`

## Core Rules

- Keep cookies private. Never repeat them in final output.
- `comment_limit=0` means collect all available comments.
- Comment collection must paginate.
- If the direct comment API returns a login/account error, use the browser-rendered fallback.
- Do not rely on Firecrawl for comment pagination.

## Workflow

1. Confirm whether the task is batch collection or single-URL refresh.
2. Load the saved cookie from `data/xiaohongshu-cookie.txt` unless a newer cookie is provided.
3. Run or update `scripts/collect_xiaohongshu.py` with the requested URL(s), `--db`, `--refresh-url`, and `--comment-limit 0` when full comments are needed.
4. For browser plugin work, wire the popup/background scripts to the local backend endpoints in `scripts/admin_server.py`.
5. Verify that post rows, comment rows, and exported artifacts are written correctly.

## Endpoint Map

Use these backend endpoints when integrating the browser plugin:
- `GET/POST /api/xhs-cookie`
- `GET /api/xhs-plugin/status`
- `POST /api/xhs-plugin/collect`
- `POST /api/xhs-plugin/refresh`

## Validation Notes

- Refresh mode must delete the old note rows before writing the new ones.
- The plugin should expose downloadable CSV and JSON artifacts.
- When debugging, check whether the failure is cookie-related, pagination-related, or page-structure related.

## Safety Notes

- Do not propose or implement shared-server mass scraping.
- Keep the browser/plugin model user-driven and local-first.
- Preserve source URLs and timestamps for traceability.

## Reference

See [collector-workflow.md](references/collector-workflow.md) for operational details.
