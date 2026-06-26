---
name: sec-daily-digest
version: "0.2.0"
description: "Use when asked to generate a cybersecurity daily digest from CyberSecurityRSS OPML feeds and Twitter/X KOL accounts, with provider selection, recent-window filtering, archive dedup, vulnerability merging, source health monitoring, and markdown output."
env:
  # AI providers (one required for non-dry-run)
  OPENAI_API_KEY: OpenAI provider key
  GEMINI_API_KEY: Google Gemini provider key
  ANTHROPIC_API_KEY: Anthropic Claude provider key
  OLLAMA_BASE_URL: Ollama base URL (optional, defaults to http://localhost:11434)
  # Twitter/X sources (optional; at least one enables KOL section)
  TWITTERAPI_IO_KEY: twitterapi.io API key (preferred)
  X_BEARER_TOKEN: Official Twitter API v2 bearer token
  TWITTER_API_BACKEND: "twitterapiio|official|auto" (default: auto)
  # State directory
  SEC_DAILY_DIGEST_HOME: Custom state root (default: ~/.sec-daily-digest)
---

# Sec Daily Digest

Generate a daily cybersecurity digest for researchers from CyberSecurityRSS OPML feeds and Twitter/X security KOL accounts.
Trigger command: `/sec-digest`.

## When to Use

- The user asks for a daily or latest cybersecurity digest.
- The user needs balanced AI + security coverage from RSS feeds.
- The user wants Twitter/X KOL security updates alongside RSS content.
- The task needs merged vulnerability events (CVE-first + non-CVE clustering).
- The user requests provider control (`openai|gemini|claude|ollama`) or `--dry-run`.

## When Not to Use

- The user wants ad-hoc one-off article summaries (use direct summarization instead).
- The user expects arbitrary output language switching.

## Quick Start

```bash
# Basic (RSS only, no AI scoring)
bun scripts/sec-digest.ts --dry-run --output ./output/digest.md

# With AI scoring + Twitter KOLs
TWITTERAPI_IO_KEY=your-key bun scripts/sec-digest.ts \
  --provider claude --opml tiny --hours 48 --output ./output/digest.md

# Weekly mode (168h window)
bun scripts/sec-digest.ts --mode weekly --provider openai --output ./output/weekly.md

# With email delivery (requires gog)
bun scripts/sec-digest.ts --provider claude --email me@example.com --output ./output/digest.md

# With full text enrichment
bun scripts/sec-digest.ts --provider claude --enrich --output ./output/digest.md
```

## CLI Flags Reference

| Flag | Description | Default |
|------|-------------|---------|
| `--provider <id>` | AI provider: `openai\|gemini\|claude\|ollama` | `openai` |
| `--opml <profile>` | OPML profile: `tiny\|full` | `tiny` |
| `--hours <n>` | Time window in hours | `48` |
| `--mode <daily\|weekly>` | Shortcut: daily=48h, weekly=168h | — |
| `--top-n <n>` | Max articles to select | `20` |
| `--output <path>` | Output markdown file path | `./output/sec-digest-YYYYMMDD.md` |
| `--dry-run` | Rule-based scoring only (no AI calls) | false |
| `--no-twitter` | Disable Twitter/X KOL fetching | false |
| `--email <addr>` | Send digest via `gog` to address | — |
| `--enrich` | Fetch full text for articles | false |
| `--help` | Show help | — |

## Quick Reference

- Entrypoint: `scripts/sec-digest.ts`
- Pipeline: `src/pipeline/run.ts`
- Config root: `~/.sec-daily-digest/`
- Config file: `~/.sec-daily-digest/config.yaml`
- Sources file: `~/.sec-daily-digest/sources.yaml`
- Health file: `~/.sec-daily-digest/health.json`
- Archive dir: `~/.sec-daily-digest/archive/`
- OPML cache (tiny): `~/.sec-daily-digest/opml/tiny.opml`
- OPML cache (full): `~/.sec-daily-digest/opml/CyberSecurityRSS.opml`

## Required Behavior

1. Always perform OPML remote update check before feed parsing.
2. If OPML remote check fails, use local cache only when cache exists.
3. If remote check fails and no local cache exists, fail fast (`No cached OPML available and remote update check failed.`).
4. Provider defaults to `openai`; explicit `--provider` overrides config.
5. Ranking uses balanced weights (Security + AI, default `0.5/0.5`).
6. Output sections must include `AI发展`, `安全动态`, and `漏洞专报`.
7. `output_language` exists in config, but current implementation outputs fixed bilingual-style markdown; do not assume runtime language switching.
8. Twitter KOL section (`🔐 Security KOL Updates`) appears only when tweets are fetched.
9. Twitter fetch is silently skipped (no crash) when no credentials are present.

## Twitter/X Configuration

Twitter KOL accounts are configured in `~/.sec-daily-digest/sources.yaml` (auto-created on first run with 15 default security researchers).

### Default KOL List

Taviso, GossiTheDog, SwiftOnSecurity, MalwareTechBlog, briankrebs, JohnLaTwC, and 9 others.

### sources.yaml Format

```yaml
sources:
  - id: taviso
    type: twitter
    name: "Tavis Ormandy / Google Project Zero"
    handle: taviso
    enabled: true
    priority: true
    topics:
      - security

  # Disable a default source:
  - id: thegrugq
    enabled: false

  # Add a new custom source:
  - id: myresearcher
    type: twitter
    name: "My Researcher"
    handle: myresearcher
    enabled: true
    priority: false
    topics:
      - security
```

### Backend Selection

| Env Var Set | Backend Used |
|-------------|-------------|
| `TWITTERAPI_IO_KEY` | twitterapi.io (preferred, 5 QPS) |
| `X_BEARER_TOKEN` only | Official Twitter API v2 (5 concurrent) |
| Both | twitterapi.io |
| Neither | Twitter disabled (silent) |
| `TWITTER_API_BACKEND=official` | Force official API |

## Archive (Historical Dedup)

Articles seen in the past 7 days receive a −5 score penalty (not removed, just deprioritized). Archive files are stored in `~/.sec-daily-digest/archive/YYYY-MM-DD.json` and automatically cleaned after 90 days.

## Source Health Monitoring

Each run records fetch success/failure for every source. Sources failing >50% of checks (with ≥2 checks) appear in a `⚠️ Source Health Warnings` section at the bottom of the digest. Health data lives in `~/.sec-daily-digest/health.json`.

## Email Delivery (gog)

The `--email` flag sends the digest via [`gogcli`](https://github.com/steipete/gogcli):

```bash
# Install (macOS)
brew install steipete/tap/gogcli
gog auth login   # one-time OAuth setup

# Send digest
bun scripts/sec-digest.ts --provider claude \
  --email me@example.com --output /tmp/digest.md
```

Log output:
```
[sec-digest] email=sent to me@example.com
# or
[sec-digest] email=failed: gog not found in PATH. Install: ...
```

## Full Text Enrichment

`--enrich` fetches article full text before AI scoring (improves classification and summarization quality). Skips paywalled/social domains (Twitter, Reddit, GitHub, YouTube, NYT, Bloomberg, WSJ, FT).

## cron Integration

```bash
# Daily at 07:00
0 7 * * * cd /path/to/sec-daily-digest && \
  bun scripts/sec-digest.ts --mode daily --output ~/digests/sec-$(date +\%Y\%m\%d).md \
  2>&1 | tee -a ~/.sec-daily-digest/cron.log

# Weekly on Monday at 08:00
0 8 * * 1 cd /path/to/sec-daily-digest && \
  bun scripts/sec-digest.ts --mode weekly --output ~/digests/weekly-$(date +\%Y\%m\%d).md \
  2>&1 | tee -a ~/.sec-daily-digest/cron.log
```

## Common Mistakes

1. Missing API key for selected provider (`OPENAI_API_KEY is required`, `GEMINI_API_KEY is required`, `ANTHROPIC_API_KEY is required`).
2. Misreading fallback behavior: OPML fallback is cache-dependent, not unconditional.
3. Forgetting `--dry-run` when no provider credentials are available.
4. Expecting Twitter KOLs without setting `TWITTERAPI_IO_KEY` or `X_BEARER_TOKEN`.

## Success Signals

1. Logs include `[sec-digest] provider=...`, `[sec-digest] cache_fallback=true|false`, `[sec-digest] output=...`, and `[sec-digest] stats feeds=... articles=... recent=... selected=... vuln_events=... twitter_kols=...`.
2. Output markdown contains the three required sections and vulnerability references.
3. `~/.sec-daily-digest/archive/YYYY-MM-DD.json` is written after each run.
4. `~/.sec-daily-digest/health.json` is updated after each run.

## More Detail

For full installation and extended usage notes, see `README.md` and `README.zh-CN.md`.
