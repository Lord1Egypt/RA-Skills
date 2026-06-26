---
name: Skreenshot
description: Organize, tag, search, and manage screenshots on macOS. Use when users need to: (1) find specific screenshots, (2) organize screenshots into folders by category/project, (3) search screenshot content via OCR, (4) bulk rename or move screenshots, (5) clean up old screenshots, or (6) integrate with CleanShot X or macOS screenshot tool.
---

# Skreenshot

macOS accumulates screenshots rapidly—on the Desktop by default, often forgotten and unorganized. This skill provides workflows to tame the chaos.

## Quick Start

**Find screenshots:**
```bash
# List recent screenshots (last 7 days)
find ~/Desktop -name "Screenshot*.png" -mtime -7 | head -20

# Search by content (OCR)
textsnip -i ~/Desktop/Screenshot*.png | grep -i "receipt"
```

**Organize:**
```bash
# Move to categorized folders
mkdir -p ~/Pictures/Screenshots/{work,personal,receipts,memes}
mv ~/Desktop/Screenshot*.png ~/Pictures/Screenshots/personal/
```

## Default Screenshot Location

macOS saves to `~/Desktop` by default. Change it:
```bash
# Set custom location
defaults write com.apple.screencapture location ~/Pictures/Screenshots
killall SystemUIServer
```

## Screenshot Naming Patterns

Default: `Screenshot YYYY-MM-DD at HH.MM.SS.png`

Smart rename with context:
```bash
# Use script for batch rename with date + optional tags
python scripts/rename_screenshots.py --add-tags work,receipt
```

## OCR Search

Search screenshot content with OCR tools:
- **textsnip** (CLI): `textsnip -i *.png | grep "search term"`
- **EasyOCR** (Python): See `references/ocr-setup.md`
- **macOS built-in**: Live Selection (Cmd+Shift+4 then drag)

## Organization Strategies

### By Project/Client
```
Pictures/Screenshots/
├── client-acme/
├── client-globex/
└── personal/
```

### By Category
```
Pictures/Screenshots/
├── receipts/
├── bugs/
├── inspiration/
├── memes/
└── reference/
```

### By Date (auto-archive)
```
Pictures/Screenshots/
├── 2026/
│   ├── 01-january/
│   ├── 02-february/
│   └── ...
```

## CleanShot X Integration

If using CleanShot X:
- Screenshots save to custom folder (configurable)
- OCR built-in (Cmd+Shift+O)
- Auto-upload to cloud (optional)

See `references/cleancast-x.md` for workflow details.

## Automation Scripts

### `scripts/rename_screenshots.py`
Batch rename with smart patterns (date, app name, tags).

### `scripts/archive_old_screenshots.py`
Move screenshots older than N days to archive folder.

### `scripts/ocr_search.py`
Search all screenshots by text content.

## Workflow Examples

**"Find that screenshot of the error message"**
1. Search by date range (when did you see the error?)
2. OCR search for error text
3. Open matching results

**"Organize my Desktop screenshots"**
1. Run archive script for old screenshots
2. Move recent ones to categorized folders
3. Update links if needed (wikilinks, docs)

**"Search all screenshots for 'invoice'"**
1. Run OCR search script
2. Filter results by date/category
3. Return matches with preview

---

**References:**
- `references/ocr-setup.md` - OCR tool setup and usage
- `references/cleancast-x.md` - CleanShot X workflows
- `references/automation-patterns.md` - Advanced automation scripts
