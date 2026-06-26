---
name: ubuntu-browser-session
description: Use when a request needs a real Ubuntu Server browser session with durable site login reuse, bounded manual login recovery, or host-side page inspection for protected sites.
metadata:
  version: 1.0.3
---

# Ubuntu Browser Session

Use the Ubuntu host browser like a long-lived local browser for the agent.

The primary model is site-centric:

- each important site keeps one default primary identity
- agent tasks reuse that default identity automatically
- non-default identities are allowed only when the user explicitly names a different `session-key`
- user help is only for first login, expired sessions, or unrecoverable challenges

## When To Use

- Open, inspect, or interact with a protected site from the Ubuntu Server host
- Reuse an already logged-in site session such as GitHub or Google
- Recover an expired or challenge-blocked session with one bounded round of user help
- Continue browser work on the host without re-authenticating every task

Representative requests:

- "Use the Ubuntu host browser and open this dashboard."
- "Reuse the existing GitHub login on the server."
- "Continue from the same Google session."
- "Recover this protected page with the least user help."

## Do Not Use

- General web research that only needs HTTP fetch or web search
- Local desktop browsing outside the Ubuntu Server host
- Cases where an API token or non-browser auth flow is enough

## Core Rules

- Default to one primary identity per site
- Do not guess between multiple accounts automatically
- Only use a non-default identity when the user explicitly names a different `session-key`
- Prefer local recovery before asking the user to take over
- Treat wrong-page drift as recoverable: first navigate back to the requested site in the same profile, then ask for help only if the target still lands on a login wall or challenge
- Finish the host-browser workflow before switching tools: if `open-protected-page.sh` returns `ready`, keep working from this skill's host browser context and do not switch to OpenClaw's generic `browser` profile or other browser tools unless this workflow is exhausted or the task explicitly requires a different browser stack

## Preferred Entry Point

Use the wrapper first:

```bash
{baseDir}/scripts/open-protected-page.sh --url 'https://target.example' --session-key default
```

The wrapper is responsible for:

- site-centric profile lookup
- session reuse
- target-page verification
- one automatic recovery attempt when the browser drifted to the wrong page
- bounded escalation to noVNC when user help is actually needed
- keeping work inside the host browser workflow by default instead of mixing in unrelated browser profiles

## Site Session Model

Durable default identities are tracked by canonical site, not just exact origin.

Examples:

- `github.com` -> default GitHub browser identity
- `google.com` -> default Google browser identity, including `myaccount.google.com`

Persistent state is split across:

- exact manifests for the live runtime and captured browser state
- a site session registry for default per-site reuse
- compatibility identity aliases for Google-family hosts

Important files:

- `~/.agent-browser/index/site-sessions.json`
- `~/.agent-browser/sessions/...`
- `~/.agent-browser/index/identity-profiles.json`

## Manual Login Recovery

When the wrapper cannot recover locally, it starts the assisted browser overlay and returns:

- a loopback noVNC URL for SSH tunnel usage
- a LAN noVNC URL when the host IP is known and noVNC is exposed on `0.0.0.0`

Typical outputs:

```text
http://127.0.0.1:6084/vnc.html?autoconnect=1&resize=remote
http://192.168.0.200:6084/vnc.html?autoconnect=1&resize=remote
```

Use the loopback URL if you are forwarding ports over SSH from Windows or another remote machine.

Use the LAN URL only when the host firewall and network allow direct access.

## Typical Workflow

1. Try `open-protected-page.sh` with the requested URL and desired `session-key`
2. Let the wrapper resolve the default site identity
3. If the browser is already logged in but sitting on the wrong page, let the wrapper navigate back to the requested site automatically
4. If the target page is ready, continue the task from this host browser workflow first
5. If the target page still shows a login wall or challenge, open the returned noVNC URL
6. After the user finishes the login and leaves the final page loaded, run:

```bash
{baseDir}/scripts/assisted-session.sh capture --origin 'https://target.example' --session-key default
```

That finalizes the wrapper-managed session state and updates the site session registry for later reuse.

Do not use `assisted-session.sh start` as a normal entrypoint. Start with `open-protected-page.sh` so site-centric profile resolution and wrong-page recovery stay in effect.

Only reach for unrelated browser tooling after this workflow fails to complete the task and you have a concrete reason the host browser workflow is insufficient.

## Environment Checks

```bash
command -v python3
command -v curl
command -v jq
command -v Xvfb
command -v x11vnc
command -v websockify
command -v google-chrome || command -v chromium || command -v chromium-browser
```

## Key Files

- `scripts/open-protected-page.sh`: main protected-site wrapper
- `scripts/assisted-session.sh`: bounded manual takeover and capture
- `scripts/site-session-registry.sh`: canonical per-site default session registry
- `scripts/profile-resolution.sh`: site-first profile selection with compatibility fallback
- `scripts/session-manifest.sh`: runtime manifest storage and verification support
- `scripts/browser-runtime.sh`: browser runtime, target selection, and page checks
- `scripts/cdp-eval.py`: CDP evaluation, page checks, and navigation
- `scripts/cdp-snapshot.py`: structured page content extraction via CDP

## CDP Tools

`cdp-eval.py` and `cdp-snapshot.py` stay generic by default.
Forum/search-result helpers are optional enhancements; read `references/forum-enhancements.md` only when the current page is a forum topic list, category page, or search results page and you need structured topic/result links or text-based clicking.

### cdp-eval.py

Evaluate page state or run JavaScript over the Chrome DevTools Protocol.

```bash
# Check for challenge pages
python3 {baseDir}/scripts/cdp-eval.py --port PORT --check challenge

# Check for login walls
python3 {baseDir}/scripts/cdp-eval.py --port PORT --check login-wall

# Get page info (title, url, body snippet)
python3 {baseDir}/scripts/cdp-eval.py --port PORT --check page-info

# Run arbitrary JavaScript
python3 {baseDir}/scripts/cdp-eval.py --port PORT --eval 'document.title'

# Click the first visible link whose text matches or contains the given phrase
python3 {baseDir}/scripts/cdp-eval.py --port PORT --click-link-text 'Pricing'

# Navigate to a URL and wait for load
python3 {baseDir}/scripts/cdp-eval.py --port PORT --navigate 'https://example.com' --wait-navigation

# Navigate, wait for load, then check page state
python3 {baseDir}/scripts/cdp-eval.py --port PORT --navigate 'https://example.com' --wait-navigation --check page-info

# Navigate and wait for a specific element to appear (10s timeout)
python3 {baseDir}/scripts/cdp-eval.py --port PORT --navigate 'https://example.com' --wait-for '#main-content'
```

Parameters:

- `--port PORT` (required): CDP HTTP/WebSocket port
- `--target-id ID`: specific target from `/json/list`
- `--check {challenge,login-wall,page-info}`: built-in page state checks
- `--eval EXPRESSION`: arbitrary JavaScript for `Runtime.evaluate`
- `--navigate URL`: navigate to URL via `Page.navigate`
- `--click-link-text TEXT`: click the first visible matching anchor; when combined with `--navigate`, pair it with `--wait-navigation` or `--wait-for` so the destination DOM is ready before clicking
- `--wait-navigation`: wait for `Page.loadEventFired` after `--navigate`
- `--wait-for SELECTOR`: poll for CSS selector to appear (timeout 10s)

### cdp-snapshot.py

Capture structured page content in generic formats by default, plus an optional forum/search-result helper format.

```bash
# Simplified markdown (default)
python3 {baseDir}/scripts/cdp-snapshot.py --port PORT

# Plain text extraction
python3 {baseDir}/scripts/cdp-snapshot.py --port PORT --format text

# Extract all links as title+href pairs
python3 {baseDir}/scripts/cdp-snapshot.py --port PORT --format links

# Extract topic/result links from the main content area (useful on forums/search pages)
python3 {baseDir}/scripts/cdp-snapshot.py --port PORT --format topic-links

# With character limit
python3 {baseDir}/scripts/cdp-snapshot.py --port PORT --max-chars 4000
```

Output: JSON to stdout `{"title": "...", "url": "...", "content": "..."}`

Parameters:

- `--port PORT` (required): CDP HTTP/WebSocket port
- `--target-id ID`: specific target from `/json/list`
- `--format {markdown,text,links,topic-links}`: output format (default: `markdown`)
- `--max-chars N`: truncate content to N chars (default: 8000, 0=unlimited)

For `topic-links`, `meta` is best-effort surrounding text truncated to 400 characters.

See also:

- `references/forum-enhancements.md`
- `references/use-cases.md`
- `references/session-manifest.md`
- `references/assisted-session-flow.md`
- `references/testing-matrix.md`
- `references/manual-fallback.md`
- `references/validation-findings.md`
