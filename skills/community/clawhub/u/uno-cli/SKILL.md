---
name: uno-cli
description: "Uno CLI — Agent Tool Gateway via command line. 2000+ real-world tools accessible with two commands: search → call. Features Device Code OAuth (via ClawdChat SSO), hybrid search (keyword/semantic), tool calling with auto-auth, rating, and multi-account management. Use when: user needs to call external tools/APIs; or needs real-time info from services like weather, search, maps, finance, etc."
homepage: https://clawdtools.uno
metadata: {"emoji":"◆","category":"tools","api_base":"https://clawdtools.uno","version":"0.1.0"}
---

# Uno CLI

Access 2000+ real-world tools via command line. Zero install (Python 3.8+ stdlib only).

## Prerequisites

- Python 3.8+ (pre-installed on most systems)
- CLI script included: `bin/uno.py` — no extra install needed

CLI path (relative to this file): `bin/uno.py`

## Authentication

Login once before first use. Credentials are stored in `~/.uno/credentials.json`.

```bash
# Option A: Two-step login (recommended for agents — non-blocking)
python bin/uno.py login --start
# → Returns JSON: {"status": "pending", "verification_uri_complete": "https://...", "device_code": "xxx", ...}
# Show the URL to the user. After they authorize in a browser:
python bin/uno.py login --poll <device_code>
# → {"success": true, "name": "...", "email": "..."}

# Option B: One-shot interactive (for terminal users — blocks until authorized)
python bin/uno.py login

# Option C: Direct API Key
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

Uno uses **Device Code Flow** with **ClawdChat SSO**:

1. `login --start` requests a device code from Uno server
2. The returned `verification_uri_complete` URL opens a page where the user logs in via ClawdChat
3. After authorization, `login --poll` retrieves an API key
4. Works perfectly for mobile scenarios (e.g., user on phone with OpenClaw)

## Command Reference

All commands output pretty-printed JSON by default. Add `--compact` for single-line JSON (easier for programmatic parsing).

### Status

```bash
python bin/uno.py whoami               # current user info (credits, plan, keys)
python bin/uno.py health               # server health check
```

### Search Tools

```bash
python bin/uno.py search "weather" [--limit 10] [--mode hybrid|keyword|semantic] [--category dev] [--server weather-free]
```

Returns tools with `input_schema` (JSON Schema) — use it to construct correct arguments.

### Tool Details

```bash
python bin/uno.py tool get <tool_slug>
# e.g. python bin/uno.py tool get amap-maps.maps_weather
```

### Call a Tool

```bash
python bin/uno.py call <tool_slug> --args '{"city":"Beijing"}'
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
# e.g. python bin/uno.py disconnect github
```

Revokes the stored OAuth token or API key for a server. After disconnect, the next `call` will return `auth_required` again.

### API Key Management

```bash
python bin/uno.py keys list            # list active API keys
python bin/uno.py keys create          # create a new API key
python bin/uno.py keys delete <key_id> # delete an API key
```

## Agent Workflow

1. **Search first** — never guess tool slugs or parameters
2. **Read `input_schema`** from search results to construct correct arguments
3. **Search by capability** ("weather", "search", "translate"), not user intent
4. **Use `--compact`** to reduce output size (fewer tokens)
5. **If `desc` is truncated** (ends with `…`), run `tool get <slug>` for full description
6. **Check credits** with `whoami` before heavy usage — free plan has 100 daily credits
7. **Handle errors**:
   - `auth_required` with `auth_type: "api_key"` → tell user to provide an API Key (show `get_key_url` and `fields` from response)
   - `auth_required` with `auth_url` → show `auth_url` to user to open in browser for OAuth authorization; after they complete, retry the same call
   - `tool_not_found` → search again with different keywords
   - `insufficient_credits` → inform user, show `recharge_url`
   - Connection errors (timeout, cancelled) → retry once, then inform user
8. **Rate tools** after successful calls to improve search quality
9. **When multiple servers offer the same capability** (e.g., `github` vs `github-api`), prefer the one with higher `calls_7d` or `rating` in stats

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

Default: `https://clawdtools.uno`. Override with `--base-url` or env var `UNO_API_URL`.
