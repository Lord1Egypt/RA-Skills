# Implementation plan

## Final direction

Build `zsxq-digest` as a public-friendly OpenClaw skill that summarizes Knowledge Planet updates while keeping credentials and private state local.

## Accepted constraints

1. OpenClaw may run on a VPS, home server, or Mac mini while the user logs in from a phone or another machine.
2. Some environments may not have browser capability.
3. The skill must never fail silently.
4. Public sharing requires low dependency weight and strong secret isolation.
5. Knowledge Planet is hostile to heavy automation and frequent polling.

## Access priority

### 1. Local private session mode
- Default and preferred.
- Use a locally stored gitignored token/session/cookie file centered on `zsxq_access_token`.
- Best for remote-host deployments and cross-device usage.

### 2. Browser relay mode
- Secondary path.
- Use OpenClaw browser tooling with `profile="chrome"` when the user can attach a logged-in tab.
- Best for local environments, recovery, and manual verification.
- Browser collection strategy for MVP: use the aggregated update feed and filter locally by configured planet names.

### 3. Fetch fallback mode
- Viability probe only.
- Attempt only when browser is unavailable and a proven authenticated endpoint or export path exists.
- If the result is shell HTML, login wall, or incomplete content, fail with `FETCH_UNSUPPORTED`.
- Do not treat this as a standard supported mode in MVP.

## Runtime state

Keep local runtime state outside the public release:

```text
state/
  cursor.json
  session.token.json
  cookies.json
  config.json
```

## Required explicit errors

- `NOT_LOGGED_IN`
- `LOGIN_REQUIRED_QR`
- `TAB_NOT_FOUND`
- `BROWSER_UNAVAILABLE`
- `FETCH_UNSUPPORTED`
- `TOKEN_MISSING`
- `TOKEN_INVALID`
- `TOKEN_EXPIRED`
- `ACCESS_DENIED`
- `EMPTY_RESULT`
- `QUERY_FAILED`
- `PARTIAL_CAPTURE`

## Browser-mode decisions to lock before coding

1. Use the aggregated feed for MVP.
2. Avoid clicking across many planets during MVP.
3. Prefer refresh/re-navigation before extraction if the tab may be stale.
4. Limit scrolling to a conservative depth, e.g. one extra page.
5. Default to preview capture for long posts; mark `PARTIAL_CAPTURE` instead of aggressively expanding content.

## Session-token decisions to lock before coding

Recommended `state/session.token.json`:

```json
{
  "kind": "cookie",
  "cookie_name": "zsxq_access_token",
  "cookie_value": "<private>",
  "domain": ".zsxq.com",
  "source": "browser-devtools-copy",
  "captured_at": "2026-03-08T14:30:00+08:00",
  "user_agent": "optional",
  "note": "stored locally only; do not commit"
}
```

Guidance:
- Keep the README extraction steps very explicit.
- Treat this mode as primary for deployment compatibility.
- Expect anti-bot and WAF failures in some environments, and fall back to browser verification when needed.

## Cursor decisions to lock before coding

Recommended `state/cursor.json`:

```json
{
  "version": 1,
  "updated_at": "2026-03-08T14:30:00+08:00",
  "access_mode": "token",
  "ttl_days": 7,
  "max_entries": 500,
  "seen": {
    "abc123": 1772951400,
    "def456": 1772951000
  }
}
```

Rules:
- Store `item_id -> timestamp`.
- TTL prune old entries.
- Enforce `max_entries` by dropping the oldest timestamps.
- If item IDs are missing, hash a deterministic fallback key.

## MVP

Ship only:
1. single manual digest run
2. local private session mode
3. browser relay as recovery/verification path
4. cursor-based dedupe with TTL + max size
5. structured user-visible errors
6. digest truncation limits
7. aggregated-feed filtering by configured planet names when browser mode is used

Optional in MVP if easy:
- fetch viability probe

Do not ship in MVP:
- realtime push
- high-frequency polling
- deep comments/attachments scraping
- multi-account support
- API reverse engineering
- aggressive click-to-expand flows

## V1

Add daily scheduled digest:
- cron trigger
- cursor filtering
- message delivery
- conservative scroll depth when browser recovery is used

## V2

Add low-frequency incremental alerts:
- not true realtime
- default 2h/4h cadence or similarly conservative polling
- explicit warning about platform risk and resource cost
- consider per-planet mode only after the token-first path is stable

## Near-term build order

1. `dedupe_and_state.py`
2. `collect_from_session.py`
3. `collect_from_browser.py`
4. README / release notes / `.skill` packaging notes
