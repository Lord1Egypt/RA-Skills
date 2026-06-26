# Tavily Search Pro Contract

Use only when the compact `SKILL.md` is not enough.

## Commands

Script: `scripts/tavily-pro.mjs`

Subcommands:

- `search`
- `extract`
- `stats`
- `cache`
- `help`

## Quick reference

```powershell
node "<skill-dir>\scripts\tavily-pro.mjs" search "OpenClaw skills ecosystem"
node "<skill-dir>\scripts\tavily-pro.mjs" extract https://example.com/ https://www.iana.org/help/example-domains
node "<skill-dir>\scripts\tavily-pro.mjs" stats
node "<skill-dir>\scripts\tavily-pro.mjs" cache info
node "<skill-dir>\scripts\tavily-pro.mjs" cache clear # local deletion - requires explicit approval
node "<skill-dir>\scripts\tavily-pro.mjs" help
```

## Search flags

| Flag | Values | Default | Purpose |
|---|---|---|---|
| `--topic` | `general` / `news` | `general` | `news` biases to fresh articles |
| `--depth` | `basic` / `advanced` | `basic` | `advanced` = 2 credits |
| `--max` | 1-20 | `5` | Results to return |
| `--days` | integer | `7` news only | Age window |
| `--include` | comma list | none | Domains to include |
| `--exclude` | comma list | none | Domains to exclude |
| `--raw-content` | flag | off | Include full page text per result |
| `--json` | flag | off | Raw JSON output |
| `--no-cache` | flag | off | Skip cache |
| `--no-log` | flag | off | Skip usage log |
| `--no-retry` | flag | off | No backoff on 429 |
| `--ttl` | seconds | 24h general, 1h news | Override cache TTL |
| `--timeout-ms` | integer | 30000 | Per-attempt network timeout |

## Extract flags

Wraps Tavily's `/extract` endpoint. Takes one or more URLs.

```powershell
node ".\scripts\tavily-pro.mjs" extract https://example.com
node ".\scripts\tavily-pro.mjs" extract https://a.com https://b.com https://c.com
node ".\scripts\tavily-pro.mjs" extract --depth advanced https://spa-site.com
```

Flags: `--depth`, `--json`, `--no-cache`, `--no-log`, `--no-retry`, `--ttl`, `--timeout-ms`.

Credits: Tavily bills extract in batches of 5 URLs - 1 credit per 5 URLs basic, 2 per 5 advanced. The usage log tracks this.

## Stats

```powershell
node ".\scripts\tavily-pro.mjs" stats
node ".\scripts\tavily-pro.mjs" stats --days 7
node ".\scripts\tavily-pro.mjs" stats --json
```

Output includes total calls, searches vs extracts, cache hit rate, errors, credits used, and estimated credits avoided by cache.

## Cache

```powershell
node ".\scripts\tavily-pro.mjs" cache info
node ".\scripts\tavily-pro.mjs" cache clear # local deletion - requires explicit approval
```

`cache clear` accepts no extra arguments and deletes cached response JSON files only; it does not delete `usage.log`.

Responses are cached under `~/.openclaw/cache/tavily-search-pro-native-node/cache/` keyed by a SHA-256-derived hash of request body + kind. Request-body-affecting options such as topic, depth, max results, include/exclude domains, raw-content, URL list, and extract depth create different cache entries; output/control flags such as `--json`, `--ttl`, `--no-log`, and `--no-retry` do not. Cache entries are not API-account-scoped; if multiple Tavily accounts share the same OS user/home directory, they may share cached results for identical requests. Use separate profiles or `--no-cache` when account isolation matters.

Default TTLs:

- Search, general topic: 24 hours
- Search, news topic: 1 hour
- Extract: 7 days

Override with `--ttl SECONDS`; skip with `--no-cache`.

## Rate-limit backoff

On HTTP 429, makes up to 3 total attempts with exponential backoff between attempts (normally 1s, then 2s) or respects `Retry-After` when present. Disable with `--no-retry`.

Network errors and per-attempt timeouts also retry. Other HTTP errors surface immediately. Override the default 30000ms timeout with `--timeout-ms N`.

## Usage log

Every call appends one JSON line to:

```text
~/.openclaw/cache/tavily-search-pro-native-node/usage.log
```

Example:

```json
{"ts":1713732000000,"kind":"search","query":"OpenClaw","depth":"basic","topic":"general","cached":false,"credits":1}
```

Queries/URLs are logged in plaintext. Use `--no-log --no-cache` for sensitive but approved external calls so plaintext logging is skipped and sensitive research context is not cached.

## Troubleshooting

- `TAVILY_API_KEY not set` -> set env var in process environment.
- HTTP 401 -> invalid/revoked key.
- HTTP 429 -> rate limited; script auto-retries then surfaces Retry-After.
- HTTP 432 -> monthly credit cap hit.
- Network timeout -> retries, then surfaces error.
- Stale results -> use `--no-cache` or `cache clear` after explicit approval for local deletion.
- Cache/log growth -> `cache info`, `cache clear`, or manual log rotation. `cache clear` is local deletion and requires explicit approval before running.

## Agent usage pattern

1. Prefer one well-crafted search over several narrow ones.
2. Use `basic` unless the user asks for deep research.
3. Use `--include` for trusted domains when appropriate.
4. Use cache unless freshness matters.
5. For deep reads: search -> pick URLs -> extract.
6. Quote sources so the user can verify.

## Publish/update checks

Before publishing or updating:

```powershell
node --check scripts\tavily-pro.mjs
node scripts\tavily-pro.mjs help
node scripts\tavily-pro.mjs stats --json
node scripts\self-test.mjs
```

Also run a no-key smoke test with a temporary home directory to verify credential errors without spending credits. Offline mock fixtures are available only when `TAVILY_PRO_SELFTEST=1` is set by `scripts/self-test.mjs`; do not set self-test hooks for normal research use.
