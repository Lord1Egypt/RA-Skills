---
name: unified-search
description: Unified web search + deep research suite. Default ordinary /unified_search queries route to deep search-layer mode (Exa + Tavily + Grok); the legacy merged three-engine search (Tavily + Exa + Google) remains available via --legacy or the legacy subcommand. Use when user asks for “综合搜索”, “三搜索”, “三引擎”, “/unified_search”, deep search, issue/PR thread tracing, content extraction, or URL→Markdown conversion.
---

# Unified Search

This skill is now a **two-layer search suite**:

1. **Vendored deep-research stack** — now the default for ordinary `/unified_search <query>` calls
   - `search-layer`: Exa + Tavily + Grok multi-source search with intent-aware scoring
   - `fetch-thread`: deep thread / issue / PR / forum context extraction
   - `content-extract`: URL → Markdown with MinerU fallback
   - `mineru-extract`: official MinerU parsing wrapper
2. **Legacy merged search** — available via `--legacy` or the explicit `legacy` subcommand
   - Engines: **Tavily + Exa + Google**
   - Best for: quick fact-checks, troubleshooting, product/doc lookup, fast aggregated evidence

## Recommended usage policy

### A. Everyday search: default to deep search-layer

Run:

```bash
bash scripts/unified-search.sh "<query>"
```

This routes ordinary lookup queries to `search-layer` deep mode by default. Use `--legacy` or the `legacy` subcommand when the old Tavily + Exa + Google merged output is specifically needed.

Examples:

```bash
bash scripts/unified-search.sh "tavily language filter"
bash scripts/unified-search.sh "OpenClaw cron run docs"
bash scripts/unified-search.sh --legacy "OpenClaw cron run docs" --topic news --days 7
```

Chat trigger examples:
- `/unified_search tavily docs language filter`
- `/unified_search OpenClaw cron run docs`
- `/unified_search --legacy OpenClaw cron run docs --topic news --days 7`

### B. Explicit deep research: route to vendored search-layer

Run:

```bash
bash scripts/unified-search.sh search-layer "<query>" --mode deep --intent status --num 5
```

Examples:

```bash
bash scripts/unified-search.sh search-layer "OpenClaw config validation bug" --mode deep --intent status --extract-refs
bash scripts/unified-search.sh search-layer --queries "Bun vs Deno" "Bun advantages" "Deno advantages" --mode deep --intent comparison --num 5
bash scripts/unified-search.sh "RAG framework comparison" --mode deep --intent comparison --num 5
```

If `--mode / --intent / --freshness / --source / --extract-refs / --extract-refs-urls / --domain-boost` appears, the unified wrapper auto-routes to deep-search mode.

### C. Thread / issue / PR deep fetch

Run:

```bash
bash scripts/unified-search.sh fetch-thread "https://github.com/owner/repo/issues/123"
```

Examples:

```bash
bash scripts/unified-search.sh fetch-thread "https://github.com/owner/repo/issues/123" --format markdown
bash scripts/unified-search.sh fetch-thread "https://news.ycombinator.com/item?id=43197966"
```

### D. URL → Markdown extraction

Run:

```bash
bash scripts/unified-search.sh content-extract --url "https://mp.weixin.qq.com/s/example"
```

### E. MinerU direct parsing

Run:

```bash
bash scripts/unified-search.sh mineru-extract "https://example.com/file.pdf"
bash scripts/unified-search.sh mineru-parse-documents --file-sources "https://example.com/file.pdf"
```

## Wrapper subcommands

### 1) Default deep search-layer

```bash
bash scripts/unified-search.sh "<query>"
```

Ordinary queries now default to search-layer deep mode. Legacy parameters are only for `--legacy` or the explicit `legacy` subcommand:
- `--num`: max results per engine (default `5`)
- `--topic`: `general` or `news` (default `general`)
- `--days`: only for recent-news style queries
- `--save-run`: save output to custom dir
- `--json`: emit `summary.json`
- `--legacy`: force old Tavily + Exa + Google merged behavior

### 2) search-layer

```bash
bash scripts/unified-search.sh search-layer ...
```

Important parameters:
- `--mode fast|deep|answer`
- `--intent factual|status|comparison|tutorial|exploratory|news|resource`
- `--freshness pd|pw|pm|py`
- `--queries ...`
- `--domain-boost github.com,stackoverflow.com`
- `--source exa,tavily,grok,tinyfish`
- `--extract-refs`
- `--extract-refs-urls`

### 3) fetch-thread

```bash
bash scripts/unified-search.sh fetch-thread <url> [--format json|markdown] [--extract-refs-only]
```

### 4) content-extract

```bash
bash scripts/unified-search.sh content-extract --url <url>
```

### 5) mineru-extract / mineru-parse-documents

```bash
bash scripts/unified-search.sh mineru-extract <url> [--model MinerU-HTML]
bash scripts/unified-search.sh mineru-parse-documents --file-sources "<URL1>\n<URL2>"
```

## Environment / dependency notes

### Existing legacy search
- Tavily key: usually from `~/.openclaw/openclaw.json -> skills.entries.tavily.apiKey`
- Exa key: existing local setup / env override
- Google leg: depends on installed `google-search` skill

### Vendored deep-search stack
Preferred credentials file:

```json
{
  "exa": "your-exa-key",
  "tavily": "your-tavily-key",
  "grok": {
    "apiUrl": "https://api.x.ai/v1",
    "apiKey": "your-grok-key",
    "model": "grok-4.20-multi-agent-xhigh"
  },
  "tinyfish": {
    "apiKey": "your-tinyfish-key",
    "apiUrl": "https://api.search.tinyfish.ai"
  }
}
```

Location:

```bash
~/.openclaw/credentials/search.json
```

Optional env overrides:

```bash
export EXA_API_KEY="..."
export TAVILY_API_KEY="..."
export GROK_API_URL="https://api.x.ai/v1"
export GROK_API_KEY="..."
export GROK_MODEL="grok-4.20-multi-agent-0309"
export TINYFISH_API_KEY="..."
export TINYFISH_API_URL="https://api.search.tinyfish.ai"
export GITHUB_TOKEN="..."   # improves GitHub issue/PR thread fetch limits
export MINERU_TOKEN="..."   # required for MinerU parsing
```

### Local Python runtime
This skill now uses a dedicated venv:

```bash
.venv（local virtualenv, create with: python3 -m venv .venv）
```

Installed there:
- `requests`
- `trafilatura`
- `beautifulsoup4`
- `lxml`

## Important constraints

- The vendored `search-layer` script can directly use **Exa + Tavily + Grok + TinyFish**.
- The original upstream README also references **Brave via OpenClaw built-in `web_search`**, but shell scripts themselves cannot call agent-only tools. So in pure CLI mode, Brave is not auto-executed by the wrapper.
- Your original **Google-backed merged search** is preserved as the day-to-day aggregated search path.
- `content-extract` and `mineru-*` require external accessibility and, for MinerU, a valid `MINERU_TOKEN`.

## Vendored source snapshot

The upstream implementation is vendored here:

```bash
vendor/openclaw-search-skills/
```

Key vendored modules:
- `search-layer/`
- `content-extract/`
- `mineru-extract/`

## Output pattern

### Legacy merged search
1. Keep raw engine blocks (Tavily / Exa / Google)
2. Deduplicate overlapping links
3. Report:
   - consensus findings
   - disagreements / uncertainty
   - actionable next step

### Deep-search / extraction flows
Return the native structured JSON / markdown contract from the vendored tool whenever possible, then summarize with:
- direct conclusion
- strongest supporting sources
- uncertainty / conflicts
- next recommended trace or extraction step

For concise reporting template, read `references/report-template.md`.
