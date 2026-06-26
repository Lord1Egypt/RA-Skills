# Changelog

## 1.1.0

- Add bookmark folder auto-routing: folders matched to notebooks by name (case-insensitive)
- Add `list_folders.py` script
- Add `--folder-id` flag to `fetch_bookmarks.py`
- Add `auto_sync.py` for cron-based unattended sync
- Rewrite SKILL.md workflow for folder-first routing
- Push tweets as text sources instead of URLs (X blocks scraping)
- Strip emojis and `-notebook`/`-bookmarks` suffix from names when matching
- Harden `auto_sync.py`: shell injection prevention, error logging

## 1.0.0

Initial release.
