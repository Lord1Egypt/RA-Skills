---
name: web-search-pro
description: |
  Agent-first web search and retrieval for live web search, news search, docs lookup, code
  lookup, company research, site crawl, site map, and structured evidence packs.
  Includes a no-key baseline plus optional Tavily, Exa, Querit, Serper, Brave, SerpAPI, You.com,
  SearXNG, and Perplexity / Sonar providers for wider coverage and answer-first routing.
homepage: https://github.com/Zjianru/web-search-pro
metadata: {"openclaw":{"emoji":"🔎","requires":{"bins":["node"],"config":["config.json"],"env":{"TAVILY_API_KEY":"optional — premium deep search, news, and extract","EXA_API_KEY":"optional — semantic search and extract fallback","QUERIT_API_KEY":"optional — multilingual AI search with native geo and language filters","SERPER_API_KEY":"optional — Google-like search and news","BRAVE_API_KEY":"optional — structured web search aligned with existing OpenClaw setups","SERPAPI_API_KEY":"optional — multi-engine search including Baidu","YOU_API_KEY":"optional — LLM-ready web search with freshness and locale support","PERPLEXITY_API_KEY":"optional — native Perplexity Sonar access","OPENROUTER_API_KEY":"optional — gateway access to Perplexity/Sonar via OpenRouter","KILOCODE_API_KEY":"optional — gateway access to Perplexity/Sonar via Kilo","PERPLEXITY_GATEWAY_API_KEY":"optional — custom gateway key for Perplexity/Sonar models","PERPLEXITY_BASE_URL":"optional — required with PERPLEXITY_GATEWAY_API_KEY","SEARXNG_INSTANCE_URL":"optional — self-hosted privacy-first metasearch endpoint"},"note":"No API key is required for the baseline. Optional provider credentials or endpoints widen retrieval coverage."}},"clawdbot":{"emoji":"🔎","requires":{"bins":["node"],"config":["config.json"],"note":"No API key is required for the baseline. Optional provider credentials or endpoints widen retrieval coverage."},"install":[{"kind":"node","label":"Bundled Node skill runtime","bins":["node"]}],"config":{"stateDirs":[".cache/web-search-pro"],"example":"{\n  env = {\n    WEB_SEARCH_PRO_CONFIG = \"./config.json\";\n  };\n}"},"cliHelp":"node {baseDir}/scripts/search.mjs --help"}}
---

# Web Search Pro 2.1 Core Profile

This ClawHub package publishes the core retrieval profile of `web-search-pro`.
It is a code-backed Node runtime package, not an instruction-only bundle.

## Use This Skill When

- the caller needs live web search or news search
- the caller needs docs lookup or code lookup
- the caller may continue from search into extract, crawl, map, or research
- the agent needs explainable routing and visible federated-search gains
- the first run needs a real no-key baseline

## Quick Start

The shortest successful path is:

- Option A: No-key baseline
- Option B: Add one premium provider
- Then try docs, news, and research

### Option A: No-key baseline

No API key is required for the first successful run.

```bash
node {baseDir}/scripts/doctor.mjs --json
node {baseDir}/scripts/bootstrap.mjs --json
node {baseDir}/scripts/search.mjs "OpenAI Responses API docs" --json
```

### Option B: Add one premium provider

If you only add one premium provider, start with `TAVILY_API_KEY`.

```bash
export TAVILY_API_KEY=tvly-xxxxx
node {baseDir}/scripts/doctor.mjs --json
node {baseDir}/scripts/search.mjs "latest OpenAI news" --type news --json
```

### First successful searches

```bash
node {baseDir}/scripts/search.mjs "OpenClaw web search" --json
node {baseDir}/scripts/search.mjs "OpenAI Responses API docs" --preset docs --plan --json
node {baseDir}/scripts/extract.mjs "https://platform.openai.com/docs" --json
```

### Then try docs, news, and research

```bash
node {baseDir}/scripts/search.mjs "OpenAI Responses API docs" --preset docs --json
node {baseDir}/scripts/search.mjs "latest OpenAI news" --type news --json
node {baseDir}/scripts/research.mjs "OpenClaw search skill landscape" --plan --json
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

## Runtime Contract

- `selectedProvider`
  The planner's primary route.
- `routingSummary`
  Compact route explanation with confidence and federation summary.
- `routing.diagnostics`
  Full route diagnostics exposed by `--explain-routing` or `--plan`.
- `federated.providersUsed`
  The providers that actually returned results when fanout is active.
- `federated.value`
  Compact federation gain summary for added providers, recovered results, corroboration, and
  duplicate savings.
- `cached` / `cache`
  Cache hit plus TTL telemetry for agents.
- `topicType`, `topicSignals`, `researchAxes`
  Structured planning summaries for the model-facing research pack.

## Commands By Task

Included commands:

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

Runtime notes:

- Node is the only hard runtime requirement.
- No API key is required for the baseline.
- Optional provider credentials or endpoints widen coverage.
- Baseline outbound requests use `curl` when available and fall back to built-in `fetch`.

Baseline:

- No API key is required for the baseline.
- `ddg` is best-effort no-key search.
- `fetch` is the no-key extract / crawl / map fallback.

Optional provider credentials or endpoints unlock stronger coverage:

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

Review and diagnostics:

```bash
node {baseDir}/scripts/capabilities.mjs --json
node {baseDir}/scripts/doctor.mjs --json
node {baseDir}/scripts/bootstrap.mjs --json
node {baseDir}/scripts/review.mjs --json
```

Search keywords:

`web search`, `news search`, `latest updates`, `current events`, `docs search`,
`API docs`, `code search`, `company research`, `competitor analysis`, `site crawl`,
`site map`, `multilingual search`, `Baidu search`, `answer-first search`,
`cited answers`, `explainable routing`, `no-key baseline`
