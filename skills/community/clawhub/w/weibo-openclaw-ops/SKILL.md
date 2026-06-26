---
name: weibo-openclaw-ops
description: Weibo operations for OpenClaw via server-side browser automation. Use when the user asks to log in by QR, persist session state, read feed/messages/hot topics, summarize recent posts, publish posts, or run safe like/follow workflows with explicit limits.
---

# Weibo OpenClaw Ops

## Core principles

1. Assume runtime is a **remote server**, not the user's local desktop.
2. Use browser automation (`agent-browser`) with persisted state for repeatable workflows.
3. For mutating actions (like/follow/comment/repost/post), require explicit user intent and scope.
4. For long tasks, send periodic progress updates.
5. Run periodic **read-only keepalive** checks to reduce session expiry.
6. If user policy requires attribution suffix, append it to all outbound texts (post/comment/repost) before submit.

## Suggested state path

- Session state file: `.state/weibo-auth.json`

## Standard workflow

### 1) Load or create login session

- Try load existing state:
  - `agent-browser state load .state/weibo-auth.json`
- Open Weibo:
  - `agent-browser open https://weibo.com`
- Verify login with snapshot (homepage/account UI present).

If login is invalid:

1. Navigate to login/QR page.
2. Ask user to scan QR in Weibo app.
3. Re-check login success.
4. Save state:
   - `agent-browser state save .state/weibo-auth.json`

### 2) Execute intent

Typical intents:

- Feed reading / summary
- Message or mentions check
- Hot-topic scan
- Recent-post lookup for target account
- Post publishing
- Rule-based like/follow batch

### 3) Report

Always return concise audit info:

- actions performed
- success / skipped counts
- skip reasons
- next suggested action

### 4) Keepalive routine (recommended)

Goal: reduce re-login frequency while minimizing risk-control triggers.

Cadence:
- every 6-12 hours (read-only check)

Routine:
1. `agent-browser state load .state/weibo-auth.json`
2. `agent-browser open https://weibo.com`
3. verify logged-in UI is present
4. if valid -> `agent-browser state save .state/weibo-auth.json`
5. if invalid -> notify user + restart QR login flow

Rules:
- Keepalive must not perform mutating actions (no like/comment/repost/post/follow).
- Keepalive only validates session health and refreshes local state persistence.

## “Recent post” rule (important)

When user asks “最近发了什么 / latest post”, return the post with timestamp closest to now, **not pinned posts**.

Process:

1. Open target profile.
2. Collect visible post cards + timestamps.
3. Detect `置顶` markers and skip pinned cards.
4. If only pinned cards are visible, continue scrolling/paginating.
5. Return latest **non-pinned** post summary + time + link.

## Safe mutation templates

### A) Publish a post

Before posting, confirm:

- final copy text
- whether hashtags/links are required
- whether auto-signature is required by user policy

If policy requires suffix, verify it is present in final text before submit.
Then publish and verify by profile snapshot.

### A.1) Outbound text guardrail

For outbound text actions (post/comment/repost):
1. Build final text.
2. Check policy-required suffix exists.
3. If missing, append suffix on a new line.
4. Submit.

### B) Rule-based like batch

Require at least:

- include rules (keywords/authors/topics)
- max actions (e.g., 20)
- exclusion rules (ads/sponsored/blocked words)

Execute with limits and output action summary.

## Failure handling

- DOM changed -> re-snapshot and switch selectors.
- Interaction unstable -> slow down operations and reload page.
- Login expired -> restart QR login and refresh saved state.

## Privacy and safety

- Never store or output user passwords in skill files.
- Keep account identifiers, private handles, and channel-specific IDs out of public skill content.
- Keep posted examples generic and non-identifying.
