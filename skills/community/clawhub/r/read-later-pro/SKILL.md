---
name: read-later-pro
description: Read Later Pro - Save, organize, and read web articles offline. Extract clean article content from any URL, save as Markdown/PDF/EPUB, manage reading lists, and sync with popular read-later services. Use when users want to save articles for later reading, extract clean content from web pages, convert articles to different formats, organize reading lists, or work with read-later workflows.
---

# Read Later Pro

Save, organize, and read web articles offline. Extract clean article content from any URL and export to multiple formats.

## Features

- **Article Extraction**: Clean, readable content from any URL (removes ads, navigation, clutter)
- **Multiple Formats**: Export to Markdown, PDF, EPUB, or HTML
- **Reading List Management**: Organize saved articles with tags and search
- **Batch Processing**: Save multiple articles at once
- **Offline Reading**: Full-text search across saved articles
- **Service Integration**: Import from Pocket, Instapaper (export coming soon)

## Quick Start

### Save a Single Article

```bash
# Save article as Markdown
read-later save <url> --format markdown --output ./articles/

# Save as PDF
read-later save <url> --format pdf --output ./articles/

# Save with tags
read-later save <url> --tags "tech,ai" --output ./articles/
```

### Batch Save Articles

```bash
# From a list of URLs in a file
read-later batch --file urls.txt --format markdown --output ./articles/

# From browser bookmarks export
read-later import-bookmarks bookmarks.html --tags "imported"
```

### List and Search Saved Articles

```bash
# List all articles
read-later list

# Search articles
read-later search "machine learning"

# Filter by tags
read-later list --tags "tech"
```

### Export/Convert Saved Articles

```bash
# Convert saved article to different format
read-later convert <article-id> --format epub

# Export all articles as single PDF
read-later export --format pdf --output reading-collection.pdf
```

## Article Storage

Articles are stored with metadata:

```
articles/
├── article-slug/
│   ├── article.md       # Main content (Markdown)
│   ├── article.pdf      # PDF version (if generated)
│   ├── metadata.json    # Title, URL, date, tags, etc.
│   └── images/          # Downloaded images
```

## Integration with Read-Later Services

### Import from Pocket

```bash
read-later import-pocket --consumer-key <key> --access-token <token>
```

### Import from Instapaper

```bash
read-later import-instapaper --username <user> --password <pass>
```

## Reading Workflow

1. **Save**: Use `read-later save` to capture articles throughout the day
2. **Organize**: Add tags and notes to categorize content
3. **Read**: Open Markdown files in any text editor or viewer
4. **Search**: Use `read-later search` to find specific content
5. **Archive**: Move read articles to archive or delete

## Scripts

Use the provided scripts in `scripts/` directory:

- `extract_article.py` - Extract clean article content from URL
- `convert_format.py` - Convert between Markdown/PDF/EPUB/HTML
- `manage_library.py` - List, search, and organize saved articles
- `import_services.py` - Import from Pocket/Instapaper

## Tips

- Use `--full-content` flag to attempt bypassing paywalls (experimental)
- Images are downloaded locally for true offline reading
- Full-text search works across all saved article content
- Tags support nesting: "tech/ai", "tech/programming"
