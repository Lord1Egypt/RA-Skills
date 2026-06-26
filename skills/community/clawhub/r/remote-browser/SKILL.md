---
name: remote-browser-service
description: >
  Control a remote Chrome browser via HTTP API (Kubernetes or Docker backend). Use for web automation,
  form filling, navigation, and page inspection on sites the user owns or has permission to access.
  Exposes the accessibility tree, text extraction, Chrome screenshots, VNC-native screenshots,
  DOM actions, and VNC actions — optimized for AI agents. Requires an active browser session
  (created via HTTP or WebSocket).
metadata:
  openclaw:
    emoji: "🌐"
    requires:
      env:
        - name: AC_API_KEY
          secret: true
          optional: true
          description: "Bearer token or API key for auth (user_id derived from token)"
---

# Remote Browser Service

Browser control for AI agents via HTTP API. Supports both DOM-oriented automation
and remote-desktop/VNC control when you need the actual framebuffer.

## Index

- [Setup](#setup)
- [Core Workflow](#core-workflow)
- [API Reference](#api-reference)
- [Screenshot](#screenshot)
- [VNC interface](#vnc-interface)
- [VNC screenshot](#vnc-screenshot)
- [Act on elements](#act-on-elements)
- [VNC action](#vnc-action)
- [HTML snapshot](#html-snapshot)
- [Token Cost Guide](#token-cost-guide)
- [Limitations & fallbacks](#limitations--fallbacks)
- [Environment Variables](#environment-variables)
- [Tips](#tips)

## Setup

Ensure you have an active session:

1. **Create session** — `POST /api/sessions` (HTTP, no WebSocket), or open WebSocket to `/ws/{session_id}` (DevTools CDP), or run from UI. Optional `url` in body (HTTP) or query (WS) to navigate immediately.
2. **Or restore** — Use stored session from `GET /api/stored-sessions`
3. **Auth** — Pass `Authorization: Bearer <token>` or `X-API-Key`, or `?access_token=<token>`

Base URL: `https://rb.all-completed.com` (or `RBS_BASE_URL`). Replace `{session_id}` in examples. User ID is derived from the token.

## Core Workflow

1. **Navigate** to a URL
2. **Snapshot** the accessibility tree (get refs) — `GET .../json`
3. **Act** on refs or selectors (click, type, fill, press)
4. **Snapshot** again to see results

For visual or OS-level flows, use the VNC path instead:

1. **Open VNC interface** — `GET /users/{user_id}/vnc/{session_id}` when you want a live noVNC view
2. **Capture VNC framebuffer** — `GET .../vnc/screenshot`
3. **Send VNC input** — `POST .../vnc/action` with coordinates or keys
4. **Capture again** to verify pixel-level results

Refs (`e0`, `e1`, …) from `/json` can be used with `/action` via `selector` (use `ref` as selector for `e5` → `"e5"` maps to role/name; for now use CSS `selector`).

Supported actions by mode:

| Mode               | Kind     | Example                                                     |
|--------------------|----------|-------------------------------------------------------------|
| DOM (`/action`)    | `click`  | `{"kind":"click","selector":"button.submit"}`               |
| DOM (`/action`)    | `tap`    | `{"kind":"tap","selector":"button.submit"}`                 |
| DOM (`/action`)    | `type`   | `{"kind":"type","selector":"#email","text":"user@example.com"}` |
| DOM (`/action`)    | `fill`   | `{"kind":"fill","selector":"#email","text":"user@example.com"}` |
| DOM (`/action`)    | `press`  | `{"kind":"press","key":"Enter"}`                            |
| DOM (`/action`)    | `focus`  | `{"kind":"focus","selector":"input[name=search]"}`          |
| DOM (`/action`)    | `hover`  | `{"kind":"hover","selector":"button.submit"}`               |
| DOM (`/action`)    | `select` | `{"kind":"select","selector":"select","value":"option-1"}`  |
| DOM (`/action`)    | `scroll` | `{"kind":"scroll","scrollY":800}`                           |
| DOM (`/action`)    | `submit` | `{"kind":"submit","selector":"#nav-search-form"}` (or a field within the form) |
| Secrets (`/request-fill`) | — | `{"selector":"#pass","label":"Password","field":"password"}` — user fills it in the Keeper app; value never seen by the agent |
| VNC (`/vnc/action`) | `move`   | `{"kind":"move","x":320,"y":240}`                           |
| VNC (`/vnc/action`) | `click`  | `{"kind":"click","x":320,"y":240,"button":"left","repeat":1}` |
| VNC (`/vnc/action`) | `type`   | `{"kind":"type","text":"hello world"}`                      |
| VNC (`/vnc/action`) | `press`  | `{"kind":"press","keys":["Ctrl","l"]}`                      |
| VNC (`/vnc/action`) | `scroll` | `{"kind":"scroll","x":320,"y":240,"direction":"down","repeat":3}` |

## API Reference

### Create session (HTTP)

```bash
curl -X POST "https://rb.all-completed.com/api/sessions" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{}'
# Optional: {"session_id": "my-session", "url": "https://example.com"}
# Fork from stored session: {"session_id": "my-fork", "from": "original-session"}
# Ephemeral (start from metadata/fork but don't save): {"ephemeral": true}
```

Sessions idle for 5 min are closed. Use `POST .../ping` to keep alive.

Maximum 1 concurrent session per user. If creation returns 429 or WebSocket closes with a limit error: **wait a bit** (previous session may still be shutting down) **and/or close the previous session** via `DELETE /api/sessions/{session_id}` before retrying.

### List sessions

```bash
curl "https://rb.all-completed.com/api/sessions" \
  -H "Authorization: Bearer <token>"
```

### Session status

```bash
curl "https://rb.all-completed.com/api/sessions/{session_id}/status" \
  -H "Authorization: Bearer <token>"
```

Returns live session state plus current page metadata:

```json
{
  "session_id": "session-123",
  "created_at": "2026-02-12T10:00:00",
  "active_ws_connections": 1,
  "status": "ready",
  "last_error": null,
  "current_url": "https://example.com/page",
  "page_title": "Example Domain",
  "last_status_code": 200
}
```

HTTP status codes:

- `200` - Session found; manager status returned, with live page metadata when available
- `404` - Session not found for the authenticated user
- `503` - Service not initialized

`last_status_code` is the browser's last navigation response code when Chrome exposes it through Navigation Timing. If it is not available yet, the field is `null`.

### List stored sessions

```bash
curl "https://rb.all-completed.com/api/stored-sessions" \
  -H "Authorization: Bearer <token>"
```

Returns `{sessions: [...], count}`. Connect via WebSocket to `/ws/{session_id}` to resume.

### Navigate

```bash
curl -X POST "https://rb.all-completed.com/api/sessions/{session_id}/navigate" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# With timeout (seconds)
curl -X POST "https://rb.all-completed.com/api/sessions/{session_id}/navigate" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "timeout": 60}'
```

### Set location

```bash
# Override geolocation for the page (e.g. for location-aware sites)
curl -X POST "https://rb.all-completed.com/api/sessions/{session_id}/location" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"latitude": 37.7749, "longitude": -122.4194}'

# With accuracy (meters)
curl -X POST "https://rb.all-completed.com/api/sessions/{session_id}/location" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"latitude": 51.5074, "longitude": -0.1278, "accuracy": 50}'
```

### Image (download by selector)

```bash
# Capture a single element (e.g. image) by CSS selector
curl "https://rb.all-completed.com/api/sessions/{session_id}/image?selector=img.hero" \
  -H "Authorization: Bearer <token>" \
  -o image.jpg

# With quality, raw binary (selector=#banner for id)
curl "https://rb.all-completed.com/api/sessions/{session_id}/image?selector=img&quality=90&raw=true" \
  -H "Authorization: Bearer <token>" \
  -o element.jpg
```

Use `selector` (CSS) or `ref` (from snapshot). Returns JPEG of the element's bounding box.

### Snapshot (accessibility tree)

```bash
# Full tree
curl "https://rb.all-completed.com/api/sessions/{session_id}/json" \
  -H "Authorization: Bearer <token>"

# Interactive elements only (buttons, links, inputs) — much smaller
curl "https://rb.all-completed.com/api/sessions/{session_id}/json?filter=interactive" \
  -H "Authorization: Bearer <token>"

# Limit depth
curl "https://rb.all-completed.com/api/sessions/{session_id}/json?depth=5" \
  -H "Authorization: Bearer <token>"
```

Returns `{nodes: [{ref, role, name, depth, value?, disabled?, focused?, nodeId?}], count}`.

### Extract text

```bash
# Readability mode (default) — strips nav/footer/ads
curl "https://rb.all-completed.com/api/sessions/{session_id}/text" \
  -H "Authorization: Bearer <token>"

# Raw innerText
curl "https://rb.all-completed.com/api/sessions/{session_id}/text?mode=raw" \
  -H "Authorization: Bearer <token>"
```

Returns `{url, title, text}`. Cheapest option (~800 tokens for most pages).

### Screenshot

```bash
# JSON with base64
curl "https://rb.all-completed.com/api/sessions/{session_id}/screenshot" \
  -H "Authorization: Bearer <token>"

# Raw JPEG bytes
curl "https://rb.all-completed.com/api/sessions/{session_id}/screenshot?raw=true" \
  -H "Authorization: Bearer <token>" \
  -o screenshot.jpg

# With quality (1-100)
curl "https://rb.all-completed.com/api/sessions/{session_id}/screenshot?quality=50&raw=true" \
  -H "Authorization: Bearer <token>" \
  -o screenshot.jpg

# Region capture (offset x,y and width,height in CSS pixels)
curl "https://rb.all-completed.com/api/sessions/{session_id}/screenshot?x=0&y=0&width=800&height=600&raw=true" \
  -H "Authorization: Bearer <token>" \
  -o region.jpg
```

Use this when Chrome DevTools rendering is enough. If you need browser chrome,
OS dialogs, permission prompts, or the exact remote desktop pixels, use
`/vnc/screenshot` instead.

### VNC interface

```bash
# Built-in noVNC client page for a session
open "https://rb.all-completed.com/users/{user_id}/vnc/{session_id}"

# Under the hood the page connects to the VNC websocket proxy
# /users/{user_id}/vnc/ws/{session_id}
```

Use the VNC interface when you need a live remote-desktop view of the session
instead of DOM snapshots.

### VNC screenshot

```bash
# Raw PNG bytes from the VNC framebuffer
curl "https://rb.all-completed.com/api/sessions/{session_id}/vnc/screenshot?raw=true" \
  -H "Authorization: Bearer <token>" \
  -o screen.png

# Cropped framebuffer region
curl "https://rb.all-completed.com/api/sessions/{session_id}/vnc/screenshot?x=0&y=0&width=800&height=600&raw=true" \
  -H "Authorization: Bearer <token>" \
  -o region.png
```

Unlike `/screenshot`, this captures the VNC framebuffer directly. Use it for
browser chrome, native permission prompts, OS-level dialogs, or anything only
visible in the remote desktop.

### Page size

```bash
# Get page content dimensions (use with screenshot clip)
curl "https://rb.all-completed.com/api/sessions/{session_id}/page-size" \
  -H "Authorization: Bearer <token>"
```

Returns `{width, height}` in CSS pixels.

### Act on elements

```bash
# Click by selector
curl -X POST "https://rb.all-completed.com/api/sessions/{session_id}/action" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"kind": "click", "selector": "button.submit"}'

# Click by coordinates (viewport x,y)
curl -X POST "https://rb.all-completed.com/api/sessions/{session_id}/action" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"kind": "click", "x": 100, "y": 200}'

# Type into element (focus + insertText)
curl -X POST "https://rb.all-completed.com/api/sessions/{session_id}/action" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"kind": "type", "selector": "#email", "text": "user@example.com"}'

# Fill (set value directly)
curl -X POST "https://rb.all-completed.com/api/sessions/{session_id}/action" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"kind": "fill", "selector": "#email", "text": "user@example.com"}'

# Press a key
curl -X POST "https://rb.all-completed.com/api/sessions/{session_id}/action" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"kind": "press", "key": "Enter"}'
# Press Enter in a specific input: -d '{"kind": "press", "key": "Enter", "selector": "input#search"}'

# Focus, hover, select, scroll
curl -X POST "https://rb.all-completed.com/api/sessions/{session_id}/action" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"kind": "focus", "selector": "input[name=search]"}'

curl -X POST "https://rb.all-completed.com/api/sessions/{session_id}/action" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"kind": "scroll", "scrollY": 800}'
```

**Action kinds:** `click`, `type`, `fill`, `press`, `focus`, `hover`, `select`, `scroll`. Use `selector` (CSS) or `ref` (from snapshot). For `click` you can use `x` and `y` (viewport coordinates) instead of selector. For `fill`, the server focuses the field, `select()` only if the field already has text (then `Input.insertText` replaces), otherwise focuses and inserts like `type`—controlled inputs (e.g. React) update reliably. For `press` use `key` (e.g. `Enter`, `Tab`, `Escape`, `Space`, `ArrowUp`); optional `selector` focuses element first.

### VNC action

```bash
# Move mouse
curl -X POST "https://rb.all-completed.com/api/sessions/{session_id}/vnc/action" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"kind":"move","x":320,"y":240}'

# Click at framebuffer coordinates
curl -X POST "https://rb.all-completed.com/api/sessions/{session_id}/vnc/action" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"kind":"click","x":320,"y":240,"button":"left","repeat":1}'

# Press keys directly over VNC
curl -X POST "https://rb.all-completed.com/api/sessions/{session_id}/vnc/action" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"kind":"press","keys":["Ctrl","l"]}'
```

**VNC action kinds:** `move`, `click`, `type`, `press`, `scroll`.

These actions are framebuffer-oriented and do not use DOM selectors. Prefer them
when DOM automation cannot see or control the target UI.

### HTML snapshot

```bash
# Full DOM with inlined CSS (opens in browser)
curl "https://rb.all-completed.com/api/sessions/{session_id}/html" \
  -H "Authorization: Bearer <token>"
```

## Token Cost Guide

| Method | Typical tokens | When to use |
|--------|----------------|-------------|
| `/status` | ~50 | Just the current URL / title / HTTP status |
| `/text` (readability) | ~800 | Reading page content |
| `/text?mode=raw` | ~2K–8K | Content readability strips (hidden labels, etc.) |
| `/json?filter=interactive` | ~3,600 | Finding buttons/links/inputs to act on (+ refs) |
| `/json` (full a11y tree) | ~10,500 | Full structure / element relationships |
| `/html?obfuscate=true` (simple markup) | ~10K–40K | Need exact CSS selectors / markup the a11y tree lacks |
| `/html` (full markup) | very large | Raw DOM + inlined CSS; rarely needed, may exceed the 5 MiB cap |
| `/image?selector=` | ~1K (vision) | Capture a single element / download an image |
| `/screenshot` (clipped, low `quality`) | ~1K–2K (vision) | Visual check of one region |
| `/screenshot` (full page) | ~2K+ (vision) | Whole-page layout / visual verification |
| `/vnc/screenshot` | ~2K+ (vision) | Non-DOM/native UI, canvas, or when DOM tools fail |

**Decision order — use the *cheapest* tool that answers your question, escalate only if it doesn't:**

1. **`/status`** — only need where you are (URL/title/status).
2. **`/text`** — reading/extracting content. (`?mode=raw` if readability hides what you need.)
3. **`/json?filter=interactive`** — locating things to click/type; returns refs to act on.
4. **`/json`** (full) — need structure/relationships the filtered tree omits.
5. **`/html?obfuscate=true`** — need a precise selector/markup not surfaced by the a11y tree. Prefer obfuscated (compact) over full.
6. **`/html`** (full) — last resort for raw markup/CSS; large.
7. **`/screenshot` (clipped + low quality)** — *only* for visual confirmation or non-DOM layout. Always clip (`x,y,width,height`) and drop `quality`; never grab a full high-quality page when a region will do.
8. **`/vnc/screenshot`** — only for native/canvas/non-DOM surfaces, or when DOM extraction genuinely fails.

**Rule of thumb:** text/markup ≫ screenshots for token cost. A clipped JPEG is still an image; a `/text` call is a few hundred tokens. Act on **selectors/refs** from steps 2–6 rather than re-screenshotting to "look again," and verify state changes with the cheapest read, not a fresh full screenshot.

## Environment Variables

| Var | Description |
|-----|-------------|
| `RBS_BASE_URL` | Base URL (e.g. https://rb.all-completed.com) |
| `AC_API_KEY` | Bearer token or API key (user_id derived from token) |

## Tips

- **Session required** — Ensure a session exists before calling navigate/json/text/action. Create via `POST /api/sessions` (HTTP), WebSocket, or restore from stored sessions.
- **Check live URL** — Use `GET /api/sessions/{session_id}/status` when you need the current page URL/title or last response status without fetching full page text.
- **429 / session limit** — If create fails with 429 or WebSocket closes (limit exceeded): wait a few seconds and/or terminate the existing session with `DELETE /api/sessions/{session_id}` first, then retry.
- **Refs from snapshot** — Use `selector` with the `ref` string (e.g. `"e5"`) when the action API supports ref→DOM resolution; otherwise prefer CSS selectors.
- **Readability vs raw** — `/text` (default) strips nav/footer/ads; `?mode=raw` returns full `innerText`.
- **Interactive filter** — `?filter=interactive` on `/json` reduces nodes by ~75% for action tasks.
- **VNC vs DOM** — Use `/action` for selectors/refs in the page DOM. Use `/vnc/action` and `/vnc/screenshot` for pixel-level automation and UI outside the DOM.
- **Stored sessions** — Sessions persist to S3 and are restored on reopen. The **whole browser profile** is captured (cookies, localStorage, sessionStorage, IndexedDB, **Service Workers**, Cache Storage, metadata) and restored as one consistent unit, so apps that keep their login in IndexedDB/Service Workers (e.g. Telegram Web) come back **logged in**, not just at the login page. List with `GET /api/stored-sessions`, then reopen by creating a session with the same `session_id` (HTTP/WebSocket). If `url` is not provided on connect, the saved page URL is used for redirect. Use `GET/PUT /api/stored-sessions/{session_id}` to read or update metadata (e.g. redirect URL). To move or edit individual persisted blobs without a live browser, use `GET/PUT /api/stored-sessions/{session_id}/cookies` (JSON array of cookie objects), `GET/PUT .../local-storage`, `GET/PUT .../session-storage` (both JSON objects with string keys and string values), `GET/PUT .../indexeddb` (IndexedDB snapshot object), and `GET/PUT .../cache-storage` (Cache Storage snapshot object). `DELETE /api/stored-sessions/{session_id}` wipes all persisted state for a session.

## Limitations & fallbacks

Real-world heavy pages (Amazon, marketplaces, dashboards) hit these. Know the fallback for each:

- **Prefer text/markup extraction over screenshots** — For reading page content, `/text`, `/json` (accessibility snapshot), and `/html` are *far* more efficient than `/screenshot` or `/vnc/screenshot`: they return compact, parseable structure instead of a large base64 image, so they cost a fraction of the tokens/bandwidth and give you selectors to act on. **Default to text/markup; use screenshots only for visual verification, pixel-level layout, or canvas/`<iframe>`/non-DOM UI.**
- **CDP frame limit (now 5 MiB)** — `/text`, `/json`, and `/html` return over a CDP WebSocket whose frame cap was raised from 1 MiB to **5 MiB**, so they now succeed on most heavy pages. If a page is still too large and you get `502` / `frame exceeds limit ... bytes`, **then** fall back: prefer narrowing first (`/text?mode=readability` (default), `/json?filter=interactive`) before resorting to a **clipped `/screenshot`** (`x,y,width,height` + lower `quality`) or `/vnc/screenshot` (framebuffer, independent of the CDP limit).
- **Prefer `fill` over `type` for form fields** — `type` does `focus()` + `Input.insertText`; some controlled/React inputs don't register it. `fill` does select-all + insertText with real input events and is the reliable choice for text fields. Use `type` only for appending to plain inputs.
- **To submit a form, use `submit` (not `press` Enter)** — a synthetic `press` Enter does not perform the browser's default submit. Use `{"kind":"submit","selector":"<form or a field in it>"}`, or click the submit button by selector (selector `click` does a DOM `element.click()`).
- **Never type secrets yourself — use `request-fill` ("Keeper")** — for passwords, login codes, 2FA, or any value you must not see, call `POST /api/sessions/{id}/request-fill` instead of `fill`/`type`. **This is THIS service's own built-in secure credential fill — "Keeper" is the user's companion app for it. It is NOT OpenClaw `secrets`/`SecretRefs` (config-backed values); do not conclude "there's no keeper" because OpenClaw secrets has no live prompt — this endpoint IS the live prompt.** The user supplies the value out-of-band in their Keeper app (which shows your `message` + a screenshot of the field area) and the **service** types it into the field; the value is never returned to you or logged. It's **async**: you get `{request_id, status:"pending"}`, then poll `GET /api/sessions/fill-status/{request_id}` (tool `get_fill_status`) until `filled` / `cancelled` / `timeout` / `error`.
  - **Default to this for any login.** Don't ask the user to paste a password into chat. Order of preference: (1) `request-fill`; (2) if it returns **`status:"no_keeper"`** (no Keeper app connected), have the user sign in themselves via the **live VNC view** (you never see the password) — the session then persists logged-in; (3) only as a last resort, with the user's explicit consent, accept a value they provide.
  - **One field:** `{"selector":"input[name=password]","label":"Password","field":"password","message":"Logging into Telegram to read your unread chats"}`.
  - **Multiple fields in one prompt (max 50):** `{"fields":[{"selector":"#user","label":"Username","field":"login"},{"selector":"#pass","label":"Password","field":"password"}],"message":"Signing in"}`.
  - **`field`** sets the prompt kind: `password` (default, masked) / `code` / `login` / `email` / `text`. **`length`** caps the input (1–4096); **`format`** constrains it (`email`, `numeric`/`digits`, or a regex). Set them when you know the value's shape — see docs/keeper-fill-formats.md.
  - **Payment cards** — use the card field kinds so the Keeper renders card-aware inputs and the user never exposes card data to you: `card-holder-name`, `card-number` (masked; `format` is a `#`-mask, default `################`, e.g. `"#### #### #### ####"`; submitted digits-only), `card-cvv` (masked), `card-exp` (`format` is a date template — `MM/YY` default, or `MM/YYYY` / `YY` / `YYYY` / `MM` for split month/year fields), `card-billing-address` (`format` names a component: `ADDRESS_LINE1`/`ADDRESS_LINE2`/`CITY`/`ZIP`/`STATE`/`COUNTRY` → single-line; **omit `format` for the whole address** → multi-line). One field per page input. **Dropdowns:** if the target is a `<select>` (expiry month/year, state, country), the service selects the matching `<option>` automatically — point the same `card-exp`/`card-billing-address` field at the `<select>`. Example: `{"fields":[{"selector":"#num","label":"Card number","field":"card-number"},{"selector":"#exp","label":"Expiry","field":"card-exp"},{"selector":"#cvv","label":"CVV","field":"card-cvv"},{"selector":"#zip","label":"ZIP","field":"card-billing-address","format":"ZIP"}],"message":"Enter card to check out"}`.
  - **One proof screenshot** is shown for the request. Pass **`screenshot_selector`** (or `screenshot_selectors`) to control what's captured — **prefer the whole `<form>`/container** (e.g. `"screenshot_selector":"form#login"`) so the user sees the form in context. Defaults to the field selectors' union if omitted.
  - Full protocol: docs/keeper-protocol.md.
- **Actions can report `{"ok": true}` without taking effect** — a `click` resolves the element box and dispatches a mouse event; if the target is off-viewport, covered by an overlay/sticky bar, or the page is a SPA mid-update, the event can be a no-op even though the call "succeeds". **Always verify state after any state-changing action** (re-screenshot, or re-check the relevant page e.g. the cart) rather than trusting `ok`. Prefer **selector-based** clicks over bare `x,y`; coordinate clicks on cart/checkout pages may also be blocked by host safety policy. If a selector click no-ops, try scrolling it into view first (`{"kind":"scroll"}`) or click via a screenshot-derived coordinate.
- **Session lifetime & reopening** — A session with **no live viewer/client** (`active_ws_connections: 0`, e.g. one created purely via the API/MCP) is reclaimed after ~5 minutes idle, and **any service restart/deploy drops all live sessions**. The stored state survives, so **to reopen/resume, just create a session with the SAME `session_id`** — it relaunches the browser and restores the full profile (you stay logged in). List resumable ids with `GET /api/stored-sessions`. For multi-step tasks: keep acting (each call resets idle), avoid long external pauses, and `ping` between steps.
- **Connecting/disconnecting (incl. CDP/Playwright) does not destroy the session** — opening a WebSocket/CDP connection (e.g. `connectOverCDP`) and closing it leaves the session running; it's reclaimed only by the idle timeout or an explicit `DELETE`. So a client may connect, work, disconnect, and reconnect later to the same live session without losing it.
- **Encrypted sessions reopen the same way** — if a session was created with `encrypt_with_api_key`, you reopen it identically: create with the same `session_id` using the same API-key/OAuth auth you use for every call. The encryption key is derived **server-side from your token** — you never see, pass, or "handle" it. Don't avoid reopening an encrypted session; it is not a special case.
