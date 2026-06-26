# Final implementation plan

## Final product definition

`zsxq-digest` is a public-friendly OpenClaw skill that helps users quickly answer one question:

**“What changed in the Knowledge Planet circles I care about, and what is worth clicking into?”**

It is not a full crawler, not a backup suite, and not a realtime event system.

## Product goals

1. Summarize recent updates from followed Knowledge Planet circles.
2. Help the user triage what deserves deep reading.
3. Stay lightweight enough to publish publicly and reuse across different OpenClaw environments.
4. Keep secrets local and never package them with the skill.

## Non-goals

- full backup/export of all content
- comments/files/images archival in MVP
- realtime push
- high-frequency polling
- multi-account orchestration
- API reverse engineering as a hard dependency

## Deployment assumptions

- OpenClaw may run on a local Mac, a Mac mini, or a VPS.
- The user may log in from another device such as a phone.
- Some environments will not have browser capability.
- Some environments will not be suitable for browser-based access as the main path.

## Access-mode architecture

Before steady-state collection begins, the skill may need a first-run **auth bootstrap** step to obtain a reusable local session artifact.


### Mode 0: Auth bootstrap (first run)
If no valid local token/session exists yet, the skill should enter a guided bootstrap flow instead of immediately failing.

Recommended MVP behavior:
- prefer host-side browser-assisted bootstrap when browser tooling is available
- if that path cannot recover a reusable token/session, fall back to manual token import
- do not promise an OAuth-style remote binding flow unless it has been proven in the real environment

### Mode A: Local private session (primary steady state)
Allow a gitignored local file that stores a private session artifact, centered on `zsxq_access_token`.

Why this is primary:
- best compatibility for VPS / Mac mini / remote-host deployment
- supports users who mainly operate from mobile devices
- does not require the browser to remain open all the time
- matches how many agents are actually deployed in practice

Primary-mode caveat:
- token-based HTTP access may hit anti-bot/WAF behavior in some environments
- therefore browser relay must remain available as a recovery and verification path

### Mode B: Browser relay (secondary)
Use OpenClaw browser tooling with `profile="chrome"` and a logged-in Knowledge Planet tab.

Why this still matters:
- avoids direct API/header assumptions
- best fallback when token mode fails
- useful for local deployments and manual verification

### Mode C: Fetch fallback (experimental)
Treat `web_fetch` or similar fetch-based access as a viability probe only.

Why it is not a standard mode:
- Knowledge Planet is a heavy SPA
- plain fetch often returns shell HTML or login walls
- stable authenticated fetch is not demonstrated as a reliable main path

## Session-token design

### Recommended file
`state/session.token.json`

### Recommended schema
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

### Extraction path to document
1. Open Knowledge Planet web app.
2. Log in.
3. Open browser devtools.
4. Go to Application/Storage or inspect an `api.zsxq.com` request.
5. Copy the `zsxq_access_token` cookie value.
6. Save it locally into `state/session.token.json`.

### Security rule
- Never commit this file.
- Never include it in a packaged `.skill`.
- Never ask the user to paste the token into a public repo or issue.

## Browser-mode collection strategy

### MVP choice
Use the **aggregated update feed** and filter locally by configured planet names.

Why this is the MVP browser strategy:
- avoids repeated clicks across many planets
- reduces browser-state disruption
- easier to explain and implement
- acts as a safe recovery path when token mode is not usable

### Known limitation
A very active circle can dominate the aggregated feed and push quieter but important circles below the fold.

### MVP mitigation
- support one conservative additional scroll page
- allow configurable `max_items`
- document the limitation in README
- recommend that users place important circles in prominent positions if possible

### Long content rule
MVP does **not** aggressively click `展开全文`.
Instead:
- capture visible preview text
- mark `PARTIAL_CAPTURE`
- keep the original URL for manual deep reading

## Cursor/state design

### Runtime files
```text
state/
  cursor.json
  session.token.json
  cookies.json
  config.json
```

### Cursor schema
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

### Cursor rules
- store `item_id -> timestamp`
- prune entries older than `ttl_days`
- enforce `max_entries` by evicting the oldest
- if no stable item ID exists, derive a deterministic fallback hash from core fields

## Config design

### Recommended `state/config.json`
```json
{
  "mode": "token",
  "planets": ["示例星球A", "示例星球B"],
  "schedule": {
    "daily_digest": "08:00",
    "quiet_hours": ["23:00-07:00"]
  },
  "limits": {
    "max_items": 30,
    "max_preview_chars": 280,
    "max_total_chars": 12000,
    "max_scroll_pages": 1
  },
  "cursor": {
    "ttl_days": 7,
    "max_entries": 500
  },
  "token_file": "state/session.token.json"
}
```

## Error model

The skill must never fail silently.

Minimum statuses:
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

Each error reply should include:
1. access mode attempted
2. observed failure
3. recommended next step

## Output design

The digest should include:
- time window
- access mode used
- number of updates scanned
- top picks
- grouped updates by planet
- anomaly / incompleteness note
- recommended reading order

## Delivery roadmap

### MVP
Ship:
1. single manual digest run
2. local private session mode
3. browser relay as secondary recovery path
4. bounded cursor dedupe
5. explicit structured errors
6. truncation limits

Optional in MVP if easy:
- browser relay manual verification flow
- fetch viability probe

Do not ship in MVP:
- realtime push
- high-frequency polling
- comment/file/image deep scraping
- multi-account support
- aggressive click-to-expand flows

### V1
Ship:
- daily scheduled digest via cron
- message delivery to the user
- browser fallback when token mode errors or expires

### V2
Explore:
- low-frequency incremental alerts
- more robust per-planet targeting
- stronger session-mode support if field-tested

## Implementation order

### P0
Lock the session-token contract:
- schema
- extraction guide
- optional `user_agent`
- error mapping

### P1
Implement bounded state handling:
- `dedupe_and_state.py`
- TTL prune
- max-entry cap
- atomic writes

### P2
Implement session collector:
- `collect_from_session.py`
- token validation
- `/v2/groups` listing support
- `/v2/groups/{group_id}/topics?scope=all&count=N` support
- normalized item output
- structured failure mapping
- optional output file writing

### P3
Implement browser collector:
- `collect_from_browser.py`
- tab targeting
- stale-page refresh
- partial-capture marking

### P4
Publish-facing docs:
- README
- install notes
- risk warnings
- `.skill` packaging instructions

## External references that informed this plan

- RSSHub ZSXQ route (`DIYgod/RSSHub`, `samuelye/RSS-Hub`): validated narrow token-based route design
- `zsxq_notice`: validated that notification-style workflows exist, but its service stack is too heavy for this skill
- `zsxqbackup` and similar spiders: validated token + user-agent conventions, but also showed what to avoid for a lightweight public skill
- `yiancode/zsxq-sdk`: validated a cleaner token extraction/documentation path

## Final decision

The final recommended path is:
- **Primary:** local private session using `zsxq_access_token`
- **Secondary:** browser relay for recovery and verification
- **Experimental only:** fetch fallback

This balances public shareability, remote deployment compatibility, and long-term maintainability.
