---
name: win11-visible-browser
description: Control, diagnose, or repair a visible Windows 11 Edge/Chrome browser from OpenClaw running in WSL2 via CDP. Use when browser automation should share the user's real visible browser session, existing tabs, cookies, logins, and state; when login, captcha, 2FA, approvals, or manual takeover require a human-in-the-loop; or when WSL2/OpenClaw browser control needs CDP, firewall, portproxy, attachOnly profile, or Windows browser troubleshooting.
metadata: {"openclaw":{"requires":{"bins":["openclaw","curl","ip"]}}}
---

# Win11 Visible Browser Automation

Use this skill when OpenClaw runs in WSL2/Linux but should work in a visible Windows 11 Edge/Chrome browser that the human can watch, use, and take over.

This is for legitimate assisted browsing in a normal visible browser session. Do not use it to bypass site protections, automate prohibited activity, or hide automation from the user.

## Safety gate

Before state-changing actions, state what/where/risk/rollback and wait for explicit confirmation. State-changing actions include editing OpenClaw config, creating Scheduled Tasks, changing Windows firewall/portproxy, starting/stopping browser processes, writing scripts outside the workspace, sending forms/messages, purchases, or account actions.

ClawScan risk mitigations to preserve:

- Prefer a dedicated browser profile by default; use a personal/logged-in profile only after explicit user approval.
- Do not proceed with browser, account, payment, form, firewall, portproxy, config, or Scheduled Task changes unless the action and rollback are clear.
- Verify Windows firewall rules are scoped to WSL/Hyper-V CIDR; never expose the CDP port to the LAN or Internet.
- Create persistent Scheduled Tasks only after explicit approval, and keep rollback documented with `Unregister-ScheduledTask`.

## Positioning

Prefer visible browser automation when the task benefits from:

- existing tabs already open in the user's browser;
- cookies, logins, extensions, and normal browser state;
- visible step-by-step human oversight;
- manual human help for login, captcha, 2FA, consent screens, account pickers, file dialogs, or sensitive approvals;
- sites that do not work well through `web_fetch` or a fresh/headless browser.

Use safe wording: this skill gives the agent access to a normal visible browser while keeping the human in the loop. It does not try to bypass anti-bot systems.


## Browser Resource Budget / Tab Hygiene

Visible browser control is expensive: it consumes tokens, Edge/Chrome memory, and CDP stability budget. Before using the visible browser, prefer cheaper tools when they satisfy the task.

### Cost ladder

Use the cheapest sufficient tool, in this order:

1. Local files, project notes, memory, or CLI output.
2. First-class APIs/CLIs (`clawhub`, `openclaw`, `curl`, source-specific tools).
3. `web_fetch` for readable public pages.
4. Browser `evaluate` for structured extraction from an already-open page.
5. Browser snapshot/screenshot for UI understanding or evidence.
6. Visible Edge/Chrome CDP only when logins, cookies, human-in-the-loop, visual verification, or sites that reject cheaper access are actually needed.

If the user explicitly asks to open a site/tab in the visible browser, do not debate whether the browser is necessary. Still check basic safety/resource risk first and report if opening another tab may overload the browser.

### Existing tabs are not agent-owned

Treat all tabs that existed before the current task as user state.

- Do not close, reload, navigate, or repurpose existing user tabs without explicit permission.
- Existing tabs already count against free system memory; do not double-subtract them in memory estimates.
- They still count against CDP complexity: many existing pages/iframes/workers can make automation unstable.
- If existing tabs leave too little resource budget, stop and ask for cleanup permission instead of taking over those tabs.

Classify tabs mentally:

- **User tabs**: existed before the task; do not touch.
- **User-requested tabs**: opened because the user explicitly asked; do not close unless asked.
- **Agent task tabs**: opened by the agent for the current task; save useful URLs and close/clean them when done.
- **Archived tabs**: URLs saved into a project file such as `browser-tabs-YYYY-MM-DD.md`; safe to close only after user approval.
- **Critical/manual tabs**: login, captcha, payment, forms, account settings; human-in-the-loop only.

### Preflight budget check

Before non-trivial visible-browser work, estimate both memory budget and CDP complexity budget. Prefer the helper:

```bash
{baseDir}/scripts/browser-budget-check.sh win-edge
```

If the helper is unavailable, inspect CDP directly:

```bash
WIN_IP=$(ip route | awk '/default/ {print $3; exit}')
curl -sS --max-time 8 "http://$WIN_IP:9223/json/list"
```

Decision inputs:

- current `page`, `iframe`, and `worker` target counts;
- whether reCAPTCHA/service workers are present;
- current browser memory when measurable;
- free system memory after existing user tabs;
- minimum number of new tabs required by the task;
- whether the task can use one reusable tab instead.

Approximate planning costs:

- simple/static tab: 50-150 MB;
- normal web app tab: 100-250 MB;
- heavy SPA/account dashboard: 250+ MB;
- iframe/worker-heavy or reCAPTCHA site: treat as high risk; do not open cards in parallel.

Memory rule of thumb:

- keep at least 1 GB safety headroom;
- if free memory after headroom is < estimated task cost, do not start;
- if unsure, use one tab and write progress to project files rather than opening more tabs.

CDP complexity stop rules:

- `targets > 30`: stop and propose inventory/cleanup;
- `pages > 10`: caution; avoid opening more tabs unless explicitly needed;
- `iframe + worker > max(6, pages * 2)`: stop; the site is spawning too much browser state;
- any reCAPTCHA burst: stop automation and switch to human-in-the-loop or project-file workflow;
- repeated `targetId`, `Execution context destroyed`, or timeout errors: refresh target inventory instead of retrying blindly.

### Minimal-tab workflow

Do not use the browser as task memory.

- Default to one list/search tab and, if needed, one reusable detail tab.
- Do not open a fan-out of many result cards/resumes/products.
- Extract links from a list into a project file first.
- Visit/detail one item at a time, record the result, then reuse or close the tab.
- Prefer `evaluate` to extract structured data; use snapshots only when the UI structure is unknown.
- Keep final chat replies compact: summary + path to saved project file, not full DOM dumps.

### Cleanup and archiving

At the end of a browser task:

1. Save useful URLs/data into the relevant project (`browser-tabs-YYYY-MM-DD.md`, `candidates.md`, `sources.md`, `progress.md`, etc.).
2. Report which agent-created tabs can be closed.
3. Close only agent-owned or user-approved archived tabs.
4. Leave user tabs and user-requested tabs alone.

For cleanup of a polluted browser session, first create a read-only inventory grouped by domain/type, deduplicate URLs, and write it to the project. Only after that, ask permission to close the relevant domain/targets.

## Recommended architecture

Use a dedicated Windows browser profile by default. Use the user's personal browser profile only when the user explicitly wants existing personal cookies/logins/tabs.

```text
OpenClaw Gateway in WSL2
  → OpenClaw browser profile (example: win-edge)
  → http://WINDOWS_WSL_GATEWAY_IP:9223
  → Windows portproxy/firewall relay
  → 127.0.0.1:9222
  → visible Windows 11 Edge/Chrome profile
```

Recommended defaults:

- OpenClaw browser profile: `win-edge` or `win-chrome`
- Windows CDP local port: `9222`
- WSL-visible relay port: `9223`
- Dedicated browser profile: `C:\ProgramData\OpenClaw\browser-profile`
- Startup/repair task: `OpenClaw-Start-Windows-Browser-CDP`

For implementation details, read `{baseDir}/references/setup.md`.

## Diagnose first

Run read-only checks before repair:

```bash
openclaw browser profiles
openclaw browser --browser-profile win-edge doctor
WIN_IP=$(ip route | awk '/default/ {print $3; exit}')
curl -sS --max-time 5 "http://$WIN_IP:9223/json/version"
```

Or use the bundled helper:

```bash
{baseDir}/scripts/check-win11-visible-browser.sh win-edge
```

If CDP works, smoke-test real browser control:

```bash
openclaw browser --browser-profile win-edge open https://example.com
openclaw browser --browser-profile win-edge snapshot --format aria
```

## Repair order

Repair in layers and stop when the layer works:

1. Confirm Windows Edge/Chrome is installed and can run visibly.
2. Start the browser with CDP on Windows localhost, usually `127.0.0.1:9222`.
3. Expose it to WSL with a Windows relay/portproxy, usually `0.0.0.0:9223 → 127.0.0.1:9222`.
4. Restrict Windows firewall to the current WSL/Hyper-V CIDR, not the whole LAN or Internet.
5. Configure an OpenClaw browser profile with `cdpUrl` pointing to the WSL-visible Windows endpoint and `attachOnly: true`.
6. Reload/restart Gateway if the profile is not visible.
7. Run doctor and a page/snapshot smoke test.

The bundled Windows repair script is `{baseDir}/scripts/start-win11-browser-cdp-for-openclaw.ps1`. Treat it as a template: review paths, profile name, browser path, ports, and firewall rule names before installing or running it.

## Common blockers

- `No supported browser found`: WSL cannot launch Windows Edge/Chrome as a local Linux browser; use remote CDP.
- Windows CDP works but WSL curl times out: fix portproxy/firewall/WSL subnet.
- Browser profile not found: OpenClaw config not loaded; reload/restart Gateway.
- WSL gateway IP changed: update `browser.profiles.<name>.cdpUrl` or rerun the documented repair flow.
- Existing tabs/logins are missing: you are probably using a dedicated profile, not the user's real profile. Ask before switching profiles.

## Evidence to report

When done, report:

- browser profile name and CDP URL tested;
- `openclaw browser --browser-profile <profile> doctor` result;
- `/json/version` result from WSL;
- Windows task/log status if relevant;
- smoke-test URL opened and snapshot result;
- any remaining manual human step needed.

## Data extraction

For structured data extraction (prices, search results, product specs, availability):

1. Snapshot the page once to understand the layout.
2. Use `act kind=evaluate` with a JavaScript function to extract clean data as JSON/strings in a single call.
3. Repeat `evaluate` for pagination or updated data; no new snapshot needed unless the DOM structure changes.

This uses orders of magnitude fewer tokens than snapshot-per-action loops.

Tips:

- If content loads lazily on scroll, scroll the container into view via evaluate before extraction.
- Extract all visible results in one pass: name, price, seller, delivery date, link.
- Some sites (Ozon, Wildberries, М.Видео) trigger antibot challenges on `web_fetch` but work through the visible CDP-attached browser.
- Яндекс Маркет generally works with both `web_fetch` and the visible browser.

## Visual result presentation

Beyond text, the visible browser lets you show results directly to the user:

- **Open result tabs** — after finding a product/article/video, open it in a labeled browser tab so the user can see and interact with it in real time.
- **Screenshot capture** — take a `screenshot` of the relevant page section and attach it to your response for instant visual confirmation.
- **Multi-tab orchestration** — open several search results at once with distinct labels (`label="product-1"`, `label="product-2"`), letting the user visually compare while you summarise.
- **Article/video handoff** — for tutorials or reviews, open the content in a tab and snapshot the key section so the user can continue watching/reading.
- **Evidence delivery** — when a specific piece of information is critical (price, address, phone, delivery date), snapshot exactly that block and deliver it for verification.