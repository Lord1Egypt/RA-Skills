---
name: robots-txt-gen
description: Generate, validate, and analyze robots.txt files for websites. Use when creating robots.txt from scratch, validating existing robots.txt syntax, checking if a URL is allowed/blocked by robots.txt rules, or generating robots.txt for common platforms (WordPress, Next.js, Django, Rails). Also use when auditing crawl directives or debugging search engine indexing issues.
---

# robots-txt-gen

Generate, validate, and test robots.txt files from the command line.

## Quick Start

```bash
# Generate a robots.txt for a platform
python3 scripts/robots_txt_gen.py generate --preset nextjs --sitemap https://example.com/sitemap.xml

# Validate an existing robots.txt
python3 scripts/robots_txt_gen.py validate --file robots.txt

# Validate a remote robots.txt
python3 scripts/robots_txt_gen.py validate --url https://example.com/robots.txt

# Test if a URL is allowed for a user-agent
python3 scripts/robots_txt_gen.py test --file robots.txt --url /admin/dashboard --agent Googlebot

# Generate with custom rules
python3 scripts/robots_txt_gen.py generate --allow "/" --disallow "/admin" --disallow "/api" --disallow "/private" --sitemap https://example.com/sitemap.xml --agent "*"
```

## Commands

### `generate`
Create a robots.txt file with custom rules or platform presets.

Options:
- `--preset <name>` — Use a platform preset: `wordpress`, `nextjs`, `django`, `rails`, `laravel`, `static`, `spa`, `ecommerce`
- `--agent <name>` — User-agent (default: `*`). Repeat for multiple agents.
- `--allow <path>` — Allow path. Repeatable.
- `--disallow <path>` — Disallow path. Repeatable.
- `--sitemap <url>` — Sitemap URL. Repeatable.
- `--crawl-delay <seconds>` — Crawl delay directive.
- `--block-ai` — Add rules to block common AI crawlers (GPTBot, ChatGPT-User, CCBot, Google-Extended, anthropic-ai, etc.)
- `--output <file>` — Write to file instead of stdout.

### `validate`
Check a robots.txt file for syntax errors and best-practice warnings.

Options:
- `--file <path>` — Local file to validate.
- `--url <url>` — Remote robots.txt URL to fetch and validate.

### `test`
Test whether a specific URL path is allowed or disallowed for a given user-agent.

Options:
- `--file <path>` — robots.txt file to test against.
- `--url <path>` — URL path to test (e.g., `/admin/login`).
- `--agent <name>` — User-agent to test as (default: `Googlebot`).

## Platform Presets

| Preset | What it blocks | Notes |
|--------|---------------|-------|
| `wordpress` | `/wp-admin/`, `/wp-includes/`, query params | Allows `/wp-admin/admin-ajax.php` |
| `nextjs` | `/_next/static/`, `/api/`, `/.next/` | Standard Next.js paths |
| `django` | `/admin/`, `/static/admin/`, `/media/private/` | Django admin and private media |
| `rails` | `/admin/`, `/assets/`, `/tmp/` | Rails conventions |
| `laravel` | `/admin/`, `/storage/`, `/vendor/` | Laravel conventions |
| `static` | Nothing blocked | Simple allow-all with sitemap |
| `spa` | `/api/`, `/assets/` | Single-page app pattern |
| `ecommerce` | `/cart/`, `/checkout/`, `/account/`, `/search?` | Prevents crawling user sessions |

## AI Crawler Blocking

The `--block-ai` flag adds disallow rules for known AI training crawlers:
- GPTBot, ChatGPT-User (OpenAI)
- Google-Extended (Google AI)
- CCBot (Common Crawl)
- anthropic-ai (Anthropic)
- Bytespider (ByteDance)
- ClaudeBot (Anthropic)
- FacebookBot (Meta)
