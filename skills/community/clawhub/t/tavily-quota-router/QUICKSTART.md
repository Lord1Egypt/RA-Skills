# Tavily Quota Router — Quickstart

Get up and running in **5 commands** (≈ 2 minutes).

## Who needs this

This skill solves **one specific problem**: you have multiple Tavily API keys, and you don't want a single 429 to block your agent. It auto-rotates across healthy keys, honors Tavily's rate-limit headers, and recovers from transient auth errors automatically.

If you have **only 1 key** or use Tavily **< 100 times/month**, **you don't need this skill** — call `https://api.tavily.com/search` directly with your key.

### ✅ Use this skill when

- You have **2 or more Tavily API keys** (multiple accounts, or shared across teammates) and want to avoid a single key's quota or rate-limit blocking your agent
- Your agent does **burst searches** — issuing 5-10 searches in quick succession will reliably 429 a single dev key
- You use Tavily **>500 times/month** and one key's monthly quota is at risk of running out mid-month
- You want **observability** into per-key health (`status` command shows usage, cooldown, errors)
- You want graceful **automatic failover**: when key A 429s, the next search automatically uses key B

### ❌ Don't use this skill when

- **You only have 1 Tavily key** — direct HTTP calls are simpler, this skill adds a layer you don't need
- **You use Tavily <100 times/month** — a single key's 1000-search monthly quota will cover you, and you won't hit 100 RPM
- **You need production-grade high concurrency** (≥100 req/sec sustained) — use the Tavily Python SDK with your own queueing and a proper HTTP client; this script is `urllib.request` based and not optimized for that scale
- **You want permanent key disable on auth errors** — as of v1.1.0 the router uses 1-hour temporary cooldown and auto-reprobes instead; if you genuinely want permanent disable, fork the script and set `AUTH_COOLDOWN_SECONDS` very high

### What you'll see if you're in the "don't use" camp

If you install this anyway with one key and a light usage pattern, you'll notice the `status` command showing a lot of `None` quota fields and `last_sync_at` updating every search call. That's the router trying to be helpful, but the per-search `/usage` sync is wasted work for low-volume users.

---

## Step 1 — Install

The skill is already installed at `~/.hermes/skills/openclaw-imports/tavily-quota-router/` in this Hermes install. Verify:

```bash
ls ~/.hermes/skills/openclaw-imports/tavily-quota-router/
```

You should see: `SKILL.md`, `scripts/tavily_multi_key.py`, `config/`, `state/`.

---

## Step 2 — Add your Tavily keys

Copy the example file and edit it:

```bash
cp ~/.hermes/skills/openclaw-imports/tavily-quota-router/config/keys.example.json \
   ~/.hermes/skills/openclaw-imports/tavily-quota-router/config/keys.json
```

Open `config/keys.json` and replace `tvly-your-key-1` / `tvly-your-key-2` with your real keys from <https://app.tavily.com/keys>. **Save and exit.**

Format:
```json
{
  "format_version": 2,
  "cooldown_minutes": 0.5,
  "keys": [
    { "key": "tvly-dev-XXXXX...", "account": "main@example.com", "notes": "main account" },
    { "key": "tvly-dev-YYYYY...", "account": "backup@example.com", "notes": "backup" }
  ]
}
```

> **Note**: `cooldown_minutes: 0.5` is 30 seconds. This is intentional — when Tavily returns a 429 with `Retry-After: 60`, the router honors that exact value (60s), not this default. This default is only used as the fallback for 5xx / timeout errors.

---

## Step 3 — Test your keys

```bash
python3 ~/.hermes/skills/openclaw-imports/tavily-quota-router/scripts/tavily_multi_key.py status
```

You should see all keys reporting `ok: true` with quota numbers like `plan_usage: 55 / plan_limit: 1000`. If any key shows `error`, double-check the key string.

---

## Step 4 — Run a search

```bash
python3 ~/.hermes/skills/openclaw-imports/tavily-quota-router/scripts/tavily_multi_key.py \
    search --query "your query here" --count 5
```

Output is JSON with `results`, `usage`, and the `key_index` that handled the request.

---

## Step 5 — Watch quota over time

After a few searches, run `status` again — you'll see `search_usage` tick up and `last_sync_at` update. The router picks the **key with the most remaining quota** for the next request automatically.

To force-clear all cooldown markers (e.g. after fixing a quota issue on Tavily's side):

```bash
python3 ~/.hermes/skills/openclaw-imports/tavily-quota-router/scripts/tavily_multi_key.py reset-month
```

---

## What the router handles for you

| Situation | What happens |
|---|---|
| 1 key returns 429 with `Retry-After: 60` | Router uses that key again after 60s |
| All keys are in cooldown | Router returns `"no available key"` with the `tried` list showing why each failed |
| A key returns 401 or 403 (auth error) | Router puts it on a 1-hour cooldown, then auto-reprobes — does **not** permanently disable |
| One key hits its monthly quota limit | Router skips it until next month rollover |
| Tavily's `/usage` endpoint itself rate-limits | The router stops calling `/usage` mid-search (lazy sync) to avoid burning your rate budget |

## When something goes wrong

The first thing to check is **always** `state/quota.json`, not the router's error message. The router message is a local cache; `quota.json` is ground truth.

```bash
cat ~/.hermes/skills/openclaw-imports/tavily-quota-router/state/quota.json | python3 -m json.tool
```

Common states:

- `cooldown_until` is in the past → cooldown already expired, the router's "no available key" message is stale. Run `reset-month` to clear it.
- `disabled: true` → leftover from before 2026-07-17. Run `reset-month` to clear it.
- `last_error: "HTTP 401 (auth error, retry in 1h)"` → key was bad; wait 1 hour or replace the key.

## Privacy

`config/keys.json` lives unencrypted on disk. The skill's bundled `.gitignore` excludes this file, but treat it like a password anyway. For multi-user servers, prefer environment variables (see `references/security-hardening.md`).