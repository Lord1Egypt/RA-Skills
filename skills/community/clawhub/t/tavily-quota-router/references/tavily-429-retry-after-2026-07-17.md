# Tavily 429 Retry-After handling — the real fix transcript (2026-07-17)

**Context**: SKILL.md claimed on 2026-07-15 that the `mark_error(..., retry_after_seconds=None)` parameter was added and "applied". It was not. The parameter existed, but the `cmd_search` HTTPError branch did not parse `e.headers.get('Retry-After')` and did not pass it through. The router was still using the local `cooldown_minutes` (default 10 min, 600 s) for every 429, regardless of what Tavily said.

This file is the verified end-to-end fix transcript — read it before claiming any "wired through / applied / patched" status in this skill.

## 1. Tavily 429 — actual response shape

Captured on 2026-07-17 with `curl -i` against the live API:

```
HTTP/2 429
Connection: close
Content-Length: 171
Content-Type: application/json
Date: Fri, 17 Jul 2026 07:46:13 GMT
Retry-After: 60
Server: awselb/2.0

{
  "detail": {
    "error": "Your request has been blocked due to excessive requests.
              Please reduce the rate of requests.
              Verify you are using production API keys."
  }
}
```

Key facts:

- `Retry-After` is a **plain integer (seconds)**, not an HTTP-date. RFC 7231 allows both; Tavily chose integer.
- The body has **no `retry_after` field**. The header is the only signal.
- The body says "use production keys" — a hint that dev keys are aggressively rate-limited.

## 2. Tavily Python SDK behavior

`from tavily import TavilyClient, UsageLimitExceededError` — inspecting the SDK source:

```python
if response.status_code == 429:
    raise UsageLimitExceededError(detail)
```

The SDK **does not** read `Retry-After`, **does not** parse the body for a retry hint, and **does not** auto-retry. It just raises. The exception class has no `retry_after` attribute. If the official SDK ignores it, the routing-of-callback logic must be our own.

## 3. The fix — minimal patch to `cmd_search`

Before (line 353 of `scripts/tavily_multi_key.py`, on 2026-07-17):

```python
except urllib.error.HTTPError as e:
    msg = f'HTTP {e.code}'
    disable = e.code in (401, 403)
    tried.append({'index': idx, 'key': mask(key), 'error': msg, 'disabled': disable})
    mark_error(cfg, state, idx, msg, disable=disable)
```

After:

```python
except urllib.error.HTTPError as e:
    msg = f'HTTP {e.code}'
    disable = e.code in (401, 403)
    # 429 时解析 Tavily 返回的 Retry-After header (单位: 秒)
    retry_after_seconds = None
    if e.code == 429:
        ra = e.headers.get('Retry-After') if e.headers else None
        if ra:
            try:
                retry_after_seconds = int(ra)
            except (TypeError, ValueError):
                pass
        if retry_after_seconds:
            msg = f'HTTP {e.code} (retry in {retry_after_seconds}s)'
    tried.append({'index': idx, 'key': mask(key), 'error': msg, 'disabled': disable,
                  'retry_after_seconds': retry_after_seconds})
    mark_error(cfg, state, idx, msg, disable=disable, retry_after_seconds=retry_after_seconds)
```

~13 lines added. The existing `mark_error(..., retry_after_seconds=...)` parameter (added 2026-07-15) was already there — only the caller was missing.

## 4. 4-step verification (mandatory after every "fix")

This is the SOP — do not trust any "wired through" claim without running all four:

| Step | Command | What it proves |
|---|---|---|
| 1. `py_compile` | `python3 -c "import py_compile; py_compile.compile('scripts/tavily_multi_key.py', doraise=True)"` | syntax is valid |
| 2. `reset-month` | `python3 scripts/tavily_multi_key.py reset-month` | state is clean (no stale cooldowns from earlier bursts) |
| 3. trigger 429 | one key × 20-30 concurrent requests, stop on first 429 | the new code path actually runs |
| 4. read quota.json | parse `state/quota.json`, compare `cooldown_until - now` vs Tavily's `Retry-After` | the parsed value actually reached the state file |

The previous "applied 2026-07-15" claim in this skill failed step 4 — the parameter was added but never called, so the state file never had a `cooldown_until` derived from `Retry-After`.

## 5. End-to-end transcript on 2026-07-17

```
1. py_compile → ✅
2. reset-month → all 4 keys cooldown=None, disabled=False
3. trigger 429:
   $ python3 -c "..." with 30 concurrent requests against keys[0]
   → got 429, Retry-After: 60
4. router search:
   $ python3 scripts/tavily_multi_key.py search --query 'ping' --count 1
   {
     "ok": false,
     "error": "no available key",
     "tried": [
       {"index": 0, "error": "HTTP 429 (retry in 60s)", "retry_after_seconds": 60},
       {"index": 1, "error": "HTTP 429 (retry in 60s)", "retry_after_seconds": 60},
       ...
     ]
   }
5. quota.json after:
   key[0] cooldown_until=2026-07-17T15:51:08  (now + 50s, not now + 600s)
   key[1] cooldown_until=2026-07-17T15:51:09  (now + 51s)
   key[2] cooldown_until=2026-07-17T15:51:10
   key[3] cooldown_until=2026-07-17T15:51:11
6. sleep 50, retry search → ok=true, key_index=0
```

`cooldown_until - now ≈ 50s`, not `600s`. Fix verified.

## 6. The "wasted quota" lesson (老大 2026-07-17: "神经病啊，逮着一个测不就行了")

Initial verification attempt burst **all 4 keys × 100 concurrent = 400 requests** to "make sure" the test caught a 429. Each key ended up with `cooldown_until = now + ~600s` (the `cooldown_minutes: 0.5` config was *not* used because `retry_after_seconds` was being ignored). All 4 keys in cooldown = the entire router is dead for 10 minutes. 100 quota wasted on each of 4 keys = 400 quota wasted.

**Correct pattern** when the goal is to *trigger* a 429 (not to do real work):

```
# one key, one burst, stop on first 429
with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
    it = ex.map(fire_one_key, range(30))
    for r in it:
        if r[1] == 429:
            break  # ← stop immediately
```

30 requests to one key. One key in cooldown. ~30 quota spent, not 400. The router-internal `search` call will still give you a 429 to verify with — it tries the next key in failover and you can read the error message + retry_after_seconds from the JSON output.

## 7. Why this SKILL.md lied (meta-lesson)

The 2026-07-15 commit that added `mark_error(..., retry_after_seconds=None)` also updated the SKILL.md to say "applied". But the only call site in `cmd_search` was not updated. The doc accurately described an *intended* state that was never reached. The two failure modes:

1. **Doc-driven fix** — write the SKILL.md first ("here's what the fix looks like"), then write the code. If you run out of energy / time / context, the doc lies.
2. **No end-to-end verification** — `mark_error(retry_after_seconds=60)` worked in unit tests, but the call site `mark_error(cfg, state, idx, msg, disable=disable)` was not updated to pass it through.

**Counter-rule**: any "applied / wired / patched" claim in a SKILL.md must be backed by the 4-step verification (table in section 4). If you can't run all 4 steps, write the claim as "intended" or "to be verified", not "applied".

This is the same class of error as the 7/16 PR #64252 false-memory incident (`commit_count=1` → "no new pushes", missing force-push) — **local state does not match the actual state of the thing being claimed**. Always check the source, never the doc.
