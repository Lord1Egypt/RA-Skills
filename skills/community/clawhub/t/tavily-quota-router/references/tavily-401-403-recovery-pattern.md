# Tavily 401/403 → 1-Hour Temporary Cooldown (Recovery Pattern)

**Status**: Applied 2026-07-17. Verified end-to-end with fake-key test.

## Why 401/403 should NOT permanently disable a key

The router used to write `disabled: true` on any 401 or 403, and the key stayed disabled until a human ran `reset-month`. The user flagged this on 2026-07-17:

> "401/403 行为不变（永久 disable）这个不一定吧...这种做个时间长点的冷却，过了冷却时间再检查，不要直接打死永不检查"

The intuition is right: **Tavily keys frequently recover** without anyone touching them. Three real recovery paths:

1. **Monthly quota rollover.** Plan limits reset on the 1st of each month. A 403 "quota exhausted" on the 30th is auto-resolved on the 1st. Permanent disable for 1+ day is fine; permanent disable for 30 days is wrong.
2. **Account reactivation.** A user might reactivate a paused Tavily account, rotate a key after a security incident, or pay an overdue invoice. None of those is visible to the router.
3. **Provider-side transient bug.** Tavily has had brief auth endpoint outages (analogy: any large SaaS). Permanent disable on a transient 401 is wrong.

## Design

- `AUTH_COOLDOWN_SECONDS = 3600` (1 hour) — constant in `scripts/tavily_multi_key.py`
- On 401 or 403, `mark_error(...)` is called with `disable=False, retry_after_seconds=3600`
- `choose_key` skips keys where `cooldown_until > now()`, so the failing key is naturally excluded from the next `cmd_search`
- After 1 hour, `cooldown_until < now()`, the key is back in the candidate pool, and the next `cmd_search` will **re-probe it** (it might be alive now)
- The "cost" of re-probing is one extra search attempt. If it 401s again, the cooldown is reset to 1h from the new failure time. This is a textbook **exponential-backoff lite** — bounded retry, no infinite loop.

## Verification (fake-key test, 2026-07-17)

```bash
# Set all keys to a fake one to force 401
python3 -c "
import json
cfg = json.load(open('config/keys.json'))
cfg['keys'] = [{'key': 'tvly-fake-key-not-real-1234567890', 'account': 'fake', 'notes': 'test 401'}]
json.dump(cfg, open('config/keys.json', 'w'), indent=2)
"
python3 scripts/tavily_multi_key.py search --query 'ping' --count 1
# → {"ok": false, "tried": [{"error": "HTTP 401 (auth error, retry in 1h)", "retry_after_seconds": 3600, ...}]}

# Inspect quota.json: cooldown_until should be ~now+3600s, disabled should be False
cat state/quota.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
k = d['keys'][0]
print('disabled:', k['disabled'])         # → False
print('cooldown_until:', k['cooldown_until'])
print('last_error:', k['last_error'])     # → HTTP 401 (auth error, retry in 1h)
"

# Restore real keys (NEVER skip this step — see "NEVER modify keys.json" pitfall)
```

## Anti-pattern this fixes

The old code path:

```python
# Old (BAD — leaves the key dead forever)
disable = e.code in (401, 403)
mark_error(cfg, state, idx, msg, disable=disable)
```

The new code path:

```python
# New (GOOD — bounded retry, no permanent disable from any error path)
disable = False  # 401/403 走 1h 临时 cooldown，不永久 disable
retry_after_seconds = AUTH_COOLDOWN_SECONDS if e.code in (401, 403) else None
if e.code in (401, 403):
    msg = f'HTTP {e.code} (auth error, retry in 1h)'
mark_error(cfg, state, idx, msg, disable=disable, retry_after_seconds=retry_after_seconds)
```

## When `disabled: true` IS appropriate

There is **one** legitimate path that still sets `disabled: true`: a human editing `state/quota.json` directly, or a future feature that asks "this key is permanently revoked, do not auto-recover." As of 2026-07-17, the router itself never sets it.

If you see `disabled: true` in `quota.json` after that date, it's either:
- Leftover from before 2026-07-17 (run `reset-month`)
- Manually set by a human
- A bug to investigate

## Related references

- `references/tavily-429-retry-after-2026-07-17.md` — the 429 sibling pattern (parse `Retry-After` header, don't use the 10-min default)
- `SKILL.md` "Key Status State Machine" — the 401/403 row now reads `→ false (was true before 2026-07-17)`
