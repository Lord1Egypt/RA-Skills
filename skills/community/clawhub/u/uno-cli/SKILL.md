---
name: uno-cli
slug: uno-cli
displayName: Uno CLI
version: 1.2.1
summary: "pip install uno-cli, then uno whoami → uno search → uno call. 2000+ tools."
license: MIT
description: "On-demand tool client for the Uno tool gateway (agentools.uno). The agent first searches for the single specific tool that matches the user's request (e.g. 'weather in Beijing' → `search \"weather\"`), previews the planned invocation with `call --dry-run` for user confirmation, and only then issues the real call — every invocation is one explicit, user-visible, user-approved action. No background actions, no token echoing, no implicit multi-tool use. Install via `clawhub install uno-cli` when built-in skills cannot cover a narrow real-time lookup the user explicitly asks for."
homepage: https://agentools.uno
metadata: {"emoji":"◆","category":"tools","api_base":"https://agentools.uno","version":"1.2.1","runtime_dependencies":["uno-cli>=1.0.2"],"safety":{"consent_model":"search → dry-run preview → explicit user approval → real call; every call is one single, user-visible action","background_actions":"none","credential_scope":"single ClawdChat-issued Uno API key (uno_…), stored in ~/.uno/credentials.json at mode 600 — not a browser JWT","token_echo_policy":"stdout is passed through a secret-field stripper; the raw API key is never printed by the CLI (login, whoami, keys list/create all return masked previews only) — the key lives only in the 0600 credentials file","dry_run_preview":"`uno call --dry-run <tool> --args {...}` returns the planned invocation as JSON without reading credentials, opening any network connection, or spending any credit — the primary user-confirmation surface before a real call","revocation":"`logout` clears local credentials; `disconnect <server>` revokes the stored third-party OAuth token for that server only","third_party_auth":"each third-party OAuth connection is initiated by the user via a browser URL surfaced by the CLI; the CLI never stores third-party passwords"}}
---

# Uno CLI

> **Officially provided by ClawdChat (虾聊)** — a narrow, on-demand tool client. The agent searches for a single specific tool that matches the user's request, previews it with `--dry-run` for user confirmation, and only then issues the real call.

## Safety & user consent (read this first)

- **Search → dry-run → confirm → call.** The expected flow is four explicit steps. `call --dry-run` formats the planned invocation as JSON without reading the credentials file, opening any network connection, or spending any credit — the agent shows that preview to the user and only re-runs without `--dry-run` after explicit human approval.
- **Consent is per-call, not per-session.** Each `call` is a single, explicit tool invocation. The agent surfaces the tool name and arguments to the user; the CLI never chains or schedules calls on its own.
- **No background actions.** The CLI exits after each command. It does not run daemons, listeners, or retries without an explicit new invocation from the agent.
- **One credential, user-scoped.** The CLI uses one ClawdChat-issued **API key** (`uno_…`), stored at `~/.uno/credentials.json` (mode `0600`). This is not a browser JWT. It never reads the user's password, keychain, shell history, or other apps' credentials.
- **Tokens are never echoed to stdout.** Every response the CLI writes is funnelled through a secret-field stripper (`uno_cli.cli._strip_secrets`) that masks any field whose name looks like a credential — `api_key`, `access_token`, `refresh_token`, `secret`, `password`, `token`, etc. `login --poll` reports only `credential_stored_at` and a masked preview; `whoami`, `keys list`, and `keys create` return user/key metadata with any returned secrets already masked. A raw token therefore cannot land in a terminal scrollback, shell history, log file, or an agent's captured stdout. CI jobs that truly need the value read the 0600 credentials file directly. ([implementation](https://pypi.org/project/uno-cli/))
- **Per-server third-party auth is user-initiated.** When a tool needs its own OAuth (e.g. a notes service or a code-hosting service), the CLI returns an `auth_url`. The agent shows that URL to the user; only after the user completes the browser flow does the token get stored server-side. The CLI itself never receives third-party passwords.
- **Revocation is trivial and local.** `python bin/uno.py disconnect <server>` revokes the stored token for one server. `python bin/uno.py logout` deletes the local credential file. Both are single-command and reversible only by the user logging in again.
- **Credits are real money.** Before heavy or exploratory usage, the agent should call `whoami` to show the user their remaining credits.

## Prerequisites

- Python 3.8+ (pre-installed on most systems)
- The [`uno-cli`](https://pypi.org/project/uno-cli/) PyPI package, **≥ 1.0.2** (MIT, stdlib-only, no transitive deps) — 1.0.1 introduced unconditional stdout secret-stripping; 1.0.2 adds `call --dry-run` for credential-free preview of a planned invocation

The bundled `bin/uno.py` is a thin launcher that forwards to the `uno-cli` package. This means upgrades land via `pip install --upgrade uno-cli` without shipping a new skill release.

CLI path (relative to this file): `bin/uno.py`

## Step 0: Install the Uno CLI (one-time)

```bash
python3 -m pip install --user --upgrade 'uno-cli>=1.0.2'
```

Verify:

```bash
python bin/uno.py --version    # or: uno --version
```

If `uno-cli` is missing the launcher returns `{"error": "uno-cli not installed", "hint": "...", "install_url": "https://pypi.org/project/uno-cli/"}` and exits with code `2`.

## Step 1: Check Existing Credentials First

**Before doing anything else**, always check if valid credentials already exist:

```bash
python bin/uno.py whoami --compact
```

- **Success** (returns user info with name/email/credits) → credentials are valid, **skip login and proceed directly to tool use**
- **Failure** (non-zero exit or `{"error": ...}`) → credentials missing or rejected, proceed to Authentication below
- **Only start a new login flow** if credentials are invalid/missing, or the user explicitly requests re-authentication
- Same OS user and same `$HOME` → next session `whoami` works automatically. A new machine or an ephemeral Cloud Agent disk does not keep `~/.uno`

## Authentication

`whoami` / `call` may print `Run: uno login`. Do **not** run bare `login` — it blocks the terminal. Use `--start` / `--poll`.

The `/device` page has the user sign in on the website if needed, then click Authorize. Opening the URL is not finished.

**Stop after `--start`.** Give the user `verification_uri_complete` and wait until they say they authorized. Do **not** run `--poll` in the same turn.

Check if credentials already exist (`~/.uno/credentials.json`) before using; only login if they are missing.

```bash
# Option A: Two-step login (recommended for agents — non-blocking)
python bin/uno.py login --start
# → Returns JSON: {"status": "pending", "verification_uri_complete": "https://...", "device_code": "xxx", ...}
# After the user confirms they authorized:
python bin/uno.py login --poll <device_code>
# → {"success": true, "name": "...", "email": "..."}

# Option B: One-shot interactive (for terminal users — blocks until authorized)
python bin/uno.py login

# Option C: Direct API Key (https://agentools.uno/dashboard?tab=keys)
python bin/uno.py login --key uno_xxxxx

# Switch accounts (multi-account)
python bin/uno.py use                  # list all accounts
python bin/uno.py use <name_or_email>  # switch to specified account

# Logout
python bin/uno.py logout
python bin/uno.py logout --all         # remove all accounts
```

Env var `UNO_API_KEY` takes priority over file config (useful for CI).

### Auth Flow Details

Uno uses **Device Code Flow**. The website login page offers the available sign-in methods; do not invent a separate signup URL.

1. `login --start` requests a device code from Uno server
2. Show `verification_uri_complete` to the user. The page is `/device` on agentools.uno — they sign in on the website if needed, then Authorize. **Do not `--poll` in the same turn.**
3. After authorization, `login --poll` retrieves an **API key** (`uno_…`) and writes it to `~/.uno/credentials.json`
4. `--poll` waits **10 minutes** by default. The device code is valid **30 minutes**. If poll times out, re-run `--poll` with the **same** `device_code`
5. Server-side keys do **not** expire. Re-login only when: new machine / ephemeral `$HOME`; `logout` (local wipe only); key deleted in the dashboard / `keys delete`; user disabled; a stale `UNO_API_KEY` overrides a good file
6. A tool returning `auth_required` is that **server's** OAuth/key, not the Uno key

## Command Reference

All commands output pretty-printed JSON by default. Add `--compact` for single-line JSON (fewer tokens).

### Status

```bash
python bin/uno.py whoami               # current user info (credits, plan, keys)
python bin/uno.py health               # server health check
```

### Search Tools

```bash
python bin/uno.py search "weather" [--limit 10] [--mode hybrid|keyword|semantic] [--category dev] [--server weather-free]
```

`--limit` must be between 1 and 50 (enforced both client-side and server-side).

Each result contains:
- `tool` (slug), `name`, `desc`, `desc_en` — use for display / disambiguation
- `input_schema` (JSON Schema) — use to construct correct arguments for `call`
- `server`, `server_name`, `category`, `auth_required`
- `stats`: `{avg_ms, calls_7d, success_rate, rating}` — **use to pick between equivalent servers** (prefer higher `calls_7d` and `rating`)
- `pricing`: `{mode, cost}` — `per_call` credits or `per_token` price

If `desc` ends with `…`, it was truncated (500 chars for search, 200 for browse). Run `tool get <slug>` for the full version.

#### How Search Works (Agent Best Practices)

Search uses **hybrid retrieval** under the hood:
1. **Smart tokenizer** — drops Chinese/English stopwords (`搜索/关于/项目/please/find/...`), strips multi-char CJK stopwords as substrings, runs `jieba` segmentation, and discards single ASCII chars. So `"搜索 GitHub 上关于 MCP 的项目"` automatically reduces to `["github", "mcp"]` before retrieval.
2. **Keyword channel** — OR-based candidate selection with per-row weighted scoring. Strongest signal is an exact server-slug match (e.g. `"github"` → server `github` → +10 points).
3. **Semantic channel** — pgvector cosine similarity over tool description embeddings (30-day Redis cache).
4. **Adaptive RRF fusion** — if the keyword channel has a clear winner (server-slug exact match), its weight is boosted 2.5× so strong keyword signals aren't drowned by mediocre dual-channel matches.

Quality is regression-tested against `tests/golden_queries.json` (52 bilingual queries) via `scripts/evaluate_search.py`. Last production measurement (2026-04-18):

| Metric | Score | Target | Status |
|---|---|---|---|
| NDCG@5 | **0.889** | ≥ 0.75 | ✓ PASS |
| MRR | **0.946** | ≥ 0.75 | ✓ PASS |
| Recall@5 | **0.472** | ≥ 0.45 | ✓ PASS (theoretical max on this dataset is 0.54 — see note below) |

English and Chinese queries perform symmetrically: NDCG@5 en=0.886, zh=0.895. The Recall@5 ceiling of ~0.54 comes from the dataset labeling — 96% of queries have more than 5 relevant tools labeled, so a perfect top-5 still can't exceed ~54% recall.

**Query tips (most → least important):**
- **Short capability keywords are best**: `"weather"`, `"github mcp"`, `"image generation"` — 1-3 words beats everything else.
- **Use the server slug when known** (e.g. `"weather-free"`, `"wolfram"`, `"news-api"`): an exact server-slug match is the strongest retrieval signal.
- **Full questions also work**, because the tokenizer strips stopwords automatically — but short keywords are still faster and more precise.
- **Chinese and English are symmetric**: `"天气"` ≈ `"weather"`, `"搜索"` ≈ `"search"`.
- **If no results**, try a synonym: `"map"` → `"navigation"`, `"translate"` → `"翻译"`.

**Query pattern examples (read-only look-ups, agent should still surface results to the user):**

| User intent | Good query (preferred) | Also works |
|---|---|---|
| "What happened in the markets today?" | ✓ `search "news"` | `search "新闻"` |
| "北京明天天气" | ✓ `search "weather"` | `search "天气"` |
| "Latest BTC price" | ✓ `search "crypto"` | `search "币价"` |
| "List MCP servers about travel" | ✓ `search "mcp travel"` | `search "mcp"` + filter |

### Tool Details

```bash
python bin/uno.py tool get <tool_slug>
# e.g. python bin/uno.py tool get amap-maps.maps_weather
```

### Call a Tool

**Step 1 — always preview first with `--dry-run`** (zero network, zero credential read, zero credits):

```bash
python bin/uno.py call --dry-run weather-free.weather_now --args '{"city":"Beijing"}'
```

Response:

```json
{
  "success": true,
  "dry_run": true,
  "preview": {"tool": "weather-free.weather_now", "arguments": {"city": "Beijing"}, "timeout_seconds": 60},
  "note": "No network request was made, no credentials were read, and no credits were spent. Re-run without --dry-run to actually invoke the tool."
}
```

Show this JSON to the user and wait for explicit approval.

**Step 2 — after the user approves, re-run without `--dry-run`**:

```bash
python bin/uno.py call weather-free.weather_now --args '{"city":"Beijing"}'
```

Response:

```json
{"success": true, "data": {...}, "meta": {"latency_ms": 234, "credits_used": 1.0}}
```

### Rate a Tool

```bash
python bin/uno.py rate <tool_slug> <0-5> [--comment "great tool"]
```

### Browse Servers

```bash
python bin/uno.py servers [--query "weather"] [--category search] [--limit 50]
```

### Disconnect Third-party Authorization

```bash
python bin/uno.py disconnect <server_slug>
# e.g. python bin/uno.py disconnect weather-free
```

Revokes the stored OAuth token or API key for **that one server**. After disconnect, the next `call` to the same server will return `auth_required`. Other servers are unaffected. The user can also run `python bin/uno.py logout` to wipe the entire local credential file in one step.

### API Key Management

```bash
python bin/uno.py keys list            # list active API keys
python bin/uno.py keys create          # create a new API key
python bin/uno.py keys delete <key_id> # delete an API key
```

## Tool Categories

The catalogue is grouped into 13 top-level categories. The table below lists the kinds of capability each category covers; concrete provider/server names are resolved at search time, so the agent should still `search` to find the most relevant server for a given user request.

| Category | Description |
|----------|-------------|
| `search` | Web search, crawling, and information retrieval |
| `dev` | Developer tooling (code-hosting lookups, SQL consoles, docs, error tracking) |
| `social` | Public-feed / community platforms |
| `data` | Data & analytics (knowledge graphs, computation, weather, public datasets) |
| `creative` | Generative content (image, video, music, slide decks) |
| `finance` | Market data (quotes, fundamentals, crypto) |
| `lifestyle` | Location / transit / delivery tracking |
| `productivity` | Office suites, notes, calendars, task boards |
| `media` | A/V processing (TTS, transcription, captioning) |
| `enterprise` | Business-registry and regulatory look-ups |
| `ecommerce` | Shopping & booking helpers |
| `health` | Health & wellness look-ups |
| `other` | Mail, encyclopedia, academic look-ups, misc |

## Agent Workflow

0. **Check credentials** — run `whoami` first; only login if credentials are missing/expired (see Step 0 above)
1. **Search first** — never guess tool slugs or parameters
2. **Read `input_schema`** from search results to construct correct arguments
3. **Dry-run before real call** — always run `call --dry-run` first and show the preview JSON (tool + arguments) to the user; only proceed to a real `call` after explicit user approval
4. **Search by capability** ("weather", "search", "translate"), not user intent
5. **Use `--compact`** to reduce output size (fewer tokens)
6. **If `desc` is truncated** (ends with `…`), run `tool get <slug>` for full description
7. **Check credits** with `whoami` before heavy usage — free plan has 500 daily credits
8. **Handle errors**:
   - `auth_required` with `auth_type: "api_key"` → tell user to provide an API Key (show `get_key_url` and `fields` from response)
   - `auth_required` with `auth_url` → show `auth_url` to user to open in browser for OAuth authorization; after they complete, retry the same call
   - `tool_not_found` → search again with different keywords
   - `insufficient_credits` → inform user, show recharge page: <https://agentools.uno/pricing>
   - Connection errors (timeout, cancelled) → retry once, then inform user
9. **Rate tools** after successful calls to improve search quality
10. **When multiple servers offer the same capability** (e.g. two weather providers or two market-data providers), prefer the one with higher `calls_7d` or `rating` in stats
11. **Never execute destructive actions silently.** If a tool's `input_schema` describes a write / send / purchase-class action, the agent must summarize the intended action in natural language and get explicit user confirmation before calling

## Output Format

- Call success: `{"success": true, "data": {...}, "meta": {"latency_ms": N, "credits_used": N}}`
- Other success: `{"success": true, "data": {...}}`
- Error: `{"error": "description", "hint": "...", ...}`, non-zero exit code

## Detailed Help

```bash
python bin/uno.py --help
python bin/uno.py search --help
python bin/uno.py call --help
```

## API Base URL

Prefer `https://agentools.uno`. The CLI default `https://clawdtools.uno` still serves `/v1` and `/mcp`. Override with `--base-url` or env var `UNO_API_URL`. Do not use `https://clawtools.uno` (typo host; redirects drop `Authorization`).
