---
name: short-io
description: "Use this skill to manage Short.io branded short links via their REST API. Triggers on: create short link, shorten URL, Short.io, manage links, short link stats, track link clicks, branded short links, custom short URL, link shortener, delete short link, list short links, QR code for link, bulk create links, domain stats."
homepage: https://short.io
license: MIT
metadata:
  {
    "openclaw":
      {
        "emoji": "🔗",
        "requires": { "bins": ["curl", "jq", "python3", "column"], "env": ["SHORT_IO_API_KEY"] },
        "primaryEnv": "SHORT_IO_API_KEY",
      },
  }
---

# Short.io Skill

You are an agent managing Short.io branded short links via the Short.io REST API.

## Required Credentials

This skill requires a **Short.io secret API key** stored as an environment variable:

```
SHORT_IO_API_KEY=your_secret_key_here
```

Store it in a secrets file of your choice and source it before running. The default location used by this skill is `~/.secrets/shortio.env` (create the directory if needed: `mkdir -p ~/.secrets`). You can override the path by setting the variable in your shell environment directly.

Get your secret key from: **Short.io Dashboard > Settings > Integrations > API**

## Required Dependencies

The helper script requires these standard tools to be installed:
- `curl` — HTTP requests
- `jq` — JSON parsing
- `python3` — output formatting
- `column` — table formatting

These are pre-installed on most Linux/macOS systems. Install via `apt install curl jq python3` or `brew install curl jq python3` if missing.

## Setup

```bash
mkdir -p ~/.secrets
echo "SHORT_IO_API_KEY=your_key_here" > ~/.secrets/shortio.env
chmod 600 ~/.secrets/shortio.env
```

Use the helper script at `scripts/shortio.sh` for all operations, or make direct API calls using the reference in `references/api.md`.

## Authentication

All requests use the header:
```
authorization: YOUR_SECRET_API_KEY
```

Use the **secret key** from your Short.io dashboard (not the public key).

## Base URLs

- **Main API:** `https://api.short.io`
- **Statistics API:** `https://statistics.short.io`

## Common Workflows

### Shorten a URL
```bash
bash scripts/shortio.sh create --domain yourdomain.com --url https://example.com/long-path --path custom-slug
```

### List all links for a domain
First get your domain ID, then list links:
```bash
bash scripts/shortio.sh list --domain-id 12345
```

### Get link statistics
```bash
bash scripts/shortio.sh stats --link-id abc123
```

### Delete a link
```bash
bash scripts/shortio.sh delete --link-id abc123
```

## Key Notes

- Domain ID (`domain_id`) is required for listing links — get it from `GET /api/domains`
- `path` in create is the custom slug (optional — Short.io auto-generates if omitted)
- `shortURL` in response is the full shortened URL (e.g., `https://yourdomain.com/custom-slug`)
- Statistics API is a separate base URL: `https://statistics.short.io`
- Bulk create supports up to 1000 links per request

## Full API Reference

See `references/api.md` for complete endpoint documentation with curl examples.
