# Web Search Pro 2.1 Core Profile

`web-search-pro` is a search skill and local retrieval runtime for agents. This ClawHub package
ships the narrower core profile: enough to search, extract, crawl, map, and assemble research
packs, while keeping the published artifact review-friendly.

It is a code-backed Node runtime package, not an instruction-only bundle.

## What This Core Profile Is

Use this package when you want:

- live web search and news search
- docs lookup and code lookup
- explainable routing
- visible federated-search gains
- extract, crawl, map, and research flows
- a real no-key baseline before adding premium providers

This package is not the full repository surface. It is the ClawHub install profile that focuses on
the core retrieval path.

## Quick Start

The shortest successful path is:

- Option A: No-key baseline
- Option B: Add one premium provider
- Then try docs, news, and research

### Option A: No-key baseline

No API key is required for the first successful run.

```bash
node scripts/doctor.mjs --json
node scripts/bootstrap.mjs --json
node scripts/search.mjs "OpenAI Responses API docs" --json
```

### Option B: Add one premium provider

If you only add one premium provider, start with `TAVILY_API_KEY`.

```bash
export TAVILY_API_KEY=tvly-xxxxx
node scripts/doctor.mjs --json
node scripts/search.mjs "latest OpenAI news" --type news --json
```

### First successful searches

```bash
node scripts/search.mjs "OpenClaw web search" --json
node scripts/search.mjs "OpenAI Responses API docs" --preset docs --plan --json
node scripts/extract.mjs "https://platform.openai.com/docs" --json
```

### Then try docs, news, and research

```bash
node scripts/search.mjs "OpenAI Responses API docs" --preset docs --json
node scripts/search.mjs "latest OpenAI news" --type news --json
node scripts/research.mjs "OpenClaw search skill landscape" --plan --json
```

## Install Model

ClawHub installs this bundle directly as a code-backed Node skill pack.

- hard runtime requirement: `node`
- no remote installer, curl-to-shell bootstrap, or Python helper transport in the baseline path
- optional runtime config file: `config.json`
- local state directory: `.cache/web-search-pro`

## Why Federated Search Matters

Federation is not just "more providers". It exposes compact gain metrics:

- `federated.value.additionalProvidersUsed`
- `federated.value.resultsRecoveredByFanout`
- `federated.value.resultsCorroboratedByFanout`
- `federated.value.duplicateSavings`
- `routingSummary.federation.value`

## What This Package Includes

- `search.mjs`
- `extract.mjs`
- `crawl.mjs`
- `map.mjs`
- `research.mjs`
- `doctor.mjs`
- `bootstrap.mjs`
- `capabilities.mjs`
- `review.mjs`
- `cache.mjs`
- `health.mjs`

## Runtime Contract

- `selectedProvider`
  The planner's primary route.
- `routingSummary`
  Compact route explanation with confidence and federation summary.
- `federated.providersUsed`
  Providers that actually returned results when fanout is active.
- `federated.value`
  Compact federation gain summary.
- `cached` / `cache`
  Cache hit and TTL telemetry for agents.
- `topicType`, `topicSignals`, `researchAxes`
  Compact planning summaries for the model-facing research pack.

## Baseline And Optional Providers

No API key is required for the baseline.

Optional provider credentials or endpoints unlock higher-quality retrieval:

```bash
TAVILY_API_KEY=tvly-xxxxx
EXA_API_KEY=exa-xxxxx
QUERIT_API_KEY=xxxxx
SERPER_API_KEY=xxxxx
BRAVE_API_KEY=xxxxx
SERPAPI_API_KEY=xxxxx
YOU_API_KEY=xxxxx
SEARXNG_INSTANCE_URL=https://searx.example.com

# Perplexity / Sonar: choose one transport path
PERPLEXITY_API_KEY=xxxxx
OPENROUTER_API_KEY=xxxxx
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1  # optional override
KILOCODE_API_KEY=xxxxx

# Or use a custom OpenAI-compatible gateway
PERPLEXITY_GATEWAY_API_KEY=xxxxx
PERPLEXITY_BASE_URL=https://gateway.example.com/v1
PERPLEXITY_MODEL=perplexity/sonar-pro  # accepts sonar* or perplexity/sonar*
```

The baseline remains:

- `ddg` for best-effort search
- `fetch` for extract / crawl / map fallback

## Core Commands

```bash
node scripts/search.mjs "OpenClaw web search" --plan --json
node scripts/extract.mjs "https://example.com/article" --json
node scripts/crawl.mjs "https://example.com/docs" --depth 2 --max-pages 10 --json
node scripts/map.mjs "https://example.com/docs" --depth 2 --max-pages 50 --json
node scripts/research.mjs "OpenClaw search skill landscape" --plan --json
node scripts/doctor.mjs --json
node scripts/bootstrap.mjs --json
node scripts/review.mjs --json
```

## Why This Is A Core Profile

The GitHub repository contains the full `2.1` source tree, including extra local-only developer
surfaces and validation tooling. The ClawHub publish package intentionally keeps the installed
artifact smaller so the registry package stays honest about its runtime shape.

The shipped core profile runs with Node plus direct network access through `curl` or built-in
`fetch`; it does not rely on Python helper transports.

Search keywords:

`web search`, `news search`, `latest updates`, `current events`, `docs search`,
`API docs`, `code search`, `company research`, `competitor analysis`, `site crawl`,
`site map`, `multilingual search`, `Baidu search`, `answer-first search`,
`cited answers`, `explainable routing`, `no-key baseline`

Full source:
- https://github.com/Zjianru/web-search-pro
