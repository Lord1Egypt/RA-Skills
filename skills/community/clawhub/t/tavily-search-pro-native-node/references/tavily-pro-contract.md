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
node "<skill-dir>\scripts\tavily-pro.mjs" cache      # defaults to cache info
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

Wraps Tavily's `/extract` endpoint. Takes one or more public HTTP(S) URLs. The CLI requires raw conventional `http://` or `https://` URLs with a host, rejects malformed/non-HTTP(S)/raw-backslash/credential-bearing URL arguments, and refuses localhost, loopback, unspecified IPv4/IPv6, link-local, RFC1918/private-address URLs, and private/local IPv4-mapped IPv6 forms before sending anything to Tavily. Credential-bearing and local/private URL errors are sanitized and do not echo the supplied URL.

```powershell
node ".\scripts\tavily-pro.mjs" extract https://example.com
node ".\scripts\tavily-pro.mjs" extract https://a.com https://b.com https://c.com
node ".\scripts\tavily-pro.mjs" extract --depth advanced https://spa-site.com
```

Flags: `--depth`, `--json`, `--no-cache`, `--no-log`, `--no-retry`, `--ttl`, `--timeout-ms`.

Estimated credits: Tavily bills extract in batches of 5 URLs - 1 credit per 5 URLs basic, 2 per 5 advanced. The usage log estimates this locally; it is not a Tavily-returned billing value.

## Stats

```powershell
node ".\scripts\tavily-pro.mjs" stats
node ".\scripts\tavily-pro.mjs" stats --days 7
node ".\scripts\tavily-pro.mjs" stats --json
```

Output includes total calls, searches vs extracts, cache hit rate, errors, estimated credits used, and estimated credits avoided by cache.

## Cache

```powershell
node ".\scripts\tavily-pro.mjs" cache info
node ".\scripts\tavily-pro.mjs" cache clear # local deletion - requires explicit approval
```

`cache` with no subcommand defaults to `cache info`. Routine cache reads/writes and usage-log reads/writes perform persistent-state containment checks and refuse symlink-indirected directories/files instead of following them outside `~/.openclaw/cache/tavily-search-pro-native-node/`. `cache clear` accepts no extra arguments, requires explicit approval, rejects symlink-indirected cache paths, deletes only expected hash-named regular cached response JSON files under the skill-specific cache directory, skips non-cache entries, and does not delete `usage.log`. It reports partial deletion failures with the number already deleted instead of returning a false zero.

Responses are cached under `~/.openclaw/cache/tavily-search-pro-native-node/cache/` keyed by a SHA-256-derived hash of request body + kind. Request-body-affecting options such as topic, depth, max results, include/exclude domains, raw-content, URL list, and extract depth create different cache entries; output/control flags such as `--json`, `--ttl`, `--no-log`, and `--no-retry` do not. Cache entries are not API-account-scoped; if multiple Tavily accounts share the same OS user/home directory, they may share cached results for identical requests. Use separate profiles or `--no-cache` when account isolation matters.

Default TTLs:

- Search, general topic: 24 hours
- Search, news topic: 1 hour
- Extract: 7 days

Override with `--ttl SECONDS`; `--ttl 0` disables cache reads for that command but still writes the fresh response to cache unless `--no-cache` is also set. Skip cache reads and writes with `--no-cache`.

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

Queries/URLs are logged in plaintext. Treat unknown/unclassified privacy sensitivity as fail-closed for outbound `search` or `extract`: classify the request first or obtain explicit approval for external Tavily transmission. Use `--no-log --no-cache` for sensitive but approved external calls so this skill's plaintext usage log is skipped and sensitive research context is not cached; this does not eliminate every possible local trace such as shell/agent transcripts, CLI arguments, stdout/stderr, or provider error text.

## Troubleshooting

- `TAVILY_API_KEY not set` -> set env var in process environment.
- HTTP 401 -> invalid/revoked key.
- HTTP 429 -> rate limited; script auto-retries then surfaces Retry-After.
- HTTP 432 -> monthly credit cap hit.
- Network timeout -> retries, then surfaces error.
- Stale results -> use `--no-cache` or `cache clear` after explicit approval for local deletion.
- Cache/log growth -> `cache info`, `cache clear`, or manual log rotation. `cache clear` is local deletion and requires explicit approval before running; it fails closed on cache-path indirection and reports partial deletion failures truthfully.

## Agent usage pattern

1. Classify privacy sensitivity before outbound `search` or `extract`; `unknown` fails closed until classified or explicitly approved for external Tavily transmission.
2. Prefer one well-crafted search over several narrow ones.
3. Use `basic` unless the user asks for deep research.
4. Use `--include` for trusted domains when appropriate.
5. Use cache unless freshness matters.
6. For deep reads: search -> pick URLs -> extract.
7. Quote sources so the user can verify.

## Publish/update checks

Before publishing or updating:

```powershell
node --check scripts\tavily-pro.mjs
node scripts\tavily-pro.mjs help
node scripts\tavily-pro.mjs stats --json
node scripts\self-test.mjs
```

Also run a no-key smoke test with a temporary home directory to verify credential errors without spending credits. Offline mock fixtures are available only when `TAVILY_PRO_SELFTEST=1` is set by `scripts/self-test.mjs`; do not set self-test hooks for normal research use.
