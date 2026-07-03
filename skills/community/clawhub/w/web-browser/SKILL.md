---
name: web-browser
metadata:
  author: es6kr
  version: "0.1.0"
description: |
  Environment-aware browser operations. Detects wmux/cmux/tmux and routes to the right backend
  (wmux/cmux panel → user-visible, plain → Playwright MCP, chrome-devtools → reuse the user's
  real logged-in session). Topics:
  ui-test - snapshots, click/fill/verify, closed shadow DOM cascade diagnosis (cdp-trace)
  [ui-test.md, cdp-trace.md].
  credential-issue - open service login via detected backend → wait for user sign-in → issue
  OR refresh an access key / token / secret / OAuth scope → hand off to follow-up automation
  (aws-cli, gh secret set, gh auth refresh, etc.) [credential-issue.md]. Covers both new
  issuance and existing-token scope expansion (PAT scope add, OAuth re-authorize, device-code).
  Use for: "UI check", "browser test", "screen verify", "Playwright test", "shadow DOM cascade",
  "::part not working", "CDP trace", "issue token", "service credential", "open login screen",
  "PAT refresh", "scope expansion", "device-code auth", "browser device-code".
---

# Web Browser

Environment-aware browser operations skill. Detects the runtime environment and routes to the
appropriate browser backend, then runs one of two workflows: UI testing/verification (`ui-test`) or
browser-login-assisted credential issuance (`credential-issue`).

## Topics

| Topic | Description | Guide |
|-------|-------------|-------|
| ui-test | Snapshot analysis, click/fill/verify, page-state diagnosis | [ui-test.md](./ui-test.md) |
| cdp-trace | CDP-based closed shadow DOM cascade diagnosis (DOM.getDocument pierce:true + CSS.getMatchedStylesForNode) | [cdp-trace.md](./cdp-trace.md) |
| credential-issue | service+command param → open login screen → wait for user login → issue access key/token/secret → hand off to automation | [credential-issue.md](./credential-issue.md) |

## Topic Dependencies

```
web-browser (Step 0: environment detection — shared by all topics)
  ├─→ ui-test (UI verification)
  │     └─→ cdp-trace (extends ui-test for closed shadow DOM)
  └─→ credential-issue (browser-login-assisted token/key issuance)
        └─→ chrome-devtools backend preferred (reuses the user's real logged-in session)
```

- **Step 0 (below) is shared** — every topic detects the backend first, then runs its workflow.
- `ui-test`, `cdp-trace` are the UI-testing family.
- `credential-issue` reuses the same backend routing + the user-visibility rule, generalized into a
  service+command parameterized auth flow.
- **Authentik SSO verification** (`sso-verify`) is **not** included in this skill — it remains in a
  separate local-only `sso-verify` skill (user-environment specific, untracked).

## CRITICAL — user visibility is the top priority (HARD STOP)

**The primary purpose of browser diagnosis/verification is "the user sees it on their own screen"**. Screenshot capture is **supporting evidence**, not a substitute for visibility.

| # | Don't | Do |
|---|-------|-----|
| 1 | Launch with `chromium.launch({ headless: true })` and only attach a screenshot in chat | `chromium.launch({ headless: false, slowMo: 500 })` — let the user follow in real time |
| 2 | "I showed the user a screenshot, so it's fine" | screenshot ≠ visible to the user. If the user says "show me", open a visible browser + slowMo |
| 3 | wmux/cmux/Playwright MCP disconnected → fall back to headless CLI | Even on CLI fallback, force `headless: false`. On a Windows desktop OS, a chromium GUI is available |
| 4 | "headless is faster and more stable by default" mindset | Speed costs user visibility. If the user says "show me", visibility wins |
| 5 | Playwright MCP disconnected → CLI fallback auto-selects headless | CLI fallback is also `headless: false`. headless is only for explicit non-interactive cases (e.g., CI assertion) |

### Self-check (every time before launching Playwright/chromium)

1. Did the user use a visibility request keyword such as "show me", "open it", "web-browser", or "browser test"? → If yes, force `headless: false`
2. Is this work interactive verification or diagnosis for the user? → If yes, `headless: false`
3. headless is justified only when (a) CI assertion (b) the user explicitly said "in headless" (c) Playwright MCP is used (the UI shows itself)
4. screenshot is supporting evidence — it can be attached to a chat report, but it does not replace user visibility

### Violation case (2026-05-28, 1st)

During a closed shadow DOM `ak-library` cascade investigation, used a `npx playwright` Bash invocation + `chromium.launch({ headless: true })` and only attached a screenshot in chat. The user requested "show it via web-ui-test" and no visible browser was provided. The user reacted angrily that the Chromium UI never appeared.

---

## Step 0: Environment Detection (MANDATORY — before any browser action)

Check environment variables AND CLI presence to determine the browser backend:

```bash
# wmux
echo "WMUX=$WMUX"
# cmux — detect via ANY of these (cmux app does NOT set CMUX_SESSION; use multi-var OR)
echo "CMUX_BUNDLE_ID=$CMUX_BUNDLE_ID"
echo "CMUX_PANEL_ID=$CMUX_PANEL_ID"
echo "CMUX_BUNDLED_CLI_PATH=$CMUX_BUNDLED_CLI_PATH"
# CLI fallback (env may be unset in nested shells but CLI still works)
command -v cmux && echo "cmux CLI present"
command -v wmux && echo "wmux CLI present"
```

### Do & Don't — Browser Backend Selection

| Environment | Detect (ANY true → environment matches) | Do (use this) | Don't (forbidden) |
|-------------|----------------------------------------|---------------|-------------------|
| **wmux** | `$WMUX` set OR `command -v wmux` succeeds | `wmux browser open/snapshot/click/type` commands via Bash | Playwright MCP — user cannot see the invisible Playwright window |
| **cmux** | `$CMUX_BUNDLE_ID` set OR `$CMUX_PANEL_ID` set OR `$CMUX_BUNDLED_CLI_PATH` set OR `command -v cmux` succeeds (e.g. `/Applications/cmux.app/Contents/Resources/bin/cmux`) | cmux browser panel commands | Playwright MCP — same reason |
| **Plain / tmux** | None of wmux/cmux signals present | Playwright MCP (Step 1 below) | — |

#### cmux detection — multi-var OR rationale

cmux app sets several env vars when launching a shell, **but `CMUX_SESSION` is NOT one of them** (a legacy guess by analogy with `WMUX`). Real vars observed in a cmux-launched shell:

- `CMUX_BUNDLE_ID` (e.g. `com.cmuxterm.app`)
- `CMUX_PANEL_ID` (UUID per panel)
- `CMUX_BUNDLED_CLI_PATH` (CLI absolute path)
- `CMUX_SHELL_INTEGRATION_DIR`
- `CMUX_AGENT_LAUNCH_*`
- `GHOSTTY_RESOURCES_DIR` (cmux uses Ghostty-based terminal)

`CMUX_SOCKET` is **set but often empty** — do not use it as the sole signal. Use the OR matrix above.

| # | Don't (single-var assumption) | Do (multi-var OR) |
|---|-------------------------------|-------------------|
| 1 | `[ -n "$CMUX_SESSION" ]` only check → false negative on cmux app | OR across `CMUX_BUNDLE_ID` / `CMUX_PANEL_ID` / `CMUX_BUNDLED_CLI_PATH` |
| 2 | Use `CMUX_SOCKET` as detection (empty in many cases) | Treat empty `CMUX_SOCKET` as no-signal; rely on the 3 vars above + CLI presence |
| 3 | Assume cmux env var name mirrors wmux (`*_SESSION`) | Verify against actual cmux app shell environment — vars differ per terminal multiplexer |

### wmux Browser Commands Reference

When `$WMUX` is set, use these instead of Playwright MCP.

**Invocation form**: the rest of this document uses the bare `wmux browser …` form, which is what runs when `wmux` is on `PATH` (the common case). If `wmux` is **not** on `PATH` in the current environment, substitute `node "$WMUX_CLI"` for `wmux` in every command below — `$WMUX_CLI` points to the same entry point. The two forms are interchangeable; pick whichever resolves on the current shell and use it consistently.

```bash
wmux browser open <url>          # navigate (= playwright navigate)
wmux browser snapshot            # get accessibility tree with @eN refs
wmux browser click @eN           # click element
wmux browser type @eN <text>     # type into element
wmux browser fill @eN <value>    # set input value
wmux browser get-text            # get page text
wmux browser screenshot          # capture screenshot
wmux browser eval <js>           # run JavaScript
wmux browser back                # go back
wmux browser forward             # go forward
wmux browser reload              # reload page
```

**Workflow**: `browser open <url>` → `browser snapshot` → read tree → `browser click/type @eN` → `browser snapshot` again.

**Refs (`@e1`, `@e2`...) expire after page changes** — always re-snapshot.

### Do & Don't — wmux vs Playwright Mapping

| Action | wmux (Do) | Playwright MCP (Don't in wmux) |
|--------|-----------|-------------------------------|
| Navigate | `Bash("wmux browser open <url>")` | `mcp__playwright__browser_navigate` |
| Snapshot | `Bash("wmux browser snapshot")` | `mcp__playwright__browser_snapshot` |
| Click | `Bash("wmux browser click @eN")` | `mcp__playwright__browser_click` |
| Type | `Bash("wmux browser type @eN text")` | `mcp__playwright__browser_type` |
| Screenshot | `Bash("wmux browser screenshot")` | `mcp__playwright__browser_take_screenshot` |
| Evaluate JS | `Bash("wmux browser eval <js>")` | `mcp__playwright__browser_evaluate` |
| Wait for text | Re-snapshot + check | `mcp__playwright__browser_wait_for` |

**Key difference**: wmux browser is visible to the user in real-time on the right panel. Playwright opens an invisible window the user cannot see.

---


## Quick Reference

After Step 0 backend detection, route to the topic:

| Goal | Topic | Entry |
|------|-------|-------|
| Verify a UI change, snapshot, click/fill | `ui-test` | [ui-test.md](./ui-test.md) |
| Diagnose `::part` not applying / closed shadow DOM cascade | `cdp-trace` | [cdp-trace.md](./cdp-trace.md) |
| Open a service login → wait for user login → issue access key/token | `credential-issue` | [credential-issue.md](./credential-issue.md) |

**Step execution order**: Step 0 (this file — detect backend + user-visibility rule) → read the
target topic `.md` → follow its procedure. The topic `.md` files hold the actual procedures; this
file is the shared backend-detection + index.
