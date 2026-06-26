---
name: tavily-search-pro-native-node
description: Research-grade Tavily toolkit for OpenClaw - native Node.js, zero dependencies. Use when the user needs deep web research, multi-URL content extraction, Tavily credit usage stats, caching, or 429 backoff. Includes search/extract/stats/cache subcommands, response caching, JSONL usage logging, and rate-limit backoff. Requires TAVILY_API_KEY in the process environment. For minimal search-only use, prefer tavily-search-native-node.
version: 1.0.11
risk_class: external-research-api-credit-cache-log
---

# Tavily Search Pro (Native Node)

Version: 1.0.11 / publishable utility.

Research-grade Tavily helper: one dependency-free Node script with `search`, `extract`, `stats`, and `cache` subcommands.

## Risk / invocation class

Risk class: **external research API / credit usage / plaintext query logging**.

Use deliberately. This skill sends search queries or URLs to Tavily over HTTPS and may append plaintext queries/URLs to a local usage log unless `--no-log` is used.

## Input packet

Required:

- `task`: search, extract, usage stats, or cache inspection.
- `query_or_urls`: search query or URL list when applicable.
- `privacy_sensitivity`: normal, sensitive, client/private, or unknown.
- `freshness_need`: normal cache ok, fresh/no-cache, or news/freshness-critical.
- `depth`: basic unless advanced is justified.

Optional:

- `trusted_domains`: include/exclude domains.
- `max_results`: default 5; avoid broad high-result searches unless needed.
- `logging_preference`: normal log, `--no-log`, or unknown.
- `output_format`: human summary or `--json`.

Stop or switch tools if the query is privacy-sensitive and sending it to Tavily is not appropriate. For one known URL, prefer `web_fetch` unless extraction quality matters.

## Output packet

Return compactly:

- command used or planned, redacted as needed
- whether cache/logging was enabled
- freshness/depth choice
- sources/results with URLs
- credits used or expected when known
- limitations/caveats
- next safe research step

## Security behavior

- Reads `TAVILY_API_KEY` from the process environment only.
- Does not read credential files or `~/.openclaw/.env`.
- Makes network calls only to Tavily's HTTPS endpoints:
  - `https://api.tavily.com/search`
  - `https://api.tavily.com/extract`
- Writes cache and usage logs only under `~/.openclaw/cache/tavily-search-pro-native-node/`.
- Cache filenames are SHA-256-derived request hashes, not plaintext queries.
- Cache entries are not API-account-scoped; if multiple Tavily accounts share the same OS user/home directory, they may share cached results for identical requests. Use separate profiles or `--no-cache` when account isolation matters.
- Usage logs may contain plaintext search queries/URLs; use `--no-log` for sensitive calls.
- Does not read or transmit local files or non-Tavily secrets; sends `TAVILY_API_KEY` only to Tavily for authentication.
- Does not modify system configuration or auto-update.
- Public-registry static-analysis `potential_exfiltration` warnings are expected because this tool combines env credentials, local cache/log file access, and Tavily network calls.

## When to use

Use this Pro skill when:

- the user needs thorough web research, not just a quick lookup;
- multiple queries are likely and cache will save credits;
- full content extraction from specific URLs is needed;
- Tavily usage/stats matter;
- 429 retry/backoff is useful.

Prefer `tavily-search-native-node` when:

- a single simple search is enough;
- minimum audit surface matters;
- no disk writes/caching/logging are desired.

Prefer `web_fetch` for a one-off known URL read.

Do not use when:

- the query is privacy-sensitive and should not leave this machine;
- the user has not approved a sensitive/client/private query to an external research API;
- freshness requires live source browsing and cache state is uncertain, unless `--no-cache` is used.

## Commands

Script: `scripts/tavily-pro.mjs`

```powershell
node "<skill-dir>\scripts\tavily-pro.mjs" search "OpenClaw skills ecosystem"
node "<skill-dir>\scripts\tavily-pro.mjs" extract https://example.com/ https://www.iana.org/help/example-domains
node "<skill-dir>\scripts\tavily-pro.mjs" stats
node "<skill-dir>\scripts\tavily-pro.mjs" cache info
node "<skill-dir>\scripts\tavily-pro.mjs" cache clear  # local deletion; use only after explicit approval
node "<skill-dir>\scripts\tavily-pro.mjs" help
```

For full flags, cache/log behavior, troubleshooting, and publish/update checks, load `references/tavily-pro-contract.md`.

## Operating guidance

- Prefer one well-crafted query over several narrow searches.
- Use `basic` depth unless advanced is justified; `advanced` costs more.
- Use `--include`/`--exclude` to scope sources when appropriate.
- Use cache by default; use `--no-cache` when freshness matters.
- Use `--no-log --no-cache` for sensitive but approved external queries so plaintext query/URL logs are skipped and sensitive research context is not cached.
- For follow-up deep reads: search -> select URLs -> extract.
- Quote sources so the user/requester can verify.
- Track credit usage with `stats` when research runs get large.
- Treat `cache clear` as local destructive cleanup; agents should ask before running it.

## Required checks before publishing/updating

Minimum no-spend checks:

```powershell
node --check skills\tavily-search-pro-native-node\scripts\tavily-pro.mjs
node skills\tavily-search-pro-native-node\scripts\tavily-pro.mjs help
node skills\tavily-search-pro-native-node\scripts\tavily-pro.mjs stats --json
node skills\tavily-search-pro-native-node\scripts\self-test.mjs
```

Also run a no-key smoke test in a temporary home/profile context when feasible to confirm credential errors without spending credits.

## Public registry exposure

Classification: **publishable utility with external API + local cache/log writes**.

Before public update, run sanitizer/static checks and make sure docs clearly disclose:

- external calls to Tavily;
- cache/log file locations and the fact that help/cache output may print a local home-derived cache path; sanitize screenshots/logs before public sharing;
- plaintext query/URL logging;
- expected static-analysis warning;
- no local file/secret exfiltration.

Do not include private/internal/client strategy or operator-specific operational notes in a public release.

## Changelog

- `1.0.11`: ClawHub publication/version refresh after public-readiness review; no runtime behavior change.
- `1.0.10`: Gate `TAVILY_PRO_MOCK_JSON` behind `TAVILY_PRO_SELFTEST=1`, add inert-hook regression, and reject unexpected `cache clear` arguments.
- `1.0.9`: Add request timeout support, strict `stats`/`cache info` argument rejection, and no-spend self-tests.
- `1.0.8`: Tighten public docs for cache-key precision and retry-attempt wording.
- `1.0.7`: Document that cache entries are request-scoped, not API-account-scoped, so shared OS profiles may share cached results.
- `1.0.6`: Add frontmatter version metadata and align reference docs so `cache clear` is consistently marked as local deletion requiring explicit approval.
- `1.0.5`: Public package wording/metadata cleanup; cache/log/security behavior unchanged.


