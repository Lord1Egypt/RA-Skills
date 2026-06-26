---
name: webunlocker
description: Bypass website blocks and scrape web content using Scrapeless Universal Scraping API.
homepage: https://www.scrapeless.com
credentials:
  - X_API_TOKEN
env:
  required:
    - X_API_TOKEN
---

# WebUnlocker OpenClaw Skill

Use this skill to bypass website blocks and scrape web content using the Scrapeless Universal Scraping API. It supports JavaScript rendering, CAPTCHA solving, IP rotation, and intelligent request retries.

**Authentication:** Set `X_API_TOKEN` in your environment or in a `.env` file in the repo root.

**Errors:** On failure the script writes a JSON error to stderr and exits with code 1.

---

## Usage

**Command:**
```bash
python3 scripts/webunlocker.py --url "https://example.com"
```

**Examples:**
```bash
# Scrape HTML content
python3 scripts/webunlocker.py --url "https://httpbin.io/get"

# Scrape plain text
python3 scripts/webunlocker.py --url "https://example.com" --response-type plaintext

# Scrape as Markdown
python3 scripts/webunlocker.py --url "https://example.com" --response-type markdown

# Take a screenshot
python3 scripts/webunlocker.py --url "https://example.com" --response-type png

# Capture network requests
python3 scripts/webunlocker.py --url "https://example.com" --response-type network

# Extract specific content types
python3 scripts/webunlocker.py --url "https://example.com" --response-type content --content-types emails,links,images

# Use a specific country proxy
python3 scripts/webunlocker.py --url "https://example.com" --country US

# Use POST method
python3 scripts/webunlocker.py --url "https://httpbin.org/post" --method POST --data '{"key": "value"}'

# Add custom headers
python3 scripts/webunlocker.py --url "https://example.com" --headers '{"User-Agent": "Mozilla/5.0"}'

# Use custom proxy
python3 scripts/webunlocker.py --url "https://example.com" --proxy-url "http://your-proxy-url:port"

# Enable JavaScript rendering
python3 scripts/webunlocker.py --url "https://example.com" --js-render

# Enable JavaScript rendering with headless mode
python3 scripts/webunlocker.py --url "https://example.com" --js-render --headless

# Enable JavaScript rendering and wait for specific element
python3 scripts/webunlocker.py --url "https://example.com" --js-render --wait-selector "body > div > p:nth-child(3) > a"

# Bypass Cloudflare protection with JavaScript rendering
python3 scripts/webunlocker.py --url "https://example.com" --js-render

# Bypass Cloudflare Turnstile challenge
python3 scripts/webunlocker.py --url "https://2captcha.com/demo/cloudflare-turnstile-challenge" --js-render --headless --response-type markdown
```

---

## Summary

| Argument | Description | Default |
|----------|-------------|---------|
| `--url` | Target URL | Required |
| `--method` | HTTP method | GET |
| `--redirect` | Allow redirects | False |
| `--headers` | Custom headers as JSON string | None |
| `--data` | Request data as JSON string | None |
| `--response-type` | Response type (html, plaintext, markdown, png, jpeg, network, content) | html |
| `--content-types` | Content types to extract (comma-separated) | None |
| `--country` | Country code for proxy | ANY |
| `--proxy-url` | Custom proxy URL | None |
| `--js-render` | Enable JavaScript rendering | False |
| `--headless` | Run browser in headless mode | False |
| `--wait-selector` | Wait for element with this selector to appear | None |

**Output:** All commands return JSON objects with the scraped content or Cloudflare bypass results.

---

## Response Types

### HTML
Returns the HTML content of the page as an escaped string.

### Plaintext
Returns the plain text content of the page, removing all HTML tags.

### Markdown
Returns the page content formatted as Markdown for better readability.

### PNG/JPEG
Returns a base64 encoded string of the page screenshot.

### Network
Returns all network requests made during page load, including URLs, methods, status codes, and headers.

### Content
Returns specific content types extracted from the page, such as emails, phone numbers, headings, images, audios, videos, links, hashtags, metadata, tables, and favicon.

---

## Notes

⚠️ **Timeout Policy:**
- Page load timeout: 30 seconds
- Global execution timeout: 180 seconds

⚠️ **Supported CAPTCHAs:**
- reCaptcha V2
- Cloudflare Turnstile
- Cloudflare Challenge

⚠️ **Rate Limits:**
- 429 errors indicate rate limit exceeded. Reduce request frequency or upgrade plan.

⚠️ **Billing:**
- Charges are applied on a per-request basis
- Only successful requests will be billed