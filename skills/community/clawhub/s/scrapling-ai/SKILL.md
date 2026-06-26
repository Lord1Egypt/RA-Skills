---
name: scrapling
description: Use Scrapling to scrape websites with adaptive parsing, Cloudflare bypass, and MCP support. Handles dynamic content, anti-bot detection, and provides clean HTML/JSON output.
metadata:
  {
    "openclaw":
      {
        "emoji": "🕷️",
        "requires": { "bins": ["scrapling"] },
        "install":
          [
            {
              "id": "pipx",
              "kind": "pipx",
              "package": "scrapling",
              "bins": ["scrapling"],
              "label": "Install Scrapling CLI (pipx)",
            },
            {
              "id": "python3-pip",
              "kind": "pip",
              "package": "scrapling",
              "bins": ["scrapling"],
              "label": "Install Scrapling CLI (pip)",
            },
          ],
      },
  }
---

# Scrapling Skill

Use the `scrapling` CLI to scrape websites with adaptive parsing and anti-bot bypass.

## When to Use

✅ **USE this skill when:**

- Scrape static or dynamic websites
- Bypass Cloudflare, captcha, or bot detection
- Extract structured data (HTML/JSON) from web pages
- Handle JavaScript-rendered content
- Get clean HTML without extra scripts/CSS

## When NOT to Use

❌ **DON'T use this skill when:**

- Simple HTTP requests → use `web_fetch`
- Need full browser automation → use `browser` tool
- API-based data → use direct API calls
- Local file processing → use file tools

## Setup

```bash
# Install CLI
pipx install scrapling
scrapling --version
```

## Common Commands

### Basic Scrape

```bash
# Get clean HTML
scrapling https://example.com -o html

# Get JSON structure
scrapling https://example.com -o json

# Save to file
scrapling https://example.com -o output.html
```

### With Headers/Timeouts

```bash
# Custom headers
scrapling https://example.com --headers "User-Agent: Mozilla/5.0"

# Timeout (seconds)
scrapling https://slow-site.com --timeout 30
```

### Extract Specific Elements

```bash
# XPath extraction
scrapling https://example.com -e "//div[@class='content']" -o html

# CSS selector
scrapling https://example.com -e "div.content" -o html
```

### JSON Output with Fields

```bash
# Extract title, meta description
scrapling https://example.com \
  --fields 'title,meta_description' \
  -o json
```

## MCP Integration

Scrapling supports MCP (Model Context Protocol) for AI agents:

```bash
# Start MCP server
scrapling mcp start
```

Then configure your agent to use the `scrape` tool via MCP.

## Examples

### Scrape News Article

```bash
scrapling https://example.com/news/article-123 \
  --fields 'title,author,publish_date,content' \
  -o json
```

### Extract Product Data

```bash
scrapling https://shop.example.com/products \
  -e "//div[@class='product']" \
  -o html
```

### Handle Cloudflare

```bash
# Scrapling auto-bypasses most protections
scrapling https://protected-site.com -o html
```

## Notes

- Default timeout: 10 seconds
- Auto-detects best output format (html/json/text)
- Handles dynamic content via headless browser when needed
- Rate limit friendly; add delays between requests

## JSON Output Format

```json
{
  "title": "Page Title",
  "meta_description": "Description text",
  "content": "<clean HTML>",
  "links": ["http://...", "..."],
  "images": [{"src": "...", "alt": "..."}]
}
```

Use the `scrapling` CLI to scrape websites with adaptive parsing and anti-bot bypass.

## When to Use

✅ **USE this skill when:**

- Scrape static or dynamic websites
- Bypass Cloudflare, captcha, or bot detection
- Extract structured data (HTML/JSON) from web pages
- Handle JavaScript-rendered content
- Get clean HTML without extra scripts/CSS

## When NOT to Use

❌ **DON'T use this skill when:**

- Simple HTTP requests → use `web_fetch`
- Need full browser automation → use `browser` tool
- API-based data → use direct API calls
- Local file processing → use file tools

## Setup

```bash
# Install CLI
pipx install scrapling
scrapling --version
```

## Common Commands

### Basic Scrape

```bash
# Get clean HTML
scrapling https://example.com -o html

# Get JSON structure
scrapling https://example.com -o json

# Save to file
scrapling https://example.com -o output.html
```

### With Headers/Timeouts

```bash
# Custom headers
scrapling https://example.com --headers "User-Agent: Mozilla/5.0"

# Timeout (seconds)
scrapling https://slow-site.com --timeout 30
```

### Extract Specific Elements

```bash
# XPath extraction
scrapling https://example.com -e "//div[@class='content']" -o html

# CSS selector
scrapling https://example.com -e "div.content" -o html
```

### JSON Output with Fields

```bash
# Extract title, meta description
scrapling https://example.com \
  --fields 'title,meta_description' \
  -o json
```

## MCP Integration

Scrapling supports MCP (Model Context Protocol) for AI agents:

```bash
# Start MCP server
scrapling mcp start
```

Then configure your agent to use the `scrape` tool via MCP.

## Examples

### Scrape News Article

```bash
scrapling https://example.com/news/article-123 \
  --fields 'title,author,publish_date,content' \
  -o json
```

### Extract Product Data

```bash
scrapling https://shop.example.com/products \
  -e "//div[@class='product']" \
  -o html
```

### Handle Cloudflare

```bash
# Scrapling auto-bypasses most protections
scrapling https://protected-site.com -o html
```

## Notes

- Default timeout: 10 seconds
- Auto-detects best output format (html/json/text)
- Handles dynamic content via headless browser when needed
- Rate limit friendly; add delays between requests

## JSON Output Format

```json
{
  "title": "Page Title",
  "meta_description": "Description text",
  "content": "<clean HTML>",
  "links": ["http://...", "..."],
  "images": [{"src": "...", "alt": "..."}]
}
```
