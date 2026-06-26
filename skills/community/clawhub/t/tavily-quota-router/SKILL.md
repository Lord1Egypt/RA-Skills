---
name: tavily-quota-router
description: >-
  Tavily quota-aware multi-key search router. Use when you want reliable Tavily-backed web search across multiple API keys, automatic failover for invalid/rate-limited keys, official usage-based routing via Tavily's /usage endpoint, and status visibility for each key. Prefer this when the user explicitly wants multi-key Tavily routing instead of OpenClaw's built-in single-key web_search provider.
---

# Tavily Quota Router

Use this skill for **multi-key Tavily search routing**. Do not confuse it with OpenClaw's built-in `web_search` provider.

## What this skill does

- Reads multiple Tavily API keys from `config/keys.json`
- Syncs each key's real usage from Tavily's official `/usage` endpoint
- Chooses a healthy key automatically before each search
- Skips invalid, rate-limited, exhausted, or cooled-down keys
- Exposes status information for every configured key

## Best use cases

Use this skill when the user wants any of the following:

- Multiple Tavily API keys with automatic routing
- Quota-aware Tavily search instead of single-key search
- Better resilience when one key becomes invalid or temporarily unavailable
- Visibility into per-key usage and remaining plan quota

## Files

- `config/keys.json` - active multi-key configuration
- `config/keys.example.json` - configuration example
- `state/quota.json` - local runtime state and cooldown markers
- `scripts/tavily_multi_key.py` - core router script

If `config/keys.json` is still empty, copy the structure from `config/keys.example.json` and add real keys before searching.

## Commands

Show status:

```bash
python3 scripts/tavily_multi_key.py status
```

Test all keys:

```bash
python3 scripts/tavily_multi_key.py test-keys
```

Search:

```bash
python3 scripts/tavily_multi_key.py search --query 'OpenClaw docs' --count 5
```

Reset only local state:

```bash
python3 scripts/tavily_multi_key.py reset-month
```

## Usage rules

1. Check `config/keys.json` first.
2. If no keys are configured, stop and tell the user to add keys.
3. Prefer the bundled script over ad-hoc Tavily requests.
4. Be clear that this is a **multi-key Tavily wrapper**, not the built-in OpenClaw `web_search` provider.
5. If the user later wants this behavior wired into their default search stack, handle that as a separate configuration task instead of silently mutating the built-in provider.

## Routing policy

- Sync usage via Tavily's official `/usage` endpoint
- Prefer keys with more remaining quota
- Prefer lower `search_usage` when remaining quota is comparable
- Disable keys on `401/403`
- Cool down keys temporarily on transient errors like `429`, `5xx`, or timeouts

## Example config

```json
{
  "cooldown_minutes": 10,
  "keys": [
    "tvly-xxx1",
    "tvly-xxx2"
  ]
}
```

## Notes

- This skill relies on Tavily's official API responses for usage and plan data.
- Local state is only used for cooldown/error handling and last synced snapshots.
- This skill is designed for controlled multi-key routing, not anonymous/public key distribution.
