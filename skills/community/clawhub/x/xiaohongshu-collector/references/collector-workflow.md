# Xiaohongshu Collector Workflow

## Scope
Use this skill when you need to work on Xiaohongshu post/comment collection in the `forbidden_company` repo, especially:
- collecting posts and comments from note URLs
- refreshing a single Xiaohongshu URL
- updating or reading the saved cookie
- wiring the browser plugin to the local backend
- debugging comment pagination or login failures

## Canonical Files
Prefer the existing repo files before inventing new flows:
- `scripts/collect_xiaohongshu.py`
- `scripts/admin_server.py`
- `scripts/run_xiaohongshu_collection.sh`
- `browser-extension/xhs-collector/`
- `docs/xiaohongshu-collector.md`
- `docs/xhs-plugin-api.md`

## Collection Rules
- Treat the browser cookie as sensitive. Never echo it back in final output.
- `comment_limit=0` means "collect all available comments".
- Comment collection must support pagination.
- If the direct comment API returns an auth or account error, prefer the browser-rendered fallback.
- Do not rely on Firecrawl for comment pagination; it is only a post-body fallback.

## Recommended Workflow
1. Confirm the note URL and whether the user wants a one-off refresh or a batch run.
2. Read the saved cookie from `data/xiaohongshu-cookie.txt` unless the user provides a newer cookie.
3. Run or update `scripts/collect_xiaohongshu.py` with:
   - `--input-urls`
   - `--output-csv`
   - `--db` when persistence is needed
   - `--refresh-url` for replacing one existing note
   - `--comment-limit 0` for full comment collection
4. If comment collection fails, check whether:
   - cookie is missing or stale
   - the browser fallback is unavailable
   - the page returns a platform auth/account error
5. For backend integration, use the plugin endpoints in `scripts/admin_server.py`:
   - `GET/POST /api/xhs-cookie`
   - `GET /api/xhs-plugin/status`
   - `POST /api/xhs-plugin/collect`
   - `POST /api/xhs-plugin/refresh`

## Result Handling
- Post rows and comment rows are written into the same evidence table/CSV flow.
- Refresh mode must delete the old note rows before writing the new ones.
- Plugin results should expose downloadable CSV and JSON artifacts.

## Safety Notes
- Never propose or implement centered mass scraping from a shared server IP.
- Keep the browser/plugin model user-driven and local-first.
- Preserve source URLs and timestamps for traceability.
