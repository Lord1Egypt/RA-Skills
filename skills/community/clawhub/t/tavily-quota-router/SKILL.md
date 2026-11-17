---
name: tavily-quota-router
description: >-
  Tavily quota-aware multi-key search router. Load BEFORE issuing any web_search call (Tavily is the default backend in this Hermes install, and burst searches burn rate limits within seconds). Use when you want reliable Tavily-backed web search across multiple API keys, automatic failover for invalid/rate-limited keys, official usage-based routing via Tavily's /usage endpoint, and status visibility for each key. Critical rules: max 1 web_search per assistant turn, stop on first 429, do not retry within cooldown.
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

- `config/keys.json` - active local multi-key configuration (do not publish with real keys)
- `config/keys.example.json` - editable example configuration
- `config/keys.publish.json` - safe publish template for packaging/release
- `state/quota.json` - local runtime state and cooldown markers
- `scripts/tavily_multi_key.py` - core router script

If `config/keys.json` is still empty, copy the structure from `config/keys.example.json` and add real keys before searching.

## Config format

### Recommended format (v2)

```json
{
  "format_version": 2,
  "cooldown_minutes": 10,
  "keys": [
    {
      "key": "tvly-your-key-1",
      "account": "your-email@example.com",
      "notes": "main account"
    },
    {
      "key": "tvly-your-key-2",
      "account": "backup@example.com",
      "notes": "backup key"
    }
  ]
}
```

### Legacy format (still supported)

```json
{
  "cooldown_minutes": 10,
  "keys": [
    "tvly-your-key-1",
    "tvly-your-key-2"
  ]
}
```

### Automatic migration

Legacy string-array configs are still supported. On first run, the router will automatically migrate the config to the v2 object format and write it back to `config/keys.json`.

If an older config used `source`, it will be mapped into `account` during migration.

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

## 🔴 BURST GUARD — HARD LIMIT, NON-NEGOTIABLE

**Before issuing ANY `web_search` call, read this:**

1. **Max 1 `web_search` per assistant turn.** No exceptions. If you find yourself about to issue a second one in the same reply, stop — re-rank your queries and pick the one most likely to land.
2. **Tavily rate-limits per-key, not per-account.** With 4 healthy keys, parallel bursts still 429 ALL of them within seconds. Quota ≠ headroom. A 4000-call/month quota burns to zero in 5 seconds if you fire 30 calls in parallel.
3. **First 429 = hard stop.** Do not retry, do not "try a different key," do not switch to `web_extract`. Report to the user: backend in cooldown, remaining minutes, ask whether to wait.
4. **Burst detection diagnostic:** if `state/quota.json` shows multiple keys with `cooldown_until` within seconds of each other, you caused the cascade. Acknowledge it, don't blame Tavily.
5. **The user's words when this fires (2026-07-09):** "我一个月4k次的搜索额度你不用不就浪费了" — followed by "你四个同时大量调用了吗". The user's point is **use the budget**, not **spend it all at once**. The intent is "don't be lazy about searching when you don't know," not "search 30 times in parallel."
6. **2026-07-17 supplement**: "逮着一个测不就行了" — when the goal is to *trigger* a 429 (e.g. to verify Retry-After handling, or to populate quota.json for a test), do **NOT** burst all 4 keys at once. Pick one key (`cfg['keys'][0]`), fire 20–30 concurrent requests, catch the first 429, **stop immediately**. The router-internal search call already gives you a 429 for free once one key is in cooldown (it tries the next key in the failover loop). One key × one burst = ~30 quota spent. Four keys × "make sure" burst = 120+ quota wasted. The user will call this "神经病" (and they will be right).

**Operational check before every `web_search`:**

```
[ ] Did I already search in this turn?           → STOP, use that result
[ ] Could this query be batched with another?    → combine into one call
[ ] Have I gotten a 429 in the last 10 minutes?  → STOP, report cooldown
[ ] Would a local lookup (config/env/file) do?   → do that first
[ ] Am I searching because I genuinely don't know (good), or because
    I'm afraid to commit to an answer (bad)?      → if "bad," answer first
```

## ⚠️ What `cooldown_minutes` actually means

**It is NOT Tavily's official limit.** It is a **local config field** in `config/keys.json`:

```json
{
  "cooldown_minutes": 10,    // ← user-configurable, default = 10
  "keys": [...]
}
```

**Tavily's actual rate limits** (per Tavily official docs `docs.tavily.com/documentation/rate-limits`):

| Environment | RPM (requests/minute) |
|---|---|
| Development (`tvly-dev-...` prefix) | **100 RPM** |
| Production (`tvly-prod-...` prefix) | **1000 RPM** |

**429 response includes a `Retry-After` header** telling the client how many seconds to wait. ~~The router currently **ignores this header** and uses the local `cooldown_minutes` instead.~~ **As of 2026-07-17 the router honors this header** — `cmd_search` parses `e.headers.get('Retry-After')` on 429 and passes it to `mark_error` as `retry_after_seconds`. Local `cooldown_minutes` is now only the worst-case fallback when the header is missing or unparseable. See "Code path (wired through search path on 2026-07-17)" below for the verification transcript.

- **老大 (2026-07-14): "10 分钟不合理" / "改掉很不合理"** — implication: 10 min is way longer than Tavily's actual recovery time. A single dev key 429 typically clears in **30s–2min**, not 10 min. ~~Until someone rewrites the router to honor `Retry-After`, set `cooldown_minutes` to **1–2** for dev keys~~ — this guidance is now superseded (router honors `Retry-After` as of 2026-07-17). The `cooldown_minutes` knob remains useful only as the fallback for 5xx/timeout and for 401/403 auth-error cooldown default. Current config value `cooldown_minutes: 0.5` (= 30s) is the historical sweet spot.

- **老大 (2026-07-15): "让你等几秒，你等个十秒二十秒的不就可以再试一下了吗"** — the **minimal-retry** principle, simpler than full retry-after parsing: if a 429 fired within the last 10-30 seconds, just wait that long and retry. Tavily dev key 429s typically clear in **10-20s**, not 10 minutes. Two paths to honor this:

  1. **Config knob (verified 2026-07-15)**: set `cooldown_minutes: 0.5` (= 30 seconds). Router accepts float `cooldown_minutes` and treats < 1 minute as fractional seconds via `timedelta(seconds=minutes * 60)`. Verified 4-key cooldown went from 11:25 → recovered by 11:26 after the change.

  2. **Code path (wired through search path on 2026-07-17)**: `mark_error(cfg, state, idx, msg, disable=False, retry_after_seconds=None)` — new optional kwarg. The `cmd_search` HTTPError branch now parses `e.headers.get('Retry-After')` (integer seconds, per Tavily's actual 429 response) and passes it through. **Verified end-to-end on 2026-07-17**: hitting key[0] with 30 concurrent requests triggered 429, router captured `Retry-After: 60`, set `cooldown_until = now + 60s` (not 600s), and the key was queryable again after a single `sleep 50` — matching the documented behavior. Before this fix, SKILL.md claimed "applied 2026-07-15" but the search call path was NOT actually wired through — see `references/tavily-429-retry-after-2026-07-17.md` for the full diff and verification transcript.  **Operational rule (mandatory after every fix like this):** do not trust SKILL.md claims about "applied / wired / patched" without re-running the 4-step verification (`py_compile` + `reset-month` + trigger 429 + read quota.json `cooldown_until`). The bug pattern is: someone adds the parameter, writes the doc, but never calls the parameter from the search path. If the verification step is skipped, you end up with a skill that lies about its own behavior.

  **Operational rule**: when user reports "I just need it to retry in 10-20s, not 10 minutes", first check if the actual recovery time is sub-minute by directly `curl https://api.tavily.com/search -H "Authorization: Bearer $KEY" -d '{"query":"ping"}'`. If it returns 200, the router is over-conservative — set `cooldown_minutes: 0.5` (or lower) and confirm.

**Workaround to change it:** edit `~/.hermes/skills/openclaw-imports/tavily-quota-router/config/keys.json` → `cooldown_minutes` field. Takes effect on next router run.

## Usage rules

1. Check `config/keys.json` first.
2. If no keys are configured, stop and tell the user to add keys.
3. Prefer the bundled script over ad-hoc Tavily requests.
4. Be clear that this is a **multi-key Tavily wrapper**, not the built-in OpenClaw `web_search` provider.
5. If the user later wants this behavior wired into their default search stack, handle that as a separate configuration task instead of silently mutating the built-in provider.
6. **Never fire multiple `web_search` calls in parallel inside the same assistant turn.** Tavily rate-limits per-key, so a 3-call burst will 429 all your healthy keys at once (see pitfalls). Serialize with `sleep 2` between calls, or batch queries. The router saves you from quota exhaustion, not from rate-limit cascades.

## Routing policy

- Sync usage via Tavily's official `/usage` endpoint
- Prefer keys with more remaining quota
- Prefer lower `search_usage` when remaining quota is comparable
- Disable keys on `401/403` — **NO LONGER PERMANENT** (changed 2026-07-17, see below)
- Cool down keys temporarily on transient errors like `429`, `5xx`, or timeouts
- 401/403 → **1-hour temporary cooldown** (`AUTH_COOLDOWN_SECONDS = 3600`), then `choose_key` auto-reprobes. Disabled state is reserved for user-initiated `reset-month` only. The previous "permanent disable" behaviour was a real bug: Tavily keys frequently recover (account reactivated, monthly quota rollover, rotated by provider) and permanent disable means a human has to notice and run `reset-month` — defeating the point of a router.

## Example config

```json
{
  "format_version": 2,
  "cooldown_minutes": 10,
  "keys": [
    {
      "key": "tvly-xxx1",
      "account": "main@example.com",
      "notes": "main account"
    },
    {
      "key": "tvly-xxx2",
      "account": "backup@example.com",
      "notes": "backup key"
    }
  ]
}
```

## Notes

- This skill relies on Tavily's official API responses for usage and plan data.
- Local state is only used for cooldown/error handling and last synced snapshots.
- This skill is designed for controlled multi-key routing, not anonymous/public key distribution.
- Do not publish real API keys inside `config/keys.json`; keep only examples/templates in distributable skill packages.
- Recommended release flow: keep real local secrets in `config/keys.json`, keep `config/keys.example.json` / `config/keys.publish.json` as safe templates, and exclude `config/keys.json` plus `state/quota.json` from published artifacts.

## Key Status State Machine

Each key in `state/quota.json` has 4 mutable fields: `disabled`, `cooldown_until`, `last_error`, `last_usage`. They change only on these events:

| Trigger | `disabled` | `cooldown_until` | `last_error` | Source code |
|---|---|---|---|---|
| `/usage` success | → `false` | — | → `null` | `sync_all_usage` ok branch |
| HTTP 401/403 | → `false` (**was `true` before 2026-07-17**) | → now + 3600s (`AUTH_COOLDOWN_SECONDS`) | → `"HTTP 4xx (auth error, retry in 1h)"` | `sync_all_usage` + `cmd_search` HTTPError branch |
| 429 | → `false` | → now + `Retry-After` (Tavily 实际值) 或 `cooldown_minutes` | → `"HTTP 429 (retry in Ns)"` | `cmd_search` HTTPError branch (wired 2026-07-17) |
| 5xx / timeout | → `false` | → now + `cooldown_minutes` (默认 0.5) | → error msg | `sync_all_usage` + `cmd_search` generic except |
| Search success | → `false` | → `null` | → `null` | `mark_success` (current key only) |
| Month rollover | reset to defaults | reset | reset | `normalize_state` (passive) |

**Critical (2026-07-17 update)**: `disabled: true` is no longer set by any error path. Only user-initiated `reset-month` or manual JSON edit can set it. This means 401/403 keys auto-recover after 1 hour via `choose_key` reprobing. If you see `disabled: true` in `quota.json`, that is **leftover from before 2026-07-17** — `reset-month` will clear it.

**Critical: only `test-keys` / `status` re-evaluate ALL keys.** A `search` call only cleans the one it actually used — siblings with `cooldown_until` in the future stay skipped until time passes.

## Pitfalls

- **`disabled: true` is sticky across restarts.** 401'd keys stay disabled in `state/quota.json` until the next `test-keys` run clears them. A key that 401'd months ago may have recovered (rotated, account reactivated) — never trust stale `disabled` markers; run `test-keys` first to refresh.
- **`last_sync_at` ≠ real-time health.** The state file snapshots when `/usage` was last called. If it's months old, key health may have changed in either direction (recovered or newly banned). Always refresh before reasoning about a key's status.
**老大 (2026-07-14) "你的检查机制是什么" — answer:** when web_search fails or router reports "no available key", the FIRST move is always `cat state/quota.json | python3 -m json.tool` and compute `now() - cooldown_until`. Reporting "quota exhausted" or "Tavily down" without this is the same class of error as "I assumed it was Ollama" — verify before stating. The router's error message is a **local cache state**, not a Tavily API verdict.

- **`cooldown_until` ≠ backend dead.** A cooldown marker was written after a single 429 burst, but the upstream may have recovered seconds later. **Never report "all keys exhausted / Tavily down" based on `state/quota.json` alone.** Before declaring the backend dead, parallel-curl each key against `https://api.tavily.com/search` directly (bypassing the router). If all return 200, the state is stale — run `reset-month` or `test-keys` to refresh, then proceed. The router state is a local cache, not ground truth. Verified 2026-07-10: four keys with `cooldown_until` 10 min in the future were all 200 OK on direct curl; reporting "exhausted" without testing is the same class of error as "I assumed it was Ollama." Test before reporting.
- **Router 错误消息 ≠ quota 真实状态**（2026-07-14 老大原话 "怎么可能额度用完了"）。router 报 "no available key (all disabled, cooled, or quota exhausted)" 时**第一步永远是看 quota.json**，**不**直接信 router 报错。**诊断顺序**：
  1. `cat state/quota.json | python3 -c "import json,sys; d=json.load(sys.stdin); [print(k['cooldown_until'], k.get('disabled'), k.get('plan_usage'),'/',k.get('plan_limit')) for k in d['keys']]"`
  2. 对比当前时间 vs `cooldown_until` —— 如果 cooldown_until < now → **cooldown 已过**，**不是真死**
  3. 对比 `plan_usage / plan_limit` —— < 80% 不算满
  4. 直接 `curl https://api.tavily.com/search -H "Authorization: Bearer $KEY" -d '{"query":"ping"}'` 实测 → 200 = quota 正常
  5. 都过了才报告"quota 真死"；不然重试 1 次再判定

  **真实陷阱**（2026-07-14）：router 报 "all disabled, cooled, or quota exhausted"，实际 quota.json 里 4 个 key 都 `cooldown_until: 21:54`，当前 22:22 —— **cooldown 早过了 28 分钟**，月度配额只用 37/1000 (3.7%)。router **没刷新缓存**导致误判。**老大原话"你的检查机制是什么"** —— 答案是先看 quota.json，**不**信 router 报错。
- **Plaintext keys in `config/keys.json`.** Real `tvly-dev-...` keys live unencrypted on disk. The bundled `.gitignore` is a 34-byte stub — verify it actually excludes `config/keys.json` AND `state/quota.json` before sharing the directory. Default to environment variables for production deployments.

- **`cooldown_minutes` fallback only (2026-07-17 update).** Previously this pitfall read: "the router ignores `Retry-After` and uses the hard-coded config value instead". As of 2026-07-17 that is **no longer true for 429** — `cmd_search` parses `Retry-After` and feeds it through `mark_error`. The local `cooldown_minutes` is now only the fallback for: (a) 5xx/timeout, (b) 401/403 auth errors (which use `AUTH_COOLDOWN_SECONDS = 3600` not `cooldown_minutes`), (c) 429 responses with no `Retry-After` header. 老话 "10 分钟哪里规定的" / "改掉很不合理" 是当初 10-min hardcoded 的产物，现在该条款被 parsed header 替代。
- **Quota exhaustion ≠ `disabled`.** `choose_key` soft-skips keys with `plan_usage >= plan_limit` but never marks them `disabled`. They'll be picked again once quota resets (next month). Don't confuse "skipped" with "broken".
- **Cross-month auto-reset is silent.** `normalize_state` wipes all per-key state when `state.month != current_month`. If you see keys mysteriously "alive" after the 1st, that's the reset, not actual recovery.
- **Parallel `/usage` syncs also burn rate limits.** `cmd_search` calls `sync_all_usage` before every search — four consecutive `/usage` requests within seconds trigger 429 on the `/usage` endpoint even when every key is healthy and quota is barely touched. Symptom: all 4 keys enter `cooldown_until = now + 10min` after a single search, `web_search` returns "no available key" but direct curl proves all keys are 200 OK. Fix: remove the `sync_all_usage(cfg, state)` call at the start of `cmd_search` in `scripts/tavily_multi_key.py` — usage syncs lazily for the one key that actually ran a search; preemptive sync of all keys is unnecessary and harmful. After patching, run `reset-month` to clear stale cooldowns. Fix applied 2026-07-13.
- **Parallel web_search calls wipe all keys in one shot.** Tavily's free plan has per-key rate limits (not just per-account). Issuing N parallel `web_search` calls in the same tool-turn triggers N consecutive 429s: key 0 429s, the router fails over to key 1, key 1 also 429s from the burst, etc. Symptom: 4 healthy keys all enter 10-minute cooldown within seconds, even though quota is barely touched (3967/4000 remaining). **Rule of thumb: max 1 web_search per assistant turn. If you genuinely need parallel coverage, serialize them with `sleep 2` between calls, or batch queries into one search.**
- **Do NOT retry within cooldown.** The router itself reports `no available key (all disabled, cooled, or quota exhausted)`. The temptation is to "try again in case it recovered" — don't. Cooldown is 10 minutes; sleeping 60s and retrying just wastes another search call and re-triggers 429. Instead: tell the user the search backend is in cooldown, give the remaining minutes, and either (a) switch to `web_extract` against a known URL if the user has one, or (b) ask them to wait.
- **`web_extract` is also rate-limited** in this install — when Tavily is in cooldown, `web_extract` returns the same `tavily-quota-router: no available key` error. Fall back to `curl` against the target URL directly when extraction is needed but Tavily is cooling down. Do not loop `web_extract` calls waiting for recovery.
- **Symptom of an in-flight cascade (2026-07-09 incident):** four healthy keys, ~33 calls used in a single 5-second window, all return `HTTP 429` within 6 seconds of each other, `state/quota.json` shows every key with `cooldown_until = now + ~10min`. Fix: stop immediately, run `python3 scripts/tavily_multi_key.py status` once to confirm scope, report to user, do not call `web_search` again until cooldown expires.
- **Quota state hides the rate-limit reality.** `state/quota.json` shows `search_usage: 6 / plan_limit: 1000`, which looks fine, but the `cooldown_until` field tells the real story. When 429 cascades hit, every key shows `cooldown_until = now + 10min` and the router refuses all of them — wait it out, don't add more keys.
- **NEVER modify `config/keys.json` without backing it up first (2026-07-17 incident).** This file holds 4 live Tavily API keys. While testing 401 handling, the agent overwrote all 4 keys with a `tvly-fake-key-...` placeholder in order to trigger a 401, then tried to "restore" them — but the only complete record of the real keys was in the file itself (no git, no archive, no copy in the conversation). The keys were unrecoverable; the user had to regenerate all 4 from the Tavily dashboard. **Rule**: before any `json.dump` / `write_file` / `sed -i` that touches a file containing live credentials, run `cp config/keys.json config/keys.json.bak.$(date +%s)` first. The backup cost is 1 ms; the recovery cost is 4 key regenerations. This is the `trash > rm` principle applied to credential files. See `hermes-credentials-management` SKILL.md for the full procedure.

## Reference

- `references/state-machine-2026-07-08.md` — full state machine walkthrough with verified 4-key health check transcript
- `references/security-hardening.md` — environment variable migration path, .gitignore verification, key rotation policy
- `references/tavily-429-retry-after-2026-07-17.md` — Tavily 429 actual response shape, the wrong SKILL.md claim ("applied 2026-07-15") that was actually only half-wired, the verified end-to-end fix diff, and the "one-key burst, stop on first 429" verification pattern
- `references/tavily-401-403-recovery-pattern.md` — why 401/403 must use temporary 1-hour cooldown (not permanent disable), the three real-world recovery paths (monthly rollover / account reactivation / provider transient), and the fake-key verification recipe

## See also

- `hermes-auxiliary-providers` — for the broader `auxiliary.*` / `web.*` backend wiring question (vision, web_extract, web backend plugin development)
- `tavily-search` — single-key fallback if the multi-key setup is overkill
