---
name: seaportal
description: "Use this skill when an agent needs to read or navigate websites without a browser: fetch a page as clean Markdown, get a JSON accessibility snapshot of interactive elements, follow links across pages, or quickly decide whether a site is static/SSR (seaportal can handle it) vs SPA/blocked (needs a real browser like pinchtab). HTTP-only, fast (<2s), token-efficient. Prefer this over a browser whenever the page is static or server-rendered."
metadata:
  openclaw:
    requires:
      bins:
        - seaportal
    homepage: https://github.com/pinchtab/seaportal
    install:
      - kind: npm
        package: seaportal
        bins: [seaportal]
      - kind: go
        package: github.com/pinchtab/seaportal/cmd/seaportal@latest
        bins: [seaportal]
---

# Web Navigation with SeaPortal

CLI-first read-only web fetcher. Use the `seaportal` command. **No JavaScript execution** — for SPAs/blocked pages, escalate to a real browser.

## Core Commands

```bash
seaportal <url>                              # Markdown + frontmatter (also writes renders/seaportal/*.md, *.json)
seaportal --json <url>                       # Full Result struct as JSON
seaportal --xml <url>                        # TEI-Lite XML (teiHeader metadata + text/body content)
seaportal --snapshot <url>                   # Accessibility tree as JSON
seaportal --snapshot --format=compact <url>  # Accessibility tree as text (most token-efficient)
seaportal --snapshot --filter=interactive --format=compact <url>  # Only links/buttons/inputs
seaportal --max-tokens=2000 <url>            # Cap Markdown body size (paragraph-boundary cut, sets truncated:true)
seaportal --snapshot --max-tokens=2000 <url> # Cap snapshot tree size
seaportal --fast <url>                       # Bail early if browser is needed
seaportal --head-only <url>                  # 16 KB range fetch — metadata + canonical only, no body
seaportal --respect-robots <url>             # Consult robots.txt; refuse disallowed fetches
seaportal --rate-limit=500ms <url>           # Min interval between same-host requests
seaportal --probe-search <url>               # Override to needs-browser when search URL yields no results
seaportal --no-dedupe <url>                  # Disable repeated-block dedup
seaportal --no-prune-fallback <url>          # Disable the heuristic fallback when readability is thin
seaportal --with-links <url>                 # Add structured list of discovered <a> links to output
seaportal --with-images <url>                # Add structured list of discovered <img> entries to output
seaportal --with-tables <url>                # Add structured tables (caption/headers/rows) to output, layout tables flattened
seaportal --with-comments <url>              # Emit user-generated comments (Disqus/native) separately in result.comments (stripped from Content by default either way)
seaportal --links=text <url>                 # Markdown link retention: none|text|all|footer (default all)
seaportal --citations <url>                  # Synonym for --links=footer (back-compat)
seaportal --chunk=heading <url>              # Chunk Markdown by heading / sentence / window
seaportal --select=".main-content" <url>     # Scope extraction to a CSS subtree
seaportal --strip=".ads,.cookie-banner" <url> # Remove matching elements before extraction
seaportal --retries 5 <url>                  # Override default retry count (3)
seaportal --max-retry-wait 10s <url>         # Override single backoff cap (30s)
seaportal --retry-timeout 60s <url>          # Override total retry budget (90s)
seaportal --base-url=URL -                   # Read HTML from stdin; --base-url resolves relative links
seaportal --ua=googlebot <url>               # User-Agent preset or literal string
seaportal --proxy=http://user:pass@proxy:8080 <url>  # Route via HTTP(S) proxy
seaportal --cache=/tmp/sp-cache <url>        # Reuse fresh 200 OK responses from disk (opt-in; default TTL 24h)
seaportal --cache=/tmp/sp-cache --cache-stale-tolerance=5m <url>  # Stale-while-revalidate: serve stale within TTL+tolerance, refresh in background
seaportal --no-pdf <url>                     # Skip PDF extraction (default: extract PDF text)
seaportal --schema=path/to/schema.yaml <url> # Apply a CSS schema (JSON/YAML), populate result.schema
seaportal --query="compound interest" <url>  # BM25-rank H2/H3 sections by relevance, annotate result.rankedSections
seaportal --query=... --top-n=3 <url>        # Keep only the top-N most relevant sections in rankedSections
seaportal --query=... --top-n=3 --filter-by-query <url>  # Replace Content with concatenated top-N sections
seaportal --split-out=dir/ --split-bytes=32768 <url>  # Shard output across multiple files; print manifest (path\tindex/of\tbytes) to stdout
seaportal --version
```

## Subcommands

The default verb (no subcommand) is URL extraction — `seaportal <url>` behaves exactly as documented above.

- `seaportal sitemap <url>` — fetch a sitemap.xml, recurse into nested `<sitemapindex>` references, decompress `.gz`, and print one URL per line. Flags: `--json` (emit JSON array of `{loc,lastmod,changefreq,priority}` entries), `--max-urls N` (default 50000), `--max-depth N` (default 5), `--allow-internal` (permit trusted private/internal hosts). Example: `seaportal sitemap https://example.com/sitemap.xml --json`.
- `seaportal feed <url>` — fetch and parse RSS 2.0, Atom 1.0, or JSON Feed 1.x into a unified `{title, link, published, summary, author, guid}` shape (format sniffed from the root element / first byte). Default output is one TSV line per item (`published\ttitle\tlink`). Flags: `--json` (emit JSON array), `--max-items N` (default 200), `--allow-internal` (permit trusted private/internal hosts). Example: `seaportal feed https://example.com/feed.xml --json`.
- `seaportal mcp` — run as an MCP (Model Context Protocol) server over JSON-RPC 2.0 line-delimited stdio. Exposes four tools — `fetch_url`, `fetch_snapshot`, `parse_sitemap`, `parse_feed` — each routing to the library entry point of the same shape. No flags; configuration flows through MCP tool arguments. See **MCP integration** below.
- `seaportal help` — usage summary including subcommands.

## MCP integration

Register seaportal as an MCP server in your editor (Claude Desktop / Claude Code / Cursor) — example `claude_desktop_config.json`:

```jsonc
{
  "mcpServers": {
    "seaportal": {
      "command": "seaportal",
      "args": ["mcp"]
    }
  }
}
```

Tools exposed: `fetch_url` (`{url, dedupe?, fast?, with_links?, with_images?, with_tables?, with_comments?, max_tokens?}`), `fetch_snapshot` (`{url, filter?, max_tokens?, allow_internal?}`), `parse_sitemap` (`{url, max_depth?, max_urls?, allow_internal?}`), `parse_feed` (`{url, max_items?, allow_internal?}`). Each returns its library result as a single JSON text content block.

## User-Agent presets

`--ua=<name>` accepts curated presets; unknown values pass through as literal UA strings. Empty (default) sends a real Chrome UA. Per-host `DomainUserAgent` overrides still win.

- `chrome` (default), `safari`, `firefox` — real browser UAs
- `googlebot`, `bingbot`, `search-bot` — bot UAs (may trigger reverse-DNS challenges)
- `seaportal` — honest self-identify for cooperative sites

## Cache

`--cache=<dir>` is opt-in: only fresh 200 OK responses are stored, keyed by SHA-256 of URL + Accept/Accept-Language/User-Agent. `--cache-ttl=<dur>` controls freshness (default 24h). `--no-cache` bypasses reads but still writes — i.e. "force refresh". Errors / 3xx / 4xx / 5xx are never cached. Result includes `cacheHit: true` on a replay.

Past-TTL entries that carry `ETag` or `Last-Modified` are automatically re-validated with a conditional GET (`If-None-Match` / `If-Modified-Since`). A `304 Not Modified` replays the cached body, refreshes `FetchedAt`, and sets `cacheRevalidated: true` (distinct from `cacheHit`, which means "served from disk with no network call"). A `200` replaces the entry; other statuses leave the cache untouched.

`--cache-stale-tolerance=<dur>` enables stale-while-revalidate (SWR) semantics: entries whose age falls within `TTL + tolerance` are served immediately from disk (with `cacheStale: true`) while a background goroutine fires the conditional GET to refresh the entry for the next call. Default `0` keeps the existing synchronous-revalidate behaviour. The SWR band does not require validators on the cached entry — within tolerance the body is trusted unconditionally; beyond tolerance the existing validator-gated synchronous revalidation runs. `--no-cache` bypasses SWR entirely. Background refresh failures are silent and leave the stale entry intact for the next attempt.

## PDF extraction

`application/pdf` responses are extracted by default: text is pulled page-by-page via `ledongthuc/pdf` and flows through the same `Result.Content` Markdown pipeline (link retention, truncation, chunking, cache) with `ExtractionMethod="pdf"` and `--- page N ---` separators. Pass `--no-pdf` to restore the legacy "skipped binary content" behaviour. Image-only / scanned PDFs yield an empty extraction error (no OCR).

## HTTP transport

- HTTPS connections negotiate HTTP/2 via ALPN when the server offers `h2`;
  fall back to HTTP/1.1 otherwise.
- HTTP (no TLS) always uses HTTP/1.1.
- All HTTPS connections use a Chrome 122 TLS fingerprint via utls — bypasses
  Cloudflare's Go-default-TLS bot detection.
- The negotiated protocol is surfaced on `Result.protocol` (`"h2"` or
  `"http/1.1"`).

## Proxy support

`--proxy=URL` routes the fetch through a proxy. `http://` and `https://` proxy URLs are supported with Basic auth taken from the URL userinfo (`user:pass@host:port`). HTTPS targets use a CONNECT tunnel; the Chrome TLS fingerprint is preserved end-to-end with the origin. `socks5://` URLs work for HTTP target URLs only — HTTPS-over-SOCKS5 is a V1 limitation. Invalid proxy URLs fail fast with `result.Error = "invalid proxy URL: ..."`.

## Security defaults (local / internal URLs)

The CLI is **safe by default** (`DefaultSecurityPolicy`): it blocks targets that
resolve to private/internal IPs (SSRF guard), allows only `http`/`https`, caps
redirects at 10 with per-hop re-validation, and bounds the raw (50 MiB) and
decompressed (200 MiB) body.

- **Reading `localhost`, `127.0.0.1`, a `192.168.*`/`10.*` host, or any intranet
  URL fails by default** with `Error: target resolves to a private/internal IP`.
  Add **`--allow-internal`** to permit it (you are vouching the target is trusted).
- Other knobs: `--max-redirects N`, `--allow-domains` / `--deny-domains`,
  `--trusted-resolve-cidrs`, `--max-response-bytes`, `--max-decompressed-bytes`.
- The MCP server applies the same safe default to `fetch_url`, `fetch_snapshot`,
  `parse_sitemap`, and `parse_feed`.
- Caveats: with `--proxy` the dial-time rebinding check is skipped (the target is
  still vetted before fetch and on each redirect, just not at connect time).

## Per-host rate limiting

`--rate-limit=DURATION` enforces a minimum interval between requests to the same host. Useful primarily for library callers sharing a `HostRateLimiter` across calls via `Options.RateLimiter`; a single CLI invocation only fires one request, so the throttle has no cross-call effect by itself. Combines with `--respect-robots` crawl-delay (both apply; effective wait is their sum).

## Chunking

`--chunk=NAME[:SIZE[:OVERLAP]]` populates `result.chunks` (off by default). Runs after `--max-tokens` truncation; fenced code blocks are never split.

- `--chunk=heading` — split at H2/H3 boundaries; pre-heading prologue is its own chunk.
- `--chunk=sentence:512` — group sentences until ~512 tokens; heading inherited from nearest H2/H3 above.
- `--chunk=window:2000:200` — 2000-char windows, 200-char overlap, snapped to word boundaries.

## Query relevance

`--query="..."` scores each H2/H3-bounded Markdown section against the query with standard BM25 (k1=1.5, b=0.75) and populates `result.rankedSections` (descending score). Pure additive by default — `Content` is untouched. Combine with `--top-n=N` to truncate, or `--filter-by-query` to replace `Content` with the concatenated top-N sections (default top-3 when `--top-n` is unset). No stopwords/stemming in V1; IDF handles common words naturally.

- `seaportal --json --query="formula" <url>` — annotate all sections with scores.
- `seaportal --json --query="formula" --top-n=3 <url>` — keep only the 3 highest-scoring sections in `rankedSections`.
- `seaportal --query="formula" --top-n=3 --filter-by-query <url>` — Markdown body becomes just those 3 sections.

## Schema extraction

`--schema=<path>` applies a declarative CSS schema (JSON or YAML, format sniffed from extension) to the raw HTML and surfaces the result as `result.schema` in JSON output. Three modes per field: single value (`selector` only), multiple values (`multiple: true`), nested array of objects (`fields:` populated). Optional `attr:` reads an attribute instead of text. Runs on the pre-preprocess DOM so chrome elements (nav/sidebar) are reachable. Bad selectors or load failures become warnings, never crash. Example schema:

```yaml
fields:
  title: { selector: h1 }
  tags:  { selector: .tag, multiple: true }
  products:
    selector: .product
    fields:
      name:  { selector: .name }
      price: { selector: .price, attr: data-price }
```

Invoke: `seaportal --json --schema=./schema.yaml <url>`. XPath is a V2 limitation — CSS only for now.

## Chaining with a browser fetcher

When a page needs JS execution, let `pinchtab` (or any other fetcher) render the HTML, then pipe it into seaportal for extraction:

```bash
pinchtab fetch https://example.com | seaportal --base-url https://example.com --json -
```

`--base-url` is required in stdin mode. Network-only flags (`--head-only`, `--respect-robots`, `--retries`) are silently no-ops with a stderr warning.

## Workflow: navigating a site

1. **Fetch the entry point as Markdown**: `seaportal <url>`. Read the frontmatter — `pageClass`, `trustworthy`, `needsBrowser`, `confidence` tell you if extraction is reliable.
2. **Decide next step from `pageClass`**:
   - `static` / `ssr` / `hydrated` → trustworthy, keep using seaportal.
   - `spa` / `dynamic` → JS-only content, **stop and escalate to a browser** (pinchtab).
   - `blocked` → bot-protection or login wall, **escalate**.
3. **Discover links**: extract URLs from the Markdown body, OR run `seaportal --snapshot --filter=interactive --format=compact <url>` to see only links/buttons with their `href`s. Each entry has a stable `ref` (`e1`, `e2`…) and CSS `selector`.
4. **Follow a link**: take the `href`, resolve against the page URL if relative, and re-run `seaportal <new-url>`.
5. **Repeat** until you have what you need. Track visited URLs to avoid loops.

There is no session, no click, no form submit — every navigation is a fresh HTTP GET. To "click" a link you re-invoke seaportal on its `href`.

## Choosing output format

| Goal | Command |
|---|---|
| Read article / docs content | `seaportal <url>` (Markdown) |
| Programmatic decision-making | `seaportal --json <url>` |
| Map of page structure (cheap on tokens) | `seaportal --snapshot --format=compact <url>` |
| Just the actionable links/buttons | `seaportal --snapshot --filter=interactive --format=compact <url>` |
| Large page, must cap tokens | add `--max-tokens=2000` (caps snapshot tree in snapshot mode, or Markdown body otherwise; truncates at the latest paragraph boundary and sets `truncated: true`) |

Compact snapshot rows look like:
```
e2 link "Docs" <a> [interactive] href=/docs
e5 heading "Welcome" <h1> level=1
```

## Classification cheat sheet (when to escalate)

`pageClass` field in the frontmatter / JSON:

| Class | Action |
|---|---|
| `static` | Use seaportal — pure HTML, high confidence. |
| `ssr` | Use seaportal — server-rendered. |
| `hydrated` | Use seaportal — SSR + JS, usually fine. |
| `spa` | **Escalate** — JS-only, seaportal will return little/empty. |
| `dynamic` | **Escalate** — heavy client rendering. |
| `blocked` | **Escalate** — bot protection, captcha, or login wall. |

Also escalate if `needsBrowser: true` or `validationOk: false`. Use `--fast` when you want seaportal to bail early on any of these instead of doing full extraction.

For programmatic routing, prefer `profile.decision` + `profile.browserRecommended` over mapping `pageClass` yourself: one explicit decision (`static-high-confidence` / `static-ok` / `static-caution` / `browser-needed` / `blocked` / `unreachable` / `not-found` / `unsupported`), where `browserRecommended: true` means a real browser is likely to help. See docs/reference/browser-discriminator.md.

## Thin Markdown? Try the snapshot before escalating

If seaportal classified the page as `static`/`ssr`/`hydrated` (i.e. it thinks extraction succeeded) but the Markdown body looks thin — `length` < ~1500, no real paragraphs, mostly headings or naked links — **don't escalate yet**. Readability sometimes prunes link-heavy or table-heavy sections that the accessibility tree still has in full. Retry with:

```bash
seaportal --snapshot --format=compact <url>                    # whole structure
seaportal --snapshot --filter=interactive --format=compact <url>  # just links/buttons
```

If the snapshot returns substantial nodes, use those. If the snapshot is also thin, *then* escalate. Canonical situations where the fallback is worth a try: government index pages (`usa.gov`, `gov.uk`) where the link set is the content, and reference/listing pages where the prose is incidental to the structure. Don't loop — one snapshot retry is enough; if it's not there, it's not coming.

For search URLs specifically, `--probe-search` short-circuits CNN/DDG-style JS search shells with reason `client-rendered-search` — when set, seaportal flips outcome to `needs-browser` if a search-shaped URL returns a short body with no result-list structure.

## Output side-effects

The default Markdown mode (no flag) **also writes two files** under `./renders/seaportal/<domain>_<timestamp>.{md,json}` from the working directory. If running from a directory where that's unwanted, use `--json` or `--snapshot` instead — those only print to stdout.

## TEI-Lite XML output (`--xml`)

`--xml` emits a TEI-Lite-shaped document: `<teiHeader>` with title/author/published-date/language/source URL, plus `<text><body>` containing the Markdown converted into `<head>`, `<list>`/`<item>`, `<code>`, and `<p>` elements. Mutually exclusive with `--json` (exit 2). Scope is basic structural shaping — full TEI ODD validation, footnotes, and cross-references are out of scope.

## Output splitting

`--split-out=<dir>` shards the rendered output into multiple files under `<dir>`, capped at `--split-bytes` (default `--max-tokens × 4` or 32 KB). Prefers existing `--chunk` boundaries; otherwise splits on paragraph boundaries. Files are named `<url-slug>-NNN.{md,json}` and written atomically (`.tmp` + rename). Stdout receives a TSV manifest (`path\tindex/of\tbytes`) instead of the content body. Not supported with `--xml`.

## What this skill is NOT

- Not a browser. No JS execution, no clicks, no form fills, no cookies/sessions.
- Not stateful. Each call is independent.
- For interactive flows, multi-step forms, or auth — use the `pinchtab` skill instead. A common pattern is: **seaportal first, pinchtab on escalation.**
