---
name: url-shortener-cli
description: Shorten URLs from terminal with custom slugs, local storage, and basic analytics. A self‑contained CLI that maps long URLs to short slugs using a local JSON file.
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# URL Shortener CLI

## What This Does

A local, self‑contained URL shortener that runs entirely on your machine. No external APIs, no internet required after setup.

Key features:
- **Shorten URLs** – Generate short slugs for long URLs
- **Custom slugs** – Use your own short codes
- **Expand slugs** – Retrieve original URLs
- **Local storage** – All mappings saved in a JSON file (`~/.url-shortener/mappings.json`)
- **Basic analytics** – Track click counts and creation dates
- **Management** – List, search, update, and delete mappings
- **Import/export** – Backup and restore your URL database

## How To Use

### Shorten a URL:
```bash
./scripts/main.py shorten https://example.com/very/long/path
```

### Shorten with custom slug:
```bash
./scripts/main.py shorten https://example.com --slug mypage
```

### Expand a slug:
```bash
./scripts/main.py expand mypage
```

### List all mappings:
```bash
./scripts/main.py list
```

### Get detailed info for a slug:
```bash
./scripts/main.py info mypage
```

### Delete a mapping:
```bash
./scripts/main.py delete mypage
```

### Search URLs:
```bash
./scripts/main.py search "example"
```

### Import/export:
```bash
./scripts/main.py export --file urls.json
./scripts/main.py import --file urls.json
```

### Full command reference:
```bash
./scripts/main.py help
```

## Commands

- `shorten`: Create a new short URL
  - `url`: The long URL to shorten (required)
  - `--slug`: Custom slug (optional, auto‑generated if omitted)
  - `--description`: Optional description
  - `--tags`: Comma‑separated tags for organization

- `expand`: Get the original URL for a slug
  - `slug`: The short slug (required)

- `list`: List all mappings
  - `--sort`: Sort by `created`, `clicks`, `slug`, `url` (default: created)
  - `--reverse`: Reverse sort order
  - `--limit`: Show only N entries
  - `--json`: Output as JSON

- `info`: Show detailed information for a slug
  - `slug`: The short slug (required)
  - `--json`: Output as JSON

- `delete`: Delete a mapping
  - `slug`: The short slug to delete (required)
  - `--force`: Skip confirmation

- `search`: Search in URLs, descriptions, or tags
  - `query`: Search term (required)
  - `--field`: Search field: `url`, `description`, `tags`, `all` (default: all)

- `export`: Export mappings to a JSON file
  - `--file`: Output file (default: `urls-export.json`)

- `import`: Import mappings from a JSON file
  - `--file`: Input file (required)
  - `--overwrite`: Replace existing mappings (default: merge)

- `stats`: Show usage statistics
  - `--json`: Output as JSON

- `cleanup`: Remove old or unused mappings
  - `--older-than-days`: Remove entries older than N days
  - `--max-clicks`: Remove entries with fewer than N clicks
  - `--dry-run`: Show what would be removed

## Output Examples

### Shorten a URL:
```
$ ./scripts/main.py shorten https://github.com/openclaw/openclaw
Shortened: https://github.com/openclaw/openclaw
Slug:      x7f9k2
Full command: ./scripts/main.py expand x7f9k2
```

### List mappings:
```
Slug     URL                                     Clicks  Created
-------  --------------------------------------  ------  -------------------
x7f9k2   https://github.com/openclaw/openclaw    12      2026‑03‑18 10:30:00
mypage   https://example.com                     5       2026‑03‑17 14:22:00
docs     https://docs.openclaw.ai                42      2026‑03‑16 09:15:00
```

### JSON output (with `--json`):
```json
{
  "x7f9k2": {
    "url": "https://github.com/openclaw/openclaw",
    "slug": "x7f9k2",
    "clicks": 12,
    "created": "2026-03-18T10:30:00Z",
    "description": "OpenClaw GitHub repo",
    "tags": ["github", "openclaw"]
  }
}
```

## Installation Notes

Requires Python 3.6+. No external dependencies. The tool creates a configuration directory at `~/.url-shortener/` and stores mappings in `mappings.json`.

## Limitations

- **Local only** – Mappings exist only on your machine; not shareable across devices
- **No public access** – Shortened URLs only work on your own system
- **No expiration** – Entries persist until manually deleted
- **No collision detection** – Custom slugs must be unique (tool will warn)
- **Basic analytics** – Only tracks click counts; no geographic or referrer data
- **No QR codes** – Does not generate QR codes for shortened URLs
- **No API** – Cannot be called by other applications (except via CLI)

## Security Considerations

- All data stored locally in plain JSON (no encryption)
- No authentication required (any user on the system can access)
- URLs are not validated for safety (may point to malicious sites)
- No rate limiting or abuse protection
- File permissions follow your user's default

## Examples

### Create a short link for documentation:
```bash
./scripts/main.py shorten https://docs.openclaw.ai --slug docs --description "OpenClaw documentation"
```

### Get the most‑clicked links:
```bash
./scripts/main.py list --sort clicks --reverse --limit 5
```

### Search for GitHub links:
```bash
./scripts/main.py search "github" --field url
```

### Backup your URL database:
```bash
./scripts/main.py export --file url-backup-$(date +%Y%m%d).json
```

### Clean up old entries (older than 30 days):
```bash
./scripts/main.py cleanup --older-than-days 30
```