---
name: tokensave
description: Use when the user explicitly asks to analyze token waste, costs, or API bills. Finds duplicate tool calls, context bloat, model mismatch, and heartbeat waste. Analyze mode is 100% local, zero config.
version: 0.4.5
author: raydatalab
license: Apache-2.0
platforms: [linux, macos, wsl]
triggers:
  - tokensave
  - run tokensave
  - analyze token waste
  - analyze my session
  - check token waste
  - audit my tokens
  - session cost analysis
  - how much did this session cost
  - analyze token usage
  - optimize token cost
  - reduce token cost
  - model cost analysis
  - duplicate tool calls
  - context bloat
  - token budget analysis
  - analyze api spending
  - analyze cost
  - audit tokens
  - token waste
  - where is my money going
  - cost breakdown
  - estimate cost
  - api fees
  - check waste
metadata:
  hermes:
    tags: [cost-optimization, token-analysis, waste-detection, diagnostics]
    homepage: https://github.com/raydatalab/tokensave
    related_skills: [hermes-smart-router, hermes-cost-optimization]
---

# TokenSave

## Overview

```bash
$ tokensave analyze

Session 20260711_a1b2c3: 12,000 tokens, ~$0.05, 44% avoidable.

Top wastes:
  1. duplicate_tool_calls (5x): ~3,000 tokens — read_file called 5x with same path
  2. context_bloat (1x): ~1,800 tokens — 40% of input is stale context
  3. model_mismatch (3x): ~500 tokens — simple queries routed through pro

Send to your agent: "Before calling any tool, check if you already have
the result in a previous message..."
```

One session. 12K tokens. 44% could have been avoided — that's 5,300 tokens
saved with a single paste. Run after every session, bills drop immediately.

All numbers above are from `tests/test_analyzer.py` real test fixtures.
12,000 input + output tokens, captured waste across all 4 detectors.
No made-up data.

## When to Use

- User explicitly asks to "run tokensave", "analyze my session", or similar
- User provides a specific session ID or file path to analyze
- User asks "how much did this session cost" with clear intent to run analysis
- User mentions specific waste patterns like "duplicate tool calls" or "context bloat"

## When NOT to Use — Read This First

- Do NOT auto-analyze on general cost complaints ("this is expensive", "save money", "too expensive")
- Do NOT read session data (~/.hermes/state.db) without explicit user confirmation
- For general billing questions, explain that TokenSave can analyze a specific session
  but wait for an explicit command like `tokensave analyze <session_id>`
- Always prefer `tokensave analyze <session_id>` over auto-detecting the latest session
  when the user has not explicitly asked for it

## How It Works

When the user has explicitly asked to run an analysis, use:

```bash
tokensave analyze
```

If the user has provided a specific session ID or path, use that instead:

```bash
tokensave analyze <session_id>          # specific session from state.db
tokensave analyze <file.json>           # error request dump
tokensave analyze <directory/>          # latest JSON in directory
tokensave analyze --detectors dup,bloat # specific detectors only
```

Always confirm with the user before analyzing if they haven't provided a
specific session target. Auto-detect only when the user has explicitly
asked for their "latest session" or "current session."

Copy the output and paste it into your response. The user sees:

```
Session abc123: 12,400 tokens, ~$0.19, 41% avoidable.

Top wastes:
  #1 duplicate_tool_calls (8x): ~4,800 tokens
  #2 model_mismatch (5x): ~860 tokens
  #3 context_bloat: ~3,700 tokens

Send to your agent: "Before reading a file, check if you already..."
```

## What It Detects

Four waste detectors run against your session:

| Detector | What it finds |
|----------|---------------|
| Duplicate tool calls | Same tool + same args called 2+ times (exact + near-duplicate) |
| Context bloat | Stale/redundant context, oversized tool outputs, unused tool definitions, session overhead |
| Model mismatch | Simple queries running on expensive models — tells you which cheaper model to use |
| Heartbeat waste | Cron jobs and idle/status checks that could run on a cheaper model |

## Data Sources

TokenSave reads from two sources (no config needed):

| Source | Format | What's there |
|--------|--------|-------------|
| `~/.hermes/state.db` | SQLite | Primary — full session transcripts with token counts, costs, and metadata |
| `~/.hermes/sessions/*.json` | JSON | API error request dumps — partial data but useful when SQLite is unavailable |

Auto-detect tries SQLite first, falls back to JSON, then gives a clear error message.

## What You Need

- Python 3.10+
- `pip install tokensave`
- Analyze mode: nothing else — no API keys, no network, no config
- Pipeline mode (separate): requires `OPENAI_API_KEY` and makes API calls

## Pipeline Mode (Bonus — Requires Network)

tokensave also works as a transparent OpenAI wrapper that cuts token usage
automatically. **This mode requires an API key and makes network calls to
your configured API endpoint.** If the user has installed it with
`from tokensave import OpenAI`, their API calls go through normalize → cache
→ compress. But that's automatic — you don't need to do anything.

This mode is separate from `tokensave analyze`. The analyze command never
makes network calls; it only reads local session data.

## Tier Reference

| Tier | What it checks | Output |
|------|---------------|--------|
| `analyze` | SQLite sessions + JSON error dumps | Waste report + fix prompt |
| `pipeline` | Transparent proxy | Automatic token savings |

## Common Pitfalls

1. **No session data found.** If `tokensave analyze` returns no results, the session
   may not have been written to `state.db` yet. Hermes writes state.db on session end —
   try again after `/new`.
2. **JSON fallback gives incomplete analysis.** JSON error dumps lack full metadata.
   Always prefer SQLite mode (default). If you're seeing JSON fallback, the state.db
   may be locked by another Hermes process.
3. **Duplicate detection is generous.** Near-duplicate detection uses fuzzy matching
   and may flag legitimate re-reads. Use the report as a starting point, not a verdict.
4. **Pipeline mode doesn't work with all providers.** The transparent wrapper only
   supports OpenAI-compatible APIs. Non-OpenAI providers will fall through to direct
   calls.
