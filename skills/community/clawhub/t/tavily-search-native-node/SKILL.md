---
name: tavily-search-native-node
description: Minimal Tavily web search for OpenClaw - native Node.js, zero dependencies, small audit surface. Use when the user asks to search the web, look up current information, find news, research a topic, check recent events, compare options, or get real-time data. Returns summarized, AI-optimized results with source citations. Requires TAVILY_API_KEY in the process environment. NOT for scraping individual URLs; use the platform URL-fetch/read tool when available. For caching, raw content, extract endpoint, and usage stats, use a separately reviewed Pro Tavily skill/package when available.
version: 1.0.11
risk_class: external-research-api-credit-usage
---

# Tavily Search (Native Node)

Minimal, auditable Tavily web search.

Version: 1.0.11 / publishable utility.

Native Node.js. Zero dependencies. Small runtime footprint and small audit surface.

## Security behavior

- Reads `TAVILY_API_KEY` from the process environment only.
- Does not read credential files or `~/.openclaw/.env`.
- Sends only the search request/options to `https://api.tavily.com/search`; tests may override the endpoint with `TAVILY_TEST_ENDPOINT` for local no-credit regression checks only.
- Does not write files, cache responses, write logs, transmit local files, or print the API key. The query appears in stdout output so users can verify what was searched; redact stdout before sharing externally when the query is sensitive.
- Do not search secrets, client identifiers, ticket contents, filenames, hostnames, confidential incident text, or private strategy unless the user explicitly approves sending that query to Tavily.


## When to use

Trigger phrases: "search for", "look up", "what's the latest on", "find recent news about", "research", "compare", "current info on".

**Use this when:**
- The user needs information past the model's training cutoff
- Current events, news, market data, prices, weather context, recent releases
- Research that needs citations the user can verify

**Do NOT use this when:**
- The user gives a specific URL to read -> use the platform URL-fetch/read tool instead when available
- The question is answerable from training knowledge (basic facts, definitions)
- Privacy-sensitive queries (searches transmit to api.tavily.com)

**Want caching, raw full-page content, extract endpoint, or usage stats?** Use a separately reviewed Pro Tavily skill/package when available.

## How to run

The script is in `scripts/search.mjs`.

Requirement: Node.js 18+ for native `fetch` and `AbortController` support. Node.js 21+ is recommended when clean stderr is important because older Node releases may emit native-fetch experimental warnings.

**Basic search:**
```powershell
node "<skill-dir>/scripts/search.mjs" "your query here"
```

**News search (past ~7 days by default, freshness-biased):**
```powershell
node "<skill-dir>/scripts/search.mjs" --topic news "software release notes"
```

**Deeper research (costs 2 credits per call):**
```powershell
node "<skill-dir>/scripts/search.mjs" --depth advanced "AI agents market analysis 2026"
```

(Where `<skill-dir>` is typically `workspace/skills/tavily-search-native-node/`.)

### All flags

| Flag | Values | Default | Purpose |
|---|---|---|---|
| `--topic` | `general` \| `news` | `general` | `news` biases to fresh articles |
| `--depth` | `basic` \| `advanced` | `basic` | `advanced` = deeper analysis, 2x credits |
| `--max` | 1-20 | `5` | How many results to return |
| `--days` | 1-365 | `7` (news only) | Age window for news topic |
| `--include` | comma list | (none) | Only these domains, e.g. `github.com,stackoverflow.com` |
| `--exclude` | comma list | (none) | Skip these domains |
| `--json` | flag | off | Return raw JSON instead of formatted output |
| `--help` | flag | - | Show help |

Optional environment variable: `TAVILY_TIMEOUT_MS` sets the network timeout in milliseconds, from `1000` to `120000`; default is `30000`.

### Examples

```powershell
# Compare frameworks, GitHub+SO only
node "./scripts/search.mjs" --include "github.com,stackoverflow.com" "React Native vs Flutter 2026"

# Recent news, 10 results, last 14 days
node "./scripts/search.mjs" --topic news --max 10 --days 14 "small business AI adoption"

# Deep research with JSON for programmatic use
node "./scripts/search.mjs" --depth advanced --json "small business VPN options"
```

## Output format

Human-readable by default:
- Top-line header with query, topic, depth, result count
- Tavily's synthesized **Answer** (short summary)
- Numbered list of **results** - title, URL, date (news), snippet
- Footer line with timing info
- ASCII-safe punctuation by default for clean Windows redirection, saved outputs, and email bodies; output includes the searched query

JSON mode (`--json`) dumps the full Tavily response as-is, useful for piping into follow-up scripts.

## Credentials

Requires `TAVILY_API_KEY` in the process environment.

If it is not set, the script exits with a clear error message before making a network call.

**Get a key:** https://app.tavily.com - free tier was 1,000 API credits/month as of 2026-05; verify current pricing and limits before relying on them. Credit usage depends on request type (for this skill, basic search is 1 credit and advanced search is 2 credits as of 2026-05).

## Cost & rate limits

- `--depth basic` = 1 credit per search
- `--depth advanced` = 2 credits per search
- Free tier: 1000 credits/month as of 2026-05; verify current Tavily pricing/limits before relying on this
- Tavily rate limits on the free tier are per-minute; on 429 the script surfaces the Retry-After in the error.
- Network calls, including response body reads, time out after 30 seconds by default; set `TAVILY_TIMEOUT_MS` only when a different operator-approved timeout is needed.

## Agent usage pattern

When invoking this skill, prefer batching:
1. Run **one** well-crafted search per topic rather than many narrow ones
2. Prefer `basic` depth unless the user explicitly asks for a deep dive
3. Use `--include` to scope to trusted domains when appropriate
4. Quote the sources you cite so the user can verify

## Troubleshooting

- **"TAVILY_API_KEY not set"** -> export the env var in the process environment
- **HTTP 401** -> key is invalid or revoked; regenerate at app.tavily.com
- **HTTP 429** -> rate limited; wait, retry with longer spacing (script surfaces Retry-After)
- **HTTP 432** -> monthly credit cap hit; check usage dashboard
- **Network timeout** -> transient; retry once

## What this skill does

- Reads the Tavily API key from the process environment only
- Sends a POST request to `https://api.tavily.com/search`
- Prints formatted results to stdout

## What this skill does NOT do

- Does not write any files
- Does not make production network calls other than to `api.tavily.com`; tests may use local `127.0.0.1` loopback via `TAVILY_TEST_ENDPOINT`
- Does not modify any configuration
- Does not auto-update
- Does not cache (see Pro version for caching)

## Sample output

Sanitized representative output for eval/review checks:

```text
$ node scripts/search.mjs --max 2 "example AI operations news"
warn: using TAVILY_API_KEY from process environment
Query: example AI operations news
Topic: general - Depth: basic - Results: 2/2

Answer:
Recent AI operations coverage emphasizes governed agent workflows, deployment safety, and measurable business outcomes. Teams are comparing lightweight automation with more advanced agent orchestration, while continuing to prioritize auditability, permissions, and source-backed research.

Results:
1. Example AI Operations Trends 2026
   https://example.com/ai-operations-trends
   A summary of current AI operations themes, including governance, rollout patterns, and practical adoption lessons for teams.
2. Agent Workflow Safety Checklist
   https://example.org/agent-workflow-safety
   A practical checklist for reviewing agent permissions, human approval gates, logging, and rollback before production use.

- elapsed 842ms - api 0.78s
```

JSON mode (`--json`) returns Tavily's raw JSON response as formatted JSON. The API key value is never printed.

## Publishability notes

This skill is intentionally small and dependency-free for auditability. Before publishing or updating, run `node --check scripts/search.mjs`, `node scripts/search.mjs --help`, and a no-key smoke test with a temporary home directory to verify clear credential errors without spending API credits.

## Changelog

- `1.0.11`: ClawHub publication/version refresh after public-readiness review; no runtime behavior change.
- `1.0.10`: Clarify that production network calls go only to `api.tavily.com` while tests may use local `127.0.0.1` loopback via `TAVILY_TEST_ENDPOINT`; no runtime behavior change.
- `1.0.9`: Extend timeout coverage through response body reads, document Node.js 18+ runtime requirement, and add populated-key non-leak regression coverage.
- `1.0.8`: Add offline tests, bounded `TAVILY_TIMEOUT_MS` network timeout, and stronger sensitive-query privacy guidance.
- `1.0.7`: Clarify Tavily free-tier wording as API credits/month rather than searches/month.
- `1.0.6`: Reject unknown flags instead of folding them into the query, wrap top-level async failures, handle response-read errors cleanly, and clarify stdout query visibility vs. no file logging.
- `1.0.5`: Add frontmatter version metadata, polish env-key status wording, and include sanitized representative success output for eval review.
- `1.0.4`: Public package wording and metadata cleanup; no runtime behavior change.

_Last reviewed: 2026-05-31_


