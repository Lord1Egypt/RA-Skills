---
name: siteone-crawler
description: >
  Website crawling, auditing, offline cloning, and markdown export using SiteOne Crawler (Rust).
  Trigger when the user asks to: crawl a website, audit/analyze a site for SEO/security/performance/accessibility,
  generate an HTML audit report, clone a website for offline browsing, export a website to markdown,
  generate a sitemap, stress/load test a site, or run a CI/CD quality gate check.
  Binary path: ~/.siteone-crawler/siteone-crawler
---

# SiteOne Crawler

Cross-platform website crawler/analyzer written in Rust.

## Setup (run once)

Before first use, ensure the binary exists. If not found, install it automatically:

1. Check if binary exists at the paths below (in order of priority):
   - `$HOME/.siteone-crawler/siteone-crawler`
   - Any `siteone-crawler` found in `$PATH` (via `which siteone-crawler`)
2. If neither exists, download the latest release from GitHub:
   ```bash
   INSTALL_DIR="$HOME/.siteone-crawler"
   mkdir -p "$INSTALL_DIR"
   # Detect OS/arch
   OS=$(uname -s | tr '[:upper:]' '[:lower:]')
   ARCH=$(uname -m)
   case "$ARCH" in x86_64) ARCH="x64" ;; aarch64|arm64) ARCH="arm64" ;; esac
   # Get latest release URL from GitHub API
   RELEASE_URL=$(curl -sL https://api.github.com/repos/janreges/siteone-crawler/releases/latest \
     | grep -oP "browser_download_url.*?${OS}-${ARCH}\.zip" | head -1 | sed 's/browser_download_url": "//')
   curl -sL "$RELEASE_URL" -o /tmp/siteone-crawler.zip \
     && unzip -o /tmp/siteone-crawler.zip -d /tmp/siteone-crawler \
     && mv /tmp/siteone-crawler/siteone-crawler "$INSTALL_DIR/" \
     && chmod +x "$INSTALL_DIR/siteone-crawler" \
     && rm -rf /tmp/siteone-crawler /tmp/siteone-crawler.zip
   ```
3. After installation, set `CRAWLER` to the resolved path and verify with `$CRAWLER --version`.

## Binary

```bash
CRAWLER="$HOME/.siteone-crawler/siteone-crawler"
```

If the above path doesn't exist, fall back to `$(which siteone-crawler)` after running Setup.

Always use the resolved path. The binary outputs colored text to terminal; use `--no-color` for script/pipeline usage and `--output json` for programmatic consumption.

## Common Workflows

### 1. Quick Audit (HTML report)

```bash
$CRAWLER --url="https://example.com" --output-html-report="/path/to/report.html"
```

Generates a self-contained interactive HTML audit report with quality scores (0.0-10.0) across Performance, SEO, Security, Accessibility, Best Practices.

### 2. Full Audit + JSON + Upload

```bash
$CRAWLER --url="https://example.com" \
  --output-html-report="/path/to/report.html" \
  --output-json-file="/path/to/result.json" \
  --upload --upload-retention="7d"
```

### 3. Offline Clone

```bash
$CRAWLER --url="https://example.com" --offline-export-dir="/path/to/offline-site" --disable-javascript
```

Use `--disable-javascript` for SPA/React sites to get a browsable static version. Use `--allowed-domain-for-external-files="*"` to include CDN assets.

### 4. Markdown Export

Multi-file (browsable):
```bash
$CRAWLER --url="https://example.com" --markdown-export-dir="/path/to/md-export"
```

Single-file (ideal for AI tools):
```bash
$CRAWLER --url="https://example.com" --markdown-export-dir="/tmp/md" --markdown-export-single-file="/path/to/site.md" \
  --markdown-disable-images --markdown-disable-files
```

### 5. Sitemap Generation

```bash
$CRAWLER --url="https://example.com" --sitemap-xml-file="/path/to/sitemap" --sitemap-txt-file="/path/to/sitemap"
```

### 6. CI/CD Quality Gate

```bash
$CRAWLER --url="https://example.com" --ci --ci-min-score="7.0" --ci-max-404="0" --ci-max-5xx="0"
```

Exit code 10 if thresholds not met. See references/cli-params.md for all `--ci-*` options.

### 7. Stress/Load Test

```bash
$CRAWLER --url="https://example.com" --workers="20" --max-reqs-per-sec="100" --max-depth="1"
```

**Warning**: high worker counts can cause DoS. Use with caution.

### 8. Single Page Crawl

```bash
$CRAWLER --url="https://example.com/about" --single-page --output-json-file="/path/to/result.json"
```

### 9. HTML-to-Markdown (local file)

```bash
$CRAWLER --html-to-markdown="/path/to/page.html" --html-to-markdown-output="/path/to/page.md"
```

### 10. Browse Exported Content

```bash
$CRAWLER --serve-markdown="/path/to/md-export" --serve-port="8321"
$CRAWLER --serve-offline="/path/to/offline-site" --serve-port="8321"
```

## Key Parameters Reference

See `references/cli-params.md` for the complete parameter reference organized by category.

### Most-used flags

| Flag | Purpose | Default |
|------|---------|---------|
| `--url` | Target URL (required) | - |
| `--output` | `text` or `json` | text |
| `--workers` | Concurrent threads | 3 |
| `--max-reqs-per-sec` | Requests per second limit | 10 |
| `--max-depth` | Crawl depth (0 = unlimited) | 0 |
| `--timeout` | Request timeout in seconds | 5 |
| `--no-color` | Disable colors | off |
| `--ignore-robots-txt` | Ignore robots.txt | off |

### Resource filtering

| Flag | Effect |
|------|--------|
| `--disable-all-assets` | Only crawl pages |
| `--disable-javascript` | No JS (recommended for offline/SPA) |
| `--disable-images` | No images |
| `--disable-styles` | No CSS |
| `--disable-files` | No downloadable docs |

### URL filtering

| Flag | Effect |
|------|--------|
| `--include-regex` | PCRE regex to include URLs |
| `--ignore-regex` | PCRE regex to skip URLs |
| `--allowed-domain-for-crawling` | Allow cross-domain crawling |
| `--allowed-domain-for-external-files` | Allow external asset domains |

## Script Helpers

### `scripts/audit.sh` — Quick audit wrapper

Runs a full crawl with HTML report and optional JSON output. See script for usage.

### `scripts/export-markdown.sh` — Markdown export wrapper

Exports a website to markdown (single or multi-file). See script for usage.

## Tips

- For modern JS frameworks (Next.js, React, Vue), add `--disable-javascript` when doing offline exports
- Use `--output json` for programmatic processing; JSON goes to STDOUT, progress to STDERR
- Use `--extra-columns="Title,Keywords,Description"` to add SEO columns
- Use `--timezone="Asia/Shanghai"` for local timestamps
- For large sites, increase `--memory-limit`, `--max-visited-urls`, and `--max-queue-length`
- Use `--resolve` to test local/dev servers (like curl --resolve)
- HTML reports are self-contained — open in any browser, no server needed
