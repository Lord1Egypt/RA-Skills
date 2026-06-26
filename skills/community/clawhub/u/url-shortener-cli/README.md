# URL Shortener CLI

Local, self‑contained URL shortener for your terminal.

## Features

- **Shorten URLs** with auto‑generated or custom slugs
- **Local storage** – no external APIs, no internet required
- **Basic analytics** – track click counts
- **Search & management** – list, search, update, delete
- **Import/export** – backup your URL database

## Quick Start

1. Shorten a URL:
   ```bash
   ./scripts/main.py shorten https://example.com/very/long/path
   ```

2. Use a custom slug:
   ```bash
   ./scripts/main.py shorten https://example.com --slug mypage
   ```

3. Expand a slug:
   ```bash
   ./scripts/main.py expand mypage
   ```

4. List all mappings:
   ```bash
   ./scripts/main.py list
   ```

## Commands

- `shorten` – Create short URL
- `expand` – Get original URL
- `list` – List all mappings
- `info` – Show details for a slug
- `delete` – Delete a mapping
- `search` – Search in URLs/descriptions/tags
- `export` / `import` – Backup/restore
- `stats` – Usage statistics
- `cleanup` – Remove old entries

## Storage

All mappings are saved in `~/.url-shortener/mappings.json`.

## Requirements

Python 3.6+ (no external dependencies)

## License

MIT