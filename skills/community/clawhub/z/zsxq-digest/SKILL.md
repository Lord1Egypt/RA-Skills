---
name: zsxq-digest
description: Summarize new updates from followed Knowledge Planet (知识星球 / zsxq.com) circles and produce a daily triage digest that helps decide whether to click through and read in depth. Use when the user wants: (1) a daily summary of what changed across followed planets, (2) extraction of new posts/topics from Knowledge Planet through a locally stored private access token/session file, (3) browser-assisted fallback extraction when token mode is unavailable or needs verification, (4) prioritization of which circles or posts are worth opening, or (5) a reusable workflow for private-membership content where secrets must stay local and never be published with the skill.
---

# ZSXQ Digest

## Overview

Use this skill to turn private Knowledge Planet activity into either:
- a compact daily briefing
- or a per-circle stream digest that more faithfully preserves recent visible content

Default to the stream digest when the user wants a neutral, high-density summary with minimal commentary.

Default to **local private token/session mode** because many OpenClaw deployments run on VPS, Mac mini, or other remote hosts where browser relay is inconvenient. Use browser relay as the secondary path for local environments, verification, or recovery. Never ask to publish raw passwords, cookies, or private tokens with the skill.

## Supported access modes

Choose the least risky workable mode in this order:

0. **Auth bootstrap mode (first-run authorization)**
   - If no valid local token/session exists yet, enter a guided bootstrap flow.
   - Prefer host-side browser bootstrap when browser tooling is available.
   - If browser bootstrap cannot recover a usable token, fall back to manual token import.
   - Do not pretend a plain remote URL alone is a guaranteed OAuth-style binding flow.

1. **Local private session mode (preferred steady state)**
   - Allow the user to keep a token/session file locally under `state/` or another gitignored path.
   - Treat these files as private runtime state, never as distributable assets.
   - Validate freshness before use and surface explicit expiry/login-failed errors.
   - Center the schema on `zsxq_access_token`.

2. **Browser relay mode**
   - Use a logged-in browser tab attached through OpenClaw browser tooling.
   - Prefer `profile="chrome"` when the user is using the Chrome extension relay.
   - Use this for local environments, browser-first users, or when token mode needs manual recovery/verification.
   - If token mode hits transient API instability (for example intermittent internal-error responses), prefer retry + browser fallback before asking the user to re-login.

3. **Fetch fallback mode**
   - Treat this as viability-probe-only.
   - Attempt only if the target environment lacks browser ability and a fetch path is known to work.
   - If fetch cannot carry the login state or returns incomplete content, fail clearly and recommend token mode or browser mode.

## Workflow

1. Confirm scope.
   - Ask which followed planets or categories to track.
   - Ask for the time window: today, last 24 hours, or since the last digest.
   - Ask whether the user wants all updates or only high-signal items.
   - If the joined-group list contains expired, archived, or intentionally ignored planets, keep an explicit allow/deny list in a local groups file or via CLI excludes instead of blindly summarizing everything returned by `/v2/groups`.

2. Select an access mode.
   - If no valid token/session exists yet, start auth bootstrap mode first.
   - Prefer local private session mode once a reusable token exists.
   - If browser-assisted first-run auth is needed, prefer the unified entrypoint `scripts/run_browser_bootstrap.py` before dropping down to the lower-level helper scripts.
   - If token mode is invalid or blocked, try browser relay mode for recovery/verification.
   - If neither is available, test whether fetch fallback is viable.
   - If none work, stop and return a specific action item instead of guessing.

3. Validate authentication before extraction.
   - Confirm the response or page represents a logged-in state.
   - Detect obvious failure modes: expired token, login page, QR prompt, permission denied, empty feed, or fetch blocked.
   - Surface these states explicitly.

4. Collect update units.
   - Capture circle name, post title or first line, author, timestamp, link, tags if visible, and engagement hints if available.
   - Keep raw extraction lightweight. Only preserve fields needed for ranking and digest generation.
   - If long content is collapsed, prefer preview capture plus `PARTIAL_CAPTURE` over aggressive expansion during MVP.

5. Normalize, truncate, and deduplicate.
   - Merge repeated captures of the same post.
   - Separate content types when possible: long post, Q&A, resource drop, event notice, recruitment, ad, chatter.
   - Prefer canonical post links or stable IDs.
   - Apply hard limits to preview length and total digest input size before model summarization.

6. Score for click-through value.
   - High priority: thesis changes, original analysis, concrete tactics, datasets, tools, model updates, resource bundles, deadlines, policy changes.
   - Medium priority: routine discussion with some takeaways.
   - Low priority: reposts, greetings, generic chat, duplicate notices.

7. Produce the digest.
   - Prefer the stream digest as the default public output.
   - Group by circle.
   - For each circle, expand 1~3 representative items.
   - Render the remaining items as compact summaries with original URLs.
   - Keep visible metadata light.
   - Prefer showing only useful reader-facing context such as `摘要时间跨度` and `作者` when available.
   - For normal discussion / Q&A items, prefer one concise sentence that says what the item is about.
   - Do not force visible fields like “why it matters” unless the user asks for a stronger editorial mode.

## Delivery modes

Implement these in phases:

1. **MVP**
   - Single manual run: collect recent updates and produce one digest.
   - Token/session mode first; browser relay secondary.

2. **V1**
   - Daily scheduled digest at a fixed time.
   - Use a local cursor file to suppress repeats.

3. **V2**
   - Optional low-frequency incremental alerts.
   - Do not market this as true realtime push unless the environment genuinely supports that safely.

## Error handling requirements

Never fail silently. Return a clear status and next action.

Minimum explicit statuses:
- `AUTH_BOOTSTRAP_REQUIRED`
- `QR_READY`
- `QR_EXPIRED`
- `AUTH_WAITING_CONFIRMATION`
- `AUTH_CAPTURE_UNVERIFIED`
- `AUTH_BOOTSTRAP_FALLBACK_MANUAL`
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

For each failure, tell the user what happened, what was attempted, and the recommended next step.

## Private state rules

- Keep all private runtime state under gitignored paths.
- Suitable examples: `state/session.token.json`, `state/cursor.json`, `state/config.json`, `state/groups.json`.
- Never package these files into the public skill release. If the working tree contains live runtime files, stage a sanitized copy first or use `scripts/package_public_release.py`.
- Never hardcode personal circle names or secrets into `SKILL.md`, scripts, or references unless the user explicitly wants a private fork.

## Output format

Preferred public stream layout:

```markdown
# 知识星球信息流摘要
## 星球名
- 摘要时间跨度：...
- 作者：...

### 重点展开
#### 1. 标题
- 摘要：...
- 原文：https://...

### 其余更新
- 摘要：...
  - 原文：https://...
```

Rules:
- Avoid noisy technical headers in the default user-facing output.
- Prefer concise, readable summaries over operational metadata.
- For grouped news/link-list posts, keep the public default conservative; circle-specific custom handling should stay optional/local.

If reliable extraction is incomplete, explicitly mark missing scope instead of guessing.

## Read these references when needed

- For field selection and acquisition tradeoffs: `references/extraction-strategy.md`
- For normalization and ranking output fields: `references/output-schema.md`
- For auth, fallback, config, and error strategy: `references/runtime-modes.md`
- For the auth bootstrap decision and first-run login flow: `references/auth-bootstrap.md`
- For token extraction and handling: `references/session-token-guide.md`
- For browser fallback and recovery contract: `references/browser-recovery.md`
- For a browser-to-JSON recovery workflow: `references/browser-workflow.md`
- For the starter browser evaluate payload: `scripts/browser_capture_starter.js`
- For deterministic auth-bootstrap state + token finalization: `scripts/auth_bootstrap.py`
- For preparing the real Knowledge Planet login page into QR mode: `scripts/prepare_zsxq_qr_bootstrap.js`
- For probing real WeChat QR state in the embedded login flow: `scripts/probe_wechat_qr_state.js`
- For exporting a local tracked-groups config from the live token: `scripts/export_groups_config.py`
- For the single browser-assisted bootstrap workflow entrypoint: `scripts/run_browser_bootstrap.py`
- For synchronizing bootstrap state from the browser helpers: `scripts/sync_auth_bootstrap.py`
- For CDP-based browser cookie extraction after login: `scripts/capture_browser_cookies.js`
- For the locked implementation route: `references/final-implementation-plan.md`

## Guardrails

- Respect private-content boundaries. Package workflow and scripts, not personal data.
- Assume site structure or API behavior may change. Keep selectors and parsers isolated so they can be updated quickly.
- Prefer token/session mode for deployment compatibility.
- Use browser relay as the main recovery and verification path.
- Treat fetch fallback as experimental, not as a guaranteed replacement for authenticated access.
- If access is blocked, stop and explain the failure instead of fabricating summaries.
