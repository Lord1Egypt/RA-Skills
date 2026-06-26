# sec-daily-digest

English is the primary README. Chinese version: [README.zh-CN.md](README.zh-CN.md).

`sec-daily-digest` fetches recent articles from CyberSecurityRSS OPML feeds **and Twitter/X security / AI KOL accounts**, scores and filters them (AI-first with rule fallback), deduplicates against historical archives, merges vulnerability events, monitors source health, and generates a bilingual daily markdown digest for cybersecurity researchers.

## 💬 One-Liner

Tell your AI assistant:

> **"Generate today's cybersecurity digest, focus on vulnerabilities and APT activity"**

The assistant fetches, scores, deduplicates, and renders a full Markdown report — hands-free.

More examples:

> 🗣️ "Use Claude to analyze today's security news, output to ./output/digest.md"

> 🗣️ "Generate this week's security roundup, skip Twitter, focus on CVEs"

> 🗣️ "Full-text enrichment with Gemini scoring, email to me@example.com"

Or via CLI:
```bash
bun scripts/sec-digest.ts --dry-run --output ./output/digest.md
```

## 📊 What You Get

An AI-scored, deduplicated cybersecurity digest from **dual data sources** (security RSS + Twitter/X researchers):

| Layer | Scale | Content |
|-------|-------|-------|
| 📡 RSS (tiny) | ~50 feeds | CyberSecurityRSS curated — vulns, threat intel, malware… |
| 📡 RSS (full) | 400+ feeds | Full CyberSecurityRSS OPML (`--opml full`) |
| 🐦 Twitter/X | 15 researchers | Tavis Ormandy, Brian Krebs, Kevin Beaumont, Marcus Hutchins… |

### Pipeline

```
RSS fetch + Twitter KOL fetch (parallel)
        ↓
  dedup + time filter → archive penalty (seen before −5)
        ↓
  full-text enrich (optional) → AI scoring + classification → AI summary + translation
        ↓
  vulnerability merge (CVE-first + semantic clustering)
        ↓
  render Markdown digest → email delivery (optional)
```

**Quality scoring**: priority source (+3), archive penalty (−5), keyword weights, recency.

## Highlights

- TypeScript + Bun runtime, no new npm dependencies
- **Dual source monitoring**: CyberSecurityRSS OPML + Twitter/X security KOLs (parallel fetch)
- **Historical dedup**: articles seen in the past 7 days receive a −5 score penalty; archive auto-cleans after 90 days
- **Source health monitoring**: tracks per-source fetch failures; surfaces unhealthy sources in digest footer
- **Full-text enrichment** (`--enrich`): fetches article body before AI scoring for better classification
- **Email delivery** (`--email`): sends digest via `gog`
- Mandatory OPML update check before each run
  - Default profile: `tiny.opml`
  - Optional profile: `CyberSecurityRSS.opml` (`--opml full`)
  - On remote check failure: continue with cached OPML
- Explicit provider selection: `--provider openai|gemini|claude|ollama` (default: `openai`)
- Balanced ranking: Security 50% + AI 50%
- Score display: `🔥N` (integer, 1–10 range)
- Vulnerability merge: CVE-first + semantic clustering fallback
- Output sections:
  - `## 📝 今日趋势` — macro trend highlights
  - `## 🔐 Security KOL Updates` — Twitter/X KOL tweets (when credentials present)
  - `## AI发展` — AI/LLM articles
  - `## 安全动态` — security articles
  - `## 漏洞专报` — merged vulnerability events
  - `## ⚠️ Source Health Warnings` — unhealthy sources (when detected)

## Config and State

Persistent directory: `~/.sec-daily-digest/` (override with `SEC_DAILY_DIGEST_HOME`)

| File / Directory | Description |
|-----------------|-------------|
| `config.yaml` | Main config (provider, hours, top_n, weights…) |
| `sources.yaml` | Twitter/X KOL list + custom RSS sources |
| `health.json` | Per-source fetch health history |
| `archive/YYYY-MM-DD.json` | Daily article archive for historical dedup |
| `twitter-id-cache.json` | Twitter user ID cache (official API only, 7-day TTL) |
| `opml/tiny.opml` | Cached tiny OPML |
| `opml/CyberSecurityRSS.opml` | Cached full OPML |

## Quick Start (CLI)

```bash
cd /path/to/sec-daily-digest
bun install

# Dry run (no AI, no Twitter)
bun scripts/sec-digest.ts --dry-run --output ./output/digest.md

# With AI scoring
OPENAI_API_KEY=sk-... bun scripts/sec-digest.ts \
  --provider openai --opml tiny --hours 48 --output ./output/digest.md

# With Twitter KOLs
TWITTERAPI_IO_KEY=your-key bun scripts/sec-digest.ts \
  --provider claude --output ./output/digest.md

# Weekly mode
bun scripts/sec-digest.ts --mode weekly --provider openai --output ./output/weekly.md

# Full-featured
TWITTERAPI_IO_KEY=your-key bun scripts/sec-digest.ts \
  --provider claude --enrich --email me@example.com \
  --output ./output/digest.md
```

## CLI Options

| Flag | Description | Default |
|------|-------------|---------|
| `--provider <id>` | `openai\|gemini\|claude\|ollama` | `openai` |
| `--opml <profile>` | `tiny\|full` | `tiny` |
| `--hours <n>` | Time window in hours | `48` |
| `--mode <daily\|weekly>` | Shortcut: daily=48h, weekly=168h | — |
| `--top-n <n>` | Max articles to select | `20` |
| `--output <path>` | Output markdown file path | `./output/sec-digest-YYYYMMDD.md` |
| `--dry-run` | Rule-based scoring only (no AI calls) | false |
| `--no-twitter` | Disable Twitter/X KOL fetching | false |
| `--email <addr>` | Send digest via `gog` | — |
| `--enrich` | Fetch full text before scoring | false |
| `--help` | Show help | — |

## Environment Variables

### AI Providers

**OpenAI** (default):
- `OPENAI_API_KEY` (required)
- `OPENAI_API_BASE` (optional)
- `OPENAI_MODEL` (optional)

**Gemini**:
- `GEMINI_API_KEY` (required)
- `GEMINI_MODEL` (optional)

**Claude**:
- `ANTHROPIC_API_KEY` (required)
- `CLAUDE_MODEL` (optional)
- `CLAUDE_API_BASE` (optional)

**Ollama**:
- `OLLAMA_API_BASE` (optional, default `http://127.0.0.1:11434`)
- `OLLAMA_MODEL` (optional)

### Twitter/X

| Variable | Description |
|----------|-------------|
| `TWITTERAPI_IO_KEY` | [twitterapi.io](https://twitterapi.io) key — preferred, 5 QPS |
| `X_BEARER_TOKEN` | Official Twitter API v2 bearer token |
| `TWITTER_API_BACKEND` | `twitterapiio\|official\|auto` (default: `auto`) |

Backend selection logic:
- `TWITTERAPI_IO_KEY` set → use twitterapi.io
- Only `X_BEARER_TOKEN` set → use official API
- Neither set → Twitter silently disabled (no crash)

### Other

| Variable | Description |
|----------|-------------|
| `SEC_DAILY_DIGEST_HOME` | Override state directory (default: `~/.sec-daily-digest`) |

## Configuring RSS Sources

RSS feeds come from CyberSecurityRSS OPML files (synced automatically). To add custom RSS sources on top of OPML, edit `~/.sec-daily-digest/sources.yaml`:

```yaml
sources:
  - id: my-blog
    type: rss
    name: "My Security Blog"
    url: "https://myblog.example.com/feed.xml"
    enabled: true
    priority: false
    topics:
      - security
    note: "Personal blog, check weekly"
```

### RSS Source Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique identifier across all sources. If it matches a default source ID, the entire default entry is replaced by this one. |
| `type` | `"rss"` | yes | Must be `"rss"` for RSS/Atom feed sources. |
| `name` | string | yes | Human-readable display name — shown in source attribution lines and health warning reports. |
| `url` | string | yes | Full URL of the RSS or Atom feed to fetch. |
| `enabled` | boolean | yes | Set to `false` to disable this source without deleting the entry. For default sources, a minimal `{id, enabled: false}` entry is sufficient. |
| `priority` | boolean | yes | If `true`, articles from this source receive a **+3 quality score bonus**, helping them surface above lower-priority sources with similar content. Use for high-signal feeds you always want represented. |
| `topics` | string[] | yes | Topic tags for metadata and categorization. Example values: `security`, `ai`, `exploit`, `malware`. Currently used for labeling; scoring is keyword-based. |
| `note` | string | no | Free-text description for your own reference. Not used in scoring or output. |

## Configuring Twitter/X KOL Accounts

On first run, `~/.sec-daily-digest/sources.yaml` is auto-created with 15 default security researchers (Tavis Ormandy, Brian Krebs, Kevin Beaumont, Marcus Hutchins, etc.).

### Disable a default account

Provide only `id` + `enabled: false` — no other fields needed:

```yaml
sources:
  - id: thegrugq
    enabled: false
```

### Add a new account

```yaml
sources:
  - id: myresearcher
    type: twitter
    name: "My Researcher"
    handle: myresearcher
    enabled: true
    priority: false
    topics:
      - security
    note: "Tracks APT campaigns"
```

### Replace a default account's config

Provide a full entry with the same `id` to override all fields:

```yaml
sources:
  - id: taviso
    type: twitter
    name: "Tavis Ormandy"
    handle: taviso
    enabled: true
    priority: true
    topics:
      - security
      - exploit
    note: "Google Project Zero"
```

### Twitter Source Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique identifier across all sources. Must not collide with RSS source IDs. If it matches a default Twitter source ID, the entire default entry is replaced. |
| `type` | `"twitter"` | yes | Must be `"twitter"` for Twitter/X account sources. |
| `name` | string | yes | Display name shown in the `🔐 Security KOL Updates` section of the digest. Can differ from the Twitter display name. |
| `handle` | string | yes | Twitter/X username **without** the `@` prefix. Example: `briankrebs` (not `@briankrebs`). |
| `enabled` | boolean | yes | Set to `false` to stop fetching this account. A minimal `{id, enabled: false}` entry disables a default source without needing all fields. |
| `priority` | boolean | yes | If `true`, tweets from this account receive a **+3 quality score bonus** in the article ranking pipeline. Useful for accounts whose tweets you always want in the AI发展 / 安全动态 sections. |
| `topics` | string[] | yes | Topic tags for metadata. Does not affect fetching — all tweets from an enabled account are fetched regardless. |
| `note` | string | no | Free-text description for your own reference. Not used in scoring or output. |

> **Merge behavior:** On each run, the default 15-account list is merged with your `sources.yaml`. Entries with matching `id` replace defaults; new `id`s are appended. This means new default accounts added in future releases will appear automatically — unless you explicitly disable them.

## Email Delivery

Requires [`gogcli`](https://github.com/steipete/gogcli) — a Gmail CLI that uses the official Gmail API:

```bash
# Install (macOS)
brew install steipete/tap/gogcli

# Authenticate (one-time)
gog auth login

# Send digest via email
bun scripts/sec-digest.ts --provider claude --email me@example.com --output ./output/digest.md
```

Under the hood, the `--email` flag calls:
```bash
gog gmail send --to <addr> --subject "sec-daily-digest YYYY-MM-DD" --body-file -
```

## cron Integration

```bash
# Daily at 07:00
0 7 * * * cd /path/to/sec-daily-digest && \
  bun scripts/sec-digest.ts --mode daily --output ~/digests/sec-$(date +\%Y\%m\%d).md \
  2>&1 | tee -a ~/.sec-daily-digest/cron.log

# Weekly on Monday at 08:00
0 8 * * 1 cd /path/to/sec-daily-digest && \
  bun scripts/sec-digest.ts --mode weekly --opml full \
  --output ~/digests/weekly-$(date +\%Y\%m\%d).md \
  2>&1 | tee -a ~/.sec-daily-digest/cron.log
```

## Install This Skill

Set source path:

```bash
SKILL_SRC="~/z3dev/Skills/sec-daily-digest"
```

### OpenClaw

```bash
clawhub install sec-daily-digest
```

### Claude Code

Install as a personal skill:

```bash
mkdir -p ~/.claude/skills
ln -sfn "$SKILL_SRC" ~/.claude/skills/sec-daily-digest
```

Or project-local:

```bash
mkdir -p ./.claude/skills
ln -sfn "$SKILL_SRC" ./.claude/skills/sec-daily-digest
```

### Codex

```bash
mkdir -p ~/.agents/skills
ln -sfn "$SKILL_SRC" ~/.agents/skills/sec-daily-digest
```

### OpenCode

User-level:

```bash
mkdir -p ~/.config/opencode/skills
ln -sfn "$SKILL_SRC" ~/.config/opencode/skills/sec-daily-digest
```

Project-level:

```bash
mkdir -p ./.opencode/skills
ln -sfn "$SKILL_SRC" ./.opencode/skills/sec-daily-digest
```

## Run as a Skill

```text
/sec-digest
```

## Tests

```bash
bun test
```
