---
name: tavily-search-pro-native-node
description: Research-grade Tavily web search for OpenClaw using native Node.js with zero dependencies. Use for deep web research, multi-URL content extraction, estimated Tavily credit tracking, response caching, usage-log review, and 429 backoff. Includes search, extract, stats, and cache subcommands. Requires TAVILY_API_KEY in the process environment. For minimal search-only use, prefer tavily-search-native-node.
version: 1.0.36
metadata:
  openclaw:
    requires:
      env:
        - TAVILY_API_KEY
    primaryEnv: TAVILY_API_KEY
    envVars:
      - name: TAVILY_API_KEY
        required: true
        description: Tavily API key used for authenticated search and extract requests.
risk_class: external-research-api-credit-cache-log-local-delete
---

# Tavily Search Pro (Native Node)

Version: 1.0.36 / public ClawHub utility candidate with external API, cache, usage-log, and approval-gated local cache deletion behavior.

Research-grade Tavily web search helper: one dependency-free Node script with `search`, `extract`, `stats`, and `cache` subcommands.

## Risk / invocation class

Risk class: **external research API / credit usage / plaintext query logging / local cache deletion**.

Use deliberately. This skill sends search queries or URLs to Tavily over HTTPS, may append plaintext queries/URLs to a local usage log unless `--no-log` is used, and exposes `cache clear` as approval-gated local deletion of cached response JSON files.

## Input packet

Required:

- `task`: search, extract, usage stats, or cache inspection.
- `query_or_urls`: search query or URL list when applicable.
- `privacy_sensitivity`: normal, sensitive, client/private, or unknown. `unknown` is a fail-closed state for `search` and `extract`: classify sensitivity first or obtain explicit approval for external Tavily transmission before running an outbound command.
- `freshness_need`: normal cache ok, fresh/no-cache, or news/freshness-critical.
- `depth`: basic unless advanced is justified.

Optional:

- `trusted_domains`: include/exclude domains.
- `max_results`: default 5; avoid broad high-result searches unless needed.
- `logging_preference`: normal log, `--no-log`, or unknown.
- `output_format`: human summary or `--json`.

Stop or switch tools if the query is privacy-sensitive and sending it to Tavily is not appropriate. If `privacy_sensitivity` is `unknown`, do not run `search` or `extract` until sensitivity is classified as normal or explicit approval resolves the external-send ambiguity. For one known URL, prefer `web_fetch` unless extraction quality matters.

## Output packet

Return compactly:

- command used or planned, redacted as needed
- whether cache/logging was enabled
- freshness/depth choice
- sources/results with URLs
- estimated credits used or expected when known
- limitations/caveats
- next safe research step

## Security behavior

- Reads `TAVILY_API_KEY` from the process environment only.
- Does not read credential files or `~/.openclaw/.env`.
- Makes network calls only to Tavily's HTTPS endpoints:
  - `https://api.tavily.com/search`
  - `https://api.tavily.com/extract`
- Writes cache and usage logs only under `~/.openclaw/cache/tavily-search-pro-native-node/` after routine persistent-state containment checks; routine cache/log reads and writes refuse symlink-indirected directories/files. `cache clear` requires explicit approval, rejects symlink-indirected cache paths, deletes only expected hash-named regular cached response JSON files under that skill-specific cache directory, skips non-cache entries, and reports partial deletion failures truthfully.
- Cache filenames are SHA-256-derived request hashes, not plaintext queries.
- Cache entries are not API-account-scoped; if multiple Tavily accounts share the same OS user/home directory, they may share cached results for identical requests. Use separate profiles or `--no-cache` when account isolation matters.
- Usage logs may contain plaintext search queries/URLs; use `--no-log` for approved sensitive external calls.
- Local/private URL refusal is a guardrail for obvious mistaken extract targets, not a complete SSRF boundary; Tavily performs extraction from Tavily infrastructure, not this machine.
- Does not read local files outside its documented cache/log state, and does not read non-Tavily secrets. User-supplied search queries and accepted extract URLs are sent to Tavily; `TAVILY_API_KEY` is sent only to Tavily for authentication. Credential-bearing and local/private extract URLs are rejected before API key load/Tavily transmission, and those error paths do not echo the supplied URL.
- Does not modify system configuration or auto-update. The only destructive local action is the documented, approval-gated `cache clear` deletion of expected regular cached response JSON files after cache-path containment checks.
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

- the query privacy is unknown/unclassified; classify it or get explicit approval before any external Tavily transmission;
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
node "<skill-dir>\scripts\tavily-pro.mjs" cache       # defaults to cache info
node "<skill-dir>\scripts\tavily-pro.mjs" cache clear  # local deletion; use only after explicit approval
node "<skill-dir>\scripts\tavily-pro.mjs" help
```

For full flags, cache/log behavior, troubleshooting, and publish/update checks, load `references/tavily-pro-contract.md`.

## Operating guidance

- Prefer one well-crafted query over several narrow searches.
- Use `basic` depth unless advanced is justified; `advanced` costs more.
- Use `--include`/`--exclude` to scope sources when appropriate.
- Use cache by default; use `--no-cache` when freshness matters. `--ttl 0` disables cache reads for that command but still writes the fresh response to cache unless `--no-cache` is also set.
- Treat `privacy_sensitivity: unknown` as a stop state for outbound `search`/`extract`; classify the request or get explicit approval before Tavily receives the query/URLs.
- Use `--no-log --no-cache` for sensitive but approved external queries so this skill's plaintext usage log is skipped and sensitive research context is not cached; this does not remove every possible local trace such as shell/agent transcripts or provider error text.
- For follow-up deep reads: search -> select URLs -> extract.
- Quote sources so the user/requester can verify.
- Track estimated credit usage with `stats` when research runs get large.
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

Classification: **public ClawHub utility candidate with external API + local cache/log writes + approval-gated local cache deletion**.

Before public update, run sanitizer/static checks and make sure docs clearly disclose:

- external calls to Tavily;
- cache/log file locations and the fact that help/cache output may print a local home-derived cache path; sanitize screenshots/logs before public sharing;
- plaintext query/URL logging;
- expected static-analysis warning;
- no local file/secret exfiltration.

Do not include private/internal/client strategy or operator-specific operational notes in a public release.

## Changelog

- `1.0.36`: Add runtime help-text polish that explicitly says `search` and `extract` require `TAVILY_API_KEY` and send queries/URLs to Tavily; no behavior change. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.35`: Harden routine cache/log reads and writes against symlink-indirected persistent-state directories/files, align security prose with local cache/log reads, and add no-spend regression tests proving normal search cannot redirect `usage.log` or cache-entry writes through pre-existing symlinks. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.34`: Remove the remaining overbroad Windows-indirection wording from the changelog so public source wording matches the symlink-only source/test evidence; no runtime behavior change. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.33`: Complete the symlink-only wording alignment by updating the runtime refusal message and changelog; no cache-clear behavior change. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.32`: Narrow public `cache clear` documentation from overbroad Windows-indirection wording to symlink-indirection so the wording matches source/test evidence; no runtime behavior change. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.31`: Harden `cache clear` with cache-root containment checks, symlink-indirection refusal, hash-named regular cache-file deletion only, non-cache-entry skipping, truthful partial-failure reporting, and temp-home self-test regressions. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.30`: Polish security wording so `--no-log` guidance explicitly applies to approved sensitive external calls, preserving fail-closed handling for unknown/unapproved sensitive material. No runtime behavior change. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.29`: Expand risk metadata/prose to include approval-gated local cache deletion, make `privacy_sensitivity: unknown` fail closed before outbound Tavily search/extract, and add static self-test assertions for those public-candidate safety requirements. No runtime search/extract behavior change. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.28`: Sanitize local/private extract URL errors so rejected localhost/private/link-local/ULA URLs are not echoed to stderr/log-support pastes; add path/query no-echo regression coverage. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.27`: Sanitize credential-bearing extract URL errors so rejected username/password userinfo inputs are not echoed to stderr/log-support pastes; add no-echo regression coverage. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.26`: Tighten extract URL validation to reject credential-bearing URLs with username/password userinfo before API key load/Tavily transmission; clarify user-supplied query/URL transmission wording and add regression coverage. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.25`: Tighten extract URL validation to reject raw backslash characters before URL parsing, preventing parser repair of backslash authority/path forms before API key load/Tavily transmission; add regression coverage. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.24`: Tighten extract URL validation to require raw conventional `http://` or `https://` URLs with a host, preventing URL-parser repair of slashless, one-slash, extra-slash, or backslash-ish HTTP(S) inputs before API key load/Tavily transmission; add regression coverage. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.23`: Polish extract validation so malformed or non-HTTP(S) URL arguments fail as invalid before API key load/Tavily transmission, and add no-key regression coverage for malformed HTTP/IPv6 and non-HTTP protocol cases. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.22`: Polish extract URL guard to reject IPv6 unspecified literals (`::` and expanded all-zero form) before API key load/Tavily transmission and add self-test coverage. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.21`: Fix extract URL guard to reject IPv4-mapped IPv6 private/local/link-local addresses before API key load/Tavily transmission, add `0.0.0.0` refusal, and add self-test coverage for mapped loopback/RFC1918/link-local plus mapped public DNS allow-through-to-no-key behavior. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.20`: Add ClawHub/OpenClaw runtime metadata for required `TAVILY_API_KEY`, including `requires.env`, `primaryEnv`, and `envVars`, so declared requirements match the script's env-key behavior. No runtime behavior change. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.19`: Neutralize approval/process wording in header, classification, and changelog notes. No runtime behavior change. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.18`: Normalize prior changelog wording. No runtime behavior change. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.17`: Remove person-specific wording from prior changelog notes. No runtime behavior change. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.16`: Clarify ClawHub candidate posture in the header and document that local/private URL refusal is a best-effort guardrail for obvious mistaken extract targets, not a complete SSRF boundary. No runtime behavior change. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.15`: Input-validation polish: restrict IPv6 ULA `fc00::/7` refusal to actual IPv6 literals so public DNS names beginning with `fc`/`fd` are not overblocked, while retaining ULA and link-local refusal before API key load/Tavily transmission. Adds self-test coverage for ULA and public `fc*`/`fd*` hostnames. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.14`: Input-validation polish: correctly block the full IPv6 link-local `fe80::/10` range (`fe80` through `febf`) before API key load/Tavily transmission and add self-test coverage for boundary examples. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.13`: Input-validation polish: block IPv6 link-local `fe80::/10` extract URLs before API key load/Tavily transmission, add self-test coverage, and align frontmatter description with source wording. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.12`: Polish source wording from “toolkit” to web search, clarify estimated credit labels/docs, document `--ttl 0` cache-read semantics and default `cache` behavior, reject local/private extract URLs before Tavily transmission, and avoid standing publishability wording. No categories, topics, topic tags, tags, keywords, or ClawHub catalog metadata added to source.
- `1.0.11`: Version refresh; no runtime behavior change.
- `1.0.10`: Gate `TAVILY_PRO_MOCK_JSON` behind `TAVILY_PRO_SELFTEST=1`, add inert-hook regression, and reject unexpected `cache clear` arguments.
- `1.0.9`: Add request timeout support, strict `stats`/`cache info` argument rejection, and no-spend self-tests.
- `1.0.8`: Tighten public docs for cache-key precision and retry-attempt wording.
- `1.0.7`: Document that cache entries are request-scoped, not API-account-scoped, so shared OS profiles may share cached results.
- `1.0.6`: Add frontmatter version metadata and align reference docs so `cache clear` is consistently marked as local deletion requiring explicit approval.
- `1.0.5`: Public package wording/metadata cleanup; cache/log/security behavior unchanged.
