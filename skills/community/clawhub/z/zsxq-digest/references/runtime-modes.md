# Runtime modes

## Purpose

Describe the three access modes for public-friendly deployment: local private session storage, browser relay, and fetch fallback.

## 1. Local private session mode (preferred)

### Best fit
- OpenClaw runs on a VPS, home server, or Mac mini.
- The user logs in elsewhere and then transfers a private token/session artifact to the host.
- Browser tooling is unavailable, inconvenient, or not the main deployment model.

### Strengths
- Best compatibility for remote-host deployments.
- Does not require the browser to remain open all the time.
- Matches how many agents are actually deployed in practice.

### Weaknesses
- Direct token-based HTTP access may hit anti-bot defenses or WAF rules.
- Harder for non-technical users.
- Requires careful local secret handling.

### Storage rule
- Keep private files under a gitignored runtime path, for example:

```text
state/
  session.token.json
  cookies.json
  cursor.json
  config.json
```

### Recommended session schema

Prefer a minimal cookie-based schema centered on `zsxq_access_token`.

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

### Extraction guidance
- Document a simple user path such as: browser devtools -> Application/Storage or Network -> Cookies -> copy `zsxq_access_token` -> paste into `state/session.token.json`.
- Keep the README explanation beginner-friendly.
- Never ask the user to paste the token into public chat if a local file path will do.

### Requirements
- Never commit these files.
- Validate token freshness on each run.
- Return explicit errors for missing, invalid, or expired tokens.
- Prefer optional `user_agent` capture because some token-based routes are header-sensitive.

### Caveat
- This is the preferred deployment mode, but not a guaranteed always-work mode.
- If the platform blocks token-based HTTP access in a given environment, fall back to browser relay.

## 2. Browser relay mode

### Best fit
- User environment supports OpenClaw browser tooling.
- User can attach a logged-in Chrome tab.
- Token mode is unavailable, invalid, or needs manual recovery/verification.

### Strengths
- Avoids direct API/header assumptions.
- Reuses the user's normal login flow.
- Most consistent with Knowledge Planet's interactive web experience.

### Weaknesses
- Depends on browser availability.
- Background refresh and scrolling can disturb the user's active browser session.
- Tab/session can disappear or become stale.

### Required checks
- Verify target tab exists.
- Verify page is logged in.
- Verify update list is visible.
- Detect long-content collapse and partial capture.
- Prefer a page refresh or re-navigation before extraction when the tab appears stale.

### MVP collection strategy
- Default to the aggregated update feed.
- Filter locally by configured planet names.
- Avoid clicking in and out of many planets during MVP.
- Accept the aggregation siphon risk: highly active planets can push low-volume planets below the fold.
- Mitigation for later versions: allow one controlled downward scroll, higher fetch depth, or per-planet mode.

### Long content policy
- MVP default: do **not** aggressively click `展开全文`.
- Capture visible preview text, mark `PARTIAL_CAPTURE` when truncation is detected, and keep the original link.
- Only add click-to-expand logic later when stability is proven.

## 3. Fetch fallback mode

### Best fit
- Browser tooling is unavailable.
- A fetch call can actually reach authenticated HTML or exported content.
- The user accepts best-effort behavior.

### Important limitation
- `web_fetch` is **not** a reliable replacement for authenticated access on Knowledge Planet.
- The site is a heavy SPA. In many environments, fetch will return a login wall, shell HTML, or incomplete content.

### Rule
- Treat fetch as a **viability probe**, not a standard mode.
- Attempt it only when a known authenticated endpoint or exported content path exists.
- If fetch returns incomplete content, return `FETCH_UNSUPPORTED` and recommend token mode or browser relay.
- Do not market fetch fallback as stable unless real deployment evidence proves otherwise.

## Cursor schema and retention

Use a bounded cursor file. Do not allow unbounded growth.

Recommended shape:

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
- `seen` maps stable `item_id -> unix_timestamp`.
- Remove entries older than `ttl_days`.
- Also enforce `max_entries` by evicting the oldest timestamps.
- If no stable item ID exists, hash a fallback key from `planet + author + published_at + title_or_hook`.

## Error model

Use explicit machine-friendly states plus human guidance.

Recommended states:
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

Recommended response template:

```markdown
状态: TOKEN_EXPIRED
尝试方式: local-private-session
现象: 请求返回未授权，无法拉取关注星球更新
建议下一步:
1. 更新本地 token/session 文件
2. 确认文件路径仍在 gitignore 保护下
3. 如仍失败，改用 browser 模式做验证
```

## Config suggestion

Provide a small config file for public reuse, for example:

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

## MVP recommendation

Ship local private session mode first.
Keep browser relay as the main recovery and verification path.
Document fetch fallback as viability-probe-only and explicitly experimental.
