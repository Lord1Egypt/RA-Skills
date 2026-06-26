---
name: url2md
description: Convert web pages to Markdown format. Use when the user needs to: (1) Extract readable content from a URL and convert it to Markdown, (2) Batch convert multiple URLs to Markdown files, (3) Save web page content as .md for documentation, archiving, or note-taking. Works with any HTTP/HTTPS URL that returns HTML content. Also use when OpenClaw's web_fetch tool is insufficient and a script-based or bulk conversion approach is preferred.
---

# Url2md

Convert web pages to clean, readable Markdown.

## Quick Start

### Single URL

```bash
python3 scripts/url2md.py https://example.com/article
```

Output to a file:
```bash
python3 scripts/url2md.py https://example.com/article -o article.md
```

### Batch Conversion

Create a file with URLs (one per line):
```
https://example.com/article-1
https://example.com/article-2
https://example.com/article-3
```

Convert all and save to a directory:
```bash
python3 scripts/url2md.py -f urls.txt -d ./markdown_files/
```

## Features

- **No dependencies**: Uses only Python standard library (`urllib`, `html.parser`)
- **Reader-style scope**: Strips `script`/`style`/`noscript`/`template`, then prefers the first `<article>` or `<main>` (else `<body>`) so output focuses on primary content
- **Title extraction**: Uses `og:title` / Twitter title when present, otherwise `<title>`, added as H1 when enabled
- **YAML Frontmatter**: Extracts structured metadata (title, author, published, description, category, source) from `<meta>` tags and Schema.org JSON-LD for knowledge-base workflows
- **Template system**: Customize output format with variables (`{{title}}`, `{{content}}`, `{{author}}`, `{{published}}`, `{{date}}`, etc.)
- **Link resolution**: Converts relative URLs to absolute
- **Basic formatting**: Headings, paragraphs, lists, links, images, fenced code (with optional language), GFM-style tables, bold/italic
- **Noise removal**: Skips navigation, sidebars, footers, forms, and other chrome inside the parsed fragment

## Script Reference

### `scripts/url2md.py`

**Usage:**
```
url2md.py [url] [options]
```

**Options:**
| Option | Description |
|--------|-------------|
| `url` | Single URL to convert |
| `-o, --output` | Output file (default: stdout) |
| `-f, --file` | File containing URLs to convert |
| `-d, --dir` | Output directory for batch conversion |
| `--no-title` | Skip adding page title as H1 |
| `--full-page` | Parse full `<body>` instead of `<article>`/`<main>` first (more chrome, wider coverage) |
| `--timeout` | Request timeout in seconds (default: 30) |
| `--frontmatter` | Add YAML frontmatter with extracted metadata |
| `-t, --template` | Path to a template file for customizing output |
| `--filename-template` | Batch mode filename pattern (e.g. `{{date}}-{{title}}.md`) |
| `--download-images` | Download remote images to a local folder (e.g. `assets`) |
| `-v, --version` | Show version |

**Examples:**
```bash
# Single URL to stdout
python3 scripts/url2md.py https://docs.python.org/3

# Save to file
python3 scripts/url2md.py https://docs.python.org/3 -o python-docs.md

# Batch with custom timeout
python3 scripts/url2md.py -f urls.txt -d ./output/ --timeout 60

# Skip title
python3 scripts/url2md.py https://example.com --no-title

# Whole body (no article/main focus)
python3 scripts/url2md.py https://example.com/sitemap --full-page -o sitemap.md

# YAML frontmatter (great for Obsidian / PKM)
python3 scripts/url2md.py https://example.com/article --frontmatter -o article.md

# Custom template
python3 scripts/url2md.py https://example.com/article -t article.tpl -o article.md

# Batch with smart filenames
python3 scripts/url2md.py -f urls.txt -d ./output/ --filename-template "{{date}}-{{title}}.md"

# Download images locally
python3 scripts/url2md.py https://example.com/article -o article.md --download-images assets
python3 scripts/url2md.py -f urls.txt -d ./output/ --download-images assets
```

**Template variables:** `{{title}}`, `{{content}}`, `{{url}}`, `{{source}}`, `{{author}}`, `{{published}}`, `{{description}}`, `{{category}}`, `{{site_name}}`, `{{date}}`, `{{datetime}}`

## When to Use

- Converting documentation pages to Markdown for local reference
- Archiving web articles as text files
- Building a knowledge base with structured metadata (frontmatter / templates)
- Building static content from dynamic sources
- Extracting readable content when browser tools are unavailable
- Batch processing a list of URLs

## Limitations

- Converts static HTML only; does not execute JavaScript
- Complex layouts (multi-column, heavy CSS) may lose structural fidelity
- Login-required or paywalled content requires authentication tokens
- Rate-limited sites may block repeated requests
