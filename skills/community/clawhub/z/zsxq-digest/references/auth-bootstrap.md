# Auth bootstrap design

## Goal

Give the user a smoother first-run authorization flow for `zsxq-digest` without pretending Knowledge Planet offers an official OAuth/device-code flow.

Target user experience:
1. the skill is called
2. the agent detects that no valid token exists yet
3. the agent initiates a guided authorization/bootstrap flow
4. the host ends up with a locally stored reusable session token
5. later digest runs use token mode directly

## Current reality

Today, two paths are realistically available:

1. **manual token import**
   - user copies a valid `zsxq_access_token`
   - host stores it in `state/session.token.json`
2. **browser-assisted recovery**
   - user has a logged-in browser page
   - browser tooling helps verify or recover access

What is **not** currently proven:
- a true official OAuth callback flow
- a mobile/remote login URL that automatically hands a reusable token to the host

## Recommended MVP route

Use **host-side QR forwarding / browser bootstrap** as the preferred guided login path, with manual token import as the fallback.

### Why this is the best MVP

- closest to the desired "send me a link / let me authorize once" experience
- avoids requiring the user to open devtools as the primary path
- keeps private auth material local to the host
- matches OpenClaw's browser-tool strengths better than inventing a fake OAuth flow

## MVP flow

### Path A: guided browser bootstrap (preferred when browser tooling is available)

1. user triggers the skill and no valid token is found
2. agent enters `AUTH_BOOTSTRAP_REQUIRED`
3. agent opens a host-side browser page for Knowledge Planet login
4. agent confirms that a login page / QR page is visible
5. agent captures the visible QR or login prompt and sends it to the user in chat
6. user scans / confirms login on phone or another device
7. agent polls the browser page for a logged-in state
8. if a usable session artifact can be recovered locally, host writes `state/session.token.json`
9. later runs switch back to token mode

### Path B: manual token bootstrap (fallback)

Use when:
- host browser is unavailable
- browser-based bootstrap cannot recover a usable token
- deployment is too minimal for browser flows

Steps:
1. agent explains that automatic bootstrap is unavailable in the current environment
2. agent points the user to `references/session-token-guide.md`
3. user locally prepares `state/session.token.json`
4. agent retries token mode

## Important implementation truth

The browser-bootstrap direction is promising, but one hard point remains **not fully proven in the current MVP**:

> whether the available browser-tool chain can reliably recover the exact reusable auth artifact needed by token mode in all environments.

That means:
- QR forwarding is a valid **product direction**
- but it must still keep a fallback to manual token import
- do not falsely promise "one-tap cross-device binding" until the token/session handoff is verified on a real Knowledge Planet login page

## Boundaries for a public skill

### Include in the public skill
- guided login-state detection logic
- auth bootstrap decision rules
- browser recovery workflow documentation
- manual token fallback documentation
- structured statuses and next-action messages

### Do not include in the public skill
- any personal tokens or captured cookies
- any fake guarantee that a remote URL alone can authorize the host
- custom cloud callback infrastructure unless the project intentionally expands beyond a lightweight public skill

## Suggested statuses

Add or reserve these statuses for auth bootstrap:
- `AUTH_BOOTSTRAP_REQUIRED`
- `QR_READY`
- `QR_EXPIRED`
- `AUTH_WAITING_CONFIRMATION`
- `AUTH_CAPTURE_UNVERIFIED`
- `AUTH_BOOTSTRAP_FALLBACK_MANUAL`

Keep existing statuses too:
- `TOKEN_MISSING`
- `TOKEN_INVALID`
- `TOKEN_EXPIRED`
- `ACCESS_DENIED`
- `BROWSER_UNAVAILABLE`
- `QUERY_FAILED`

## What the main agent should say honestly

Safe wording:
- "I can guide a host-side browser bootstrap flow and try to recover a reusable session token."
- "If the environment cannot yield a reusable token automatically, I will fall back to a manual token import guide."

Unsafe wording:
- "Just open this URL on your phone and the host will definitely be authorized automatically."

## Practical next step

Implement the skill so that first-run authorization is modeled as:

1. detect token missing / invalid
2. choose browser bootstrap if available
3. otherwise fall back to manual token import
4. once token is present, use token-first collection

## Bootstrap helper scripts

The repository now includes two lightweight helper scripts:
- `scripts/auth_bootstrap.py`
- `scripts/capture_browser_cookies.js`

### `auth_bootstrap.py`

Its role is to manage the deterministic local pieces of the flow:
- bootstrap state transitions
- QR readiness / expiry markers
- fallback-to-manual markers
- cookie-capture finalization into `state/session.token.json`

This script does **not** replace OpenClaw browser tooling.
Instead, it gives the browser-driven flow a stable local state machine and token-writing contract.

Intended commands:
- `init`
- `qr-ready`
- `wait`
- `expire`
- `fallback-manual`
- `finalize-cookies`
- `status`

### `capture_browser_cookies.js`

Its role is to connect to an already opened browser page through its CDP `wsUrl` and call `Network.getCookies`.

This makes the promising browser-bootstrap path more concrete:
1. browser tooling opens a login page and keeps the target tab alive
2. after login succeeds, the page `wsUrl` is known
3. `capture_browser_cookies.js` extracts cookies into a local JSON file
4. `auth_bootstrap.py finalize-cookies` filters and writes the reusable token file

This path has already been validated on a test cookie page, so the browser-to-token handoff is no longer purely hypothetical.

### `prepare_zsxq_qr_bootstrap.js`

Its role is to connect to the real Knowledge Planet login page via CDP `wsUrl`, then:
- click the protocol consent icon if needed
- click `获取登录二维码`
- return the embedded WeChat login iframe URL

This step has been validated against the real `https://wx.zsxq.com/login` page structure.

### `sync_auth_bootstrap.py`

Its role is to glue the local bootstrap pieces together.

Given a state file plus one or two page `wsUrl` values, it can:
- initialize bootstrap state if needed
- prepare the Knowledge Planet login page into QR mode
- probe the WeChat QR page state
- synchronize `auth-bootstrap.json` to `QR_READY`, `AUTH_WAITING_CONFIRMATION`, `QR_EXPIRED`, or `AUTH_CAPTURE_UNVERIFIED`

This does **not** replace browser automation. Instead, it reduces the number of manual local steps needed between browser-tool calls.

### `run_browser_bootstrap.py`

Its role is to provide a single workflow entrypoint over the lower-level helpers.

It supports three practical modes:
1. `run` / `sync` for QR preparation and state synchronization
2. `finalize` for cookie capture + token-file finalization
3. optional token verification immediately after finalization

Typical usage pattern:
1. run it with `--zsxq-ws-url` and `--wechat-ws-url` until you get `QR_READY`
2. send the QR to the user
3. after scan/confirmation, rerun it with `--capture-ws-url` on a logged-in Knowledge Planet page
4. let it write `state/captured-cookies.json`, `state/session.token.json`, and a verification probe output

This keeps the public skill honest: browser tooling still opens and owns the tabs, but the local workflow is now concentrated in one deterministic CLI entrypoint.

If the token file is written successfully but an immediate verification request hits a transient API-side failure, the wrapper returns an explicit `verification_warning` field rather than silently claiming the verification passed.

### `probe_wechat_qr_state.js`

Its role is to connect to the WeChat QR login page via CDP `wsUrl` and detect whether the page is currently in:
- `QR_READY`
- `AUTH_WAITING_CONFIRMATION`
- `QR_EXPIRED`

It also returns the live QR image URL when visible.

This matters because the real Knowledge Planet login page does not render the QR directly in its own DOM. It embeds a WeChat login iframe, so the bootstrap flow must inspect the embedded WeChat page itself.
