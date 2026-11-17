# Smart Scraper

Extract structured data from websites with integrated security protections. Supports tables, lists, prices, articles, metadata extraction, plus change monitoring with structured diffs.

**Security-first design**:
- SSRF protection: blocks private IPs, cloud metadata endpoints, dangerous URL schemes
- Cache is **disabled by default** (opt-in via `--cache` flag)
- Redirect validation prevents SSRF bypass attacks
- Rate-limited requests (100ms minimum interval)
- No dynamic code execution (no `eval`, no `execSync`, no arbitrary `require`)
- Bounded regex: all HTML pattern matching has content length limits

**Cache behavior**:
- Disk caching is **opt-in** — use `--cache` flag to enable
- Default: every request fetches fresh data
- Cache TTL: 5 minutes, max 50 entries, max 10MB total
- Cache location: `memory/scraper-cache/cache.json` (in workspace)
- Privacy warning displayed when caching is activated
- When cache is disabled, no persistent data is written to disk during `--extract`

## ⚠️ Important Warnings

### Watch Mode Persistence
`--watch <url>` writes data to disk regardless of cache setting:
- Baseline snapshots are saved per-watched-URL
- Diff results are stored on each poll interval
- These files persist until manually deleted

### HTTP Connections
This tool allows both `http://` and `https://` URLs. HTTP connections transmit data in cleartext over the network.
- Prefer HTTPS for sensitive scraping targets
- HTTP responses may be intercepted or modified in transit
- SSRF protection applies to both protocols

**Usage modes**:
- `--extract <url>` — extract structured data (tables, lists, prices, articles, or all)
- `--parse <html>` — parse raw HTML and display structure
- `--watch <url>` — monitor for content changes with baseline comparison
- `--status` — show cache statistics

**Programmatic API**: All functions exported as `module.exports` for testability.
