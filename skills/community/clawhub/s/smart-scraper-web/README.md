# Smart Scraper — Structured Web Data Extraction

Extract structured data from websites with zero external dependencies. Built-in SSRF protection, rate limiting, caching, and change monitoring.

## Features

- **Extraction modes**: tables, lists, prices, articles, metadata, or everything
- **HTML parsing**: title, headings (h1–h6), paragraphs, links, images, tables, lists, prices, meta tags
- **Change monitoring**: watch URLs for content changes with diff output
- **Security**: SSRF blocklist, URL validation, redirect limits, rate limiting
- **Caching**: optional disk cache with TTL, size limits, and eviction
- **Zero dependencies**: uses only Node.js built-in modules

## Usage

```bash
# Extract structured data from a URL
node smart-scraper.js --extract https://example.com
node smart-scraper.js --extract --all https://example.com

# Extract specific content types
node smart-scraper.js --extract --table https://example.com
node smart-scraper.js --extract --list https://example.com
node smart-scraper.js --extract --price https://example.com
node smart-scraper.js --extract --article https://example.com

# Parse raw HTML
node smart-scraper.js --parse "<html><title>Hello</title></html>"

# Change monitoring
node smart-scraper.js --watch https://example.com           # First run: capture baseline
node smart-scraper.js --watch https://example.com            # Second run: compare
node smart-scraper.js --watch https://example.com --interval 300  # Poll every 5 min
node smart-scraper.js --watch https://example.com --alert-on-change  # CI mode

# Cache control
node smart-scraper.js --extract https://example.com --cache  # Enable disk caching
node smart-scraper.js --extract https://example.com --no-cache  # Disable caching

# Status
node smart-scraper.js --status
```

## API (for programmatic use)

```javascript
const SS = require('./smart-scraper.js');

// URL validation
const result = SS.validateUrl('https://example.com');
console.log(result.valid); // true

// Parse HTML
const data = SS.parseHtml('<html>...</html>');
console.log(data.title, data.headings, data.paragraphs);

// Extract from URL (async)
const extracted = await SS.extractFromUrl('https://example.com');

// Diff two snapshots
const changes = SS.diffSnapshots(oldData, newData);

// Watch mode (async)
const exitCode = await SS.watchMode(url, interval, alertOnChange, diffOnly);
```

## Security

- **SSRF protection**: blocks private IPs, localhost, cloud metadata endpoints
- **Blocked schemes**: `file:`, `gopher:`, `data:`, `javascript:`, `ftp:`
- **Redirect validation**: re-validates redirect targets to prevent SSRF bypass
- **Rate limiting**: 100ms minimum delay between requests
- **Cache opt-in**: disk caching is disabled by default; requires `--cache` flag
- **No dynamic evaluation**: no `eval()`, no `execSync()`, no `require()` of user input
- **Bounded regex**: content length limits on all HTML regex operations

## Testing

```bash
node test/run-tests.js
```

Runs 36 tests covering URL validation, HTML parsing, byte formatting, snapshot management, utility functions, CLI integration, and SSRF protection.

## Installation

```bash
# Via ClawHub
clawhub install smart-scraper-web
```

## Changelog

- **v1.3.1**: Fix SKILL.md cache documentation; resolve ClawHub audit findings
- **v1.3.0**: Add SSRF protection, redirect validation, rate limiting
- **v1.2.0**: Add cache controls, improved error handling
- **v1.1.0**: Add extraction modes (table, list, price, article, all)
- **v1.0.0**: Initial release with `--watch` change monitoring

## License

MIT-0 — Free to use, modify, and redistribute. No attribution required.
