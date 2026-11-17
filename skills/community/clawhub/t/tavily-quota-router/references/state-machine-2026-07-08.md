# State Machine Walkthrough — 2026-07-08

Captured during a real 4-key health check on老大's NAS (fnOS / Debian 12). Used to verify the key status logic in `scripts/tavily_multi_key.py` and to find the answer to "when do disabled keys get re-evaluated?".

## Setup snapshot

- 4 keys configured, all `tvly-dev-...` format (Tavily Researcher plan, 1000 quota each)
- `state/quota.json` `month: 2026-04`, `last_sync_at: 2026-04-10T14:46:xx` (3 months stale)
- Key index 3 had `disabled: true` with `last_error: "HTTP 401"` from April 10

## Verification sequence

```bash
# 1. Full health check — refreshes ALL keys
python3 scripts/tavily_multi_key.py test-keys
```

Result: **all 4 keys returned 200 from `/usage`**, including the one marked `disabled: true` in state. The `test-keys` call ran `sync_all_usage` which re-evaluates every key and resets `disabled: false`, `last_error: null` on success.

| Index | Key (masked) | Pre-state | Post-state | `/usage` | Plan | Used / Limit |
|---|---|---|---|---|---|---|
| 0 | `tvly-dev...BORr` | healthy | healthy | ✅ | Researcher | 5 / 1000 |
| 1 | `tvly-dev...rzxM` | healthy | healthy | ✅ | Researcher | 6 / 1000 |
| 2 | `tvly-dev...gjVX` | healthy | healthy | ✅ | Researcher | 3 / 1000 |
| 3 | `tvly-dev...cUnO` | `disabled: true` | healthy | ✅ | Researcher | 0 / 1000 |

```bash
# 2. Real search — confirms routing logic
python3 scripts/tavily_multi_key.py search --query "抖音小游戏开发文档" --count 3
```

Result: `key_index: 3` was picked (糖仔's key, `account: acubesugar@outlook.com`), returned 3 valid results, all from `developer.open-douyin.com` / `layaair.com`. The `mark_success` call cleared key 3's state further.

## Confirmed logic (read straight from `tavily_multi_key.py`)

### What changes `disabled`

1. **`test-keys` / `status`** — calls `sync_all_usage`, which on `/usage` success sets `state['keys'][i]['disabled'] = False`. This is the **only** path that re-evaluates keys other than the one currently in use.
2. **Search success** — `mark_success` sets `disabled = False` **only for the key that succeeded**.
3. **Cross-month rollover** — `normalize_state` wipes the whole per-key list when `state.month != current_month()`. Happens silently on the first call of each new month.

### What sets `disabled: true`

- HTTP 401 or 403 from `/search` or `/usage` → `mark_error(... disable=True)`. Stays `true` forever (across restarts, across searches) until a `test-keys` run revalidates.

### What sets `cooldown_until`

- Non-401/403 errors (429, 5xx, timeout, network) → `mark_error(... disable=False)` sets `cooldown_until = now + cooldown_minutes` (default 10min).
- `is_cooled(st)` in `choose_key` skips keys where `now() < cooldown_until`.
- Cleared on next success via `mark_success`, or on `reset-month`.

## Common confusion clarified

**Q: A key was 401'd 3 months ago. Did it auto-recover?**
**A:** Yes — the April → May → June → July month rollovers silently reset its `disabled: true` marker. The state file in front of you was just stale, not actively wrong. But the key may have been re-banned again in the meantime. Only `test-keys` tells you for sure.

**Q: Why didn't my successful search fix key #2's `disabled: true`?**
**A:** `mark_success` only updates the index that was actually used. Keys sitting at `disabled: true` in state are invisible to `choose_key` (line 196: `if st.get('disabled'): continue`), so they never get selected, so they never get cleaned. Catch-22. Use `test-keys`.

## Verified 4-key transcript (raw, abridged)

```
test-keys output → all 4 ok, all plan=Researcher
search "抖音小游戏开发文档" → key_index=3, 3 results, ok=true
  [1] 抖音小游戏 - LAYA引擎官网
      https://layaair.com/3.x/doc/released/miniGame/byteDance/readme.html
  [2] 小游戏_抖音开放平台
      https://developer.open-douyin.com/docs/resource/zh-CN/mini-game/develop/api/mini-game/bytedance-mini-game
  [3] 小游戏文档指引 - 抖音开放平台
      https://developer.open-douyin.com/docs/resource/zh-CN/mini-game/guide/overview
```

## Operational recipe

```bash
# Weekly or when in doubt: full health check
python3 scripts/tavily_multi_key.py test-keys

# Per-call: just search (auto-failover handles transient issues)
python3 scripts/tavily_multi_key.py search --query "..." --count N

# After schema upgrades or state corruption: reset local cache
python3 scripts/tavily_multi_key.py reset-month
```

Do not publish `state/quota.json` — it contains `last_sync_at` timestamps and key indexes that, combined with other leaks, can fingerprint the user's Tavily account structure.
