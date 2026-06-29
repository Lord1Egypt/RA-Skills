---
name: url-bookmarker
description: >
  Save, categorize, search, and export web bookmarks. Use when user wants to bookmark a URL, organize links into folders/tags, find a saved link, or export bookmarks. Commands: add url title -t tags -f folder, list filter, search query, tag url tags, remove url, export format.
---

# URL Bookmarker

Save, categorize, search, and export web bookmarks with tag and folder organization. Uses local JSON storage.

## Commands

### Add a bookmark
```
bookmark add <url> [title] [-t tags] [-f folder]
```
- `url` (required): The web address to save
- `title` (optional): Custom title, defaults to URL hostname
- `-t tags`: Comma-separated tags (e.g. `-t crypto,research`)
- `-f folder`: Folder name (e.g. `-f DeFi`)

### List bookmarks
```
bookmark list [filter]
```
- No filter: shows all bookmarks
- `-t tag`: filter by tag
- `-f folder`: filter by folder
- `-a`: show all tags and folders

### Search bookmarks
```
bookmark search <query>
```
Full-text search across URLs, titles, and tags.

### Tag a bookmark
```
bookmark tag <url> <tags>
```
Add tags to an existing bookmark. Use `-t` to replace all tags.

### Remove a bookmark
```
bookmark remove <url>
```

### Export bookmarks
```
bookmark export [format]
```
Formats: `json` (default), `html` (browser-importable), `csv`

## Storage

Bookmarks stored in `assets/bookmarks.json`:
```json
{
  "urls": [{ "url": "...", "title": "...", "tags": [], "folder": null, "added": "ISO date" }],
  "tags": ["tag1", "tag2"],
  "folders": ["folder1"]
}
```

## Script Usage

Run via Python (from skill directory):
```
$env:PYTHONIOENCODING="utf-8"; uv run python scripts/bookmark_manager.py <command> [args]
```

Examples:
```
uv run python scripts/bookmark_manager.py add https://example.com "Example Site" -t research -f DevTools
uv run python scripts/bookmark_manager.py list -t crypto
uv run python scripts/bookmark_manager.py search "uniswap"
uv run python scripts/bookmark_manager.py export html
```