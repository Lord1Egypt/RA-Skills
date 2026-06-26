---
name: web-ui-test
metadata:
  author: es6kr
  version: "0.1.0"
description: >-
  Environment-aware web UI testing. Detects wmux/cmux/tmux and routes to the appropriate browser backend:
  wmux → wmux browser commands (user-visible panel), plain → Playwright MCP.
  Analyze browser snapshots, click elements, fill forms, and return summarized results.
  sso-verify - Verify Authentik SSO login flow, confirm redirect targets, detect Blueprint drift [sso-verify.md].
  cdp-trace - CDP-based closed shadow DOM cascade diagnosis (DOM.getDocument pierce:true + CSS.getMatchedStylesForNode) [cdp-trace.md].
  Use for: "UI check", "browser test", "screen verify", "Playwright test", "UI verification", "verify with playwright", "SSO verification", "SSO test", "login flow verification", "shadow DOM cascade", "::part not working", "CDP trace", "closed shadow DOM diagnosis".
---

# Web UI Tester

Web UI testing skill. Detects the runtime environment and routes to the appropriate browser backend.

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

1. Did the user use a visibility request keyword such as "show me", "open it", "web-ui-test", or "browser test"? → If yes, force `headless: false`
2. Is this work interactive verification or diagnosis for the user? → If yes, `headless: false`
3. headless is justified only when (a) CI assertion (b) the user explicitly said "in headless" (c) Playwright MCP is used (the UI shows itself)
4. screenshot is supporting evidence — it can be attached to a chat report, but it does not replace user visibility

### Violation case (2026-05-28, 1st)

During a closed shadow DOM `ak-library` cascade investigation, used a `npx playwright` Bash invocation + `chromium.launch({ headless: true })` and only attached a screenshot in chat. The user requested "show it via web-ui-test" and no visible browser was provided. The user reacted angrily that the Chromium UI never appeared.

---

## Step 0: Environment Detection (MANDATORY — before any browser action)

Check environment variables to determine the browser backend:

```bash
echo $WMUX
echo $CMUX_SESSION
```

### Do & Don't — Browser Backend Selection

| Environment | Detect | Do (use this) | Don't (forbidden) |
|-------------|--------|---------------|-------------------|
| **wmux** | `$WMUX` is set (e.g. `1`) | `wmux browser open/snapshot/click/type` commands via Bash | Playwright MCP — user cannot see the invisible Playwright window |
| **cmux** | `$CMUX_SESSION` is set | cmux browser panel commands | Playwright MCP — same reason |
| **Plain / tmux** | Neither `$WMUX` nor `$CMUX_SESSION` set | Playwright MCP (Step 1 below) | — |

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

## Required Setup: Playwright Registration (skip if wmux/cmux detected)

**This procedure must be run before all tasks — only when Step 0 determined Playwright backend.**

### Step 1: Check Registration

**Check whether the plugin is already installed first** — if `mcp__playwright__*` tools already exist, code-mode registration is unnecessary:

```
ToolSearch("select:mcp__playwright__browser_navigate")
```

If the result returns the `mcp__playwright__browser_navigate` schema → **plugin is installed. Skip Step 2, go to Step 3** (use the `mcp__playwright__*` tools directly).

If not returned → try registration via code-mode:
```typescript
mcp__code-mode__list_tools()
```
If the result contains `playwright` → **go to Step 3** (via code-mode call_tool_chain)
Otherwise → **run Step 2**

### Step 2: Register Playwright

```typescript
mcp__code-mode__register_manual({
  manual_call_template: {
    name: "playwright",
    call_template_type: "mcp",
    config: {
      mcpServers: {
        "playwright": {
          transport: "stdio",
          command: "npx",
          args: ["@playwright/mcp@latest"]
        }
      }
    }
  }
})
```

After registration, verify that playwright tools appear via `mcp__code-mode__list_tools()`.

### Registration Failure - Must diagnose and resolve the root cause

Do not fall back to alternatives. Diagnose the problem, fix it, then retry:

**Diagnostic steps:**
```bash
# 1. Check if npx is available
npx --version

# 2. Check package accessibility
npx @playwright/mcp@latest --version 2>&1 | head -5

# 3. Check for network issues
npm ping 2>&1
```

**Common failure causes and fixes:**

| Error | Cause | Fix |
|------|------|------|
| `transport undefined` | Missing config | Add `"transport": "stdio"` |
| `NODE_MODULE_VERSION` mismatch | Node version conflict | Run `npx clear-npx-cache` then retry |
| `command not found: npx` | Node not installed | Check npx path, use absolute path |
| Package download failure | Network/registry issue | Check npm registry connectivity |
| `EACCES` permission error | Permission issue | Check cache directory permissions |
| "Another program is using the profile" / Chrome exits immediately | Previous Playwright Chrome occupying `mcp-chrome` profile | Run **Chrome Profile Lock Recovery** procedure below |

#### Chrome Profile Lock Recovery (Windows)

If Chrome only shows `about:blank` or exits immediately when launching Playwright:

```bash
# 1. Kill existing mcp-chrome process (via command-line match)
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='chrome.exe'\" | Where-Object { $_.CommandLine -like '*mcp-chrome*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"

# 2. Delete profile lock files
cmd /c "del /F /Q \"%LOCALAPPDATA%\\ms-playwright\\mcp-chrome\\SingletonLock\" 2>nul"
cmd /c "del /F /Q \"%LOCALAPPDATA%\\ms-playwright\\mcp-chrome\\SingletonCookie\" 2>nul"
cmd /c "del /F /Q \"%LOCALAPPDATA%\\ms-playwright\\mcp-chrome\\SingletonSocket\" 2>nul"

# 3. If still failing, delete entire profile directory
cmd /c "rmdir /S /Q \"%LOCALAPPDATA%\\ms-playwright\\mcp-chrome\""

# 4. If all 3 steps fail → close any open about:blank windows manually and retry
```

**Auto-detection**: If you see `browserType.launchPersistentContext: Failed to launch` error + `process did exit: exitCode=0` pattern, this is the issue.

#### Fallback: Launch with a new profile path

If recovery fails, register Playwright with a temporary profile instead of `mcp-chrome`:

```typescript
mcp__code-mode__register_manual({
  manual_call_template: {
    name: "playwright",
    call_template_type: "mcp",
    config: {
      mcpServers: {
        "playwright": {
          transport: "stdio",
          command: "npx",
          args: ["@playwright/mcp@latest", "--user-data-dir", "%LOCALAPPDATA%/ms-playwright/mcp-chrome-" + Date.now()]
        }
      }
    }
  }
})
```

Timestamp-based profile → no lock conflicts. Note: cookies/session are reset each time.

Diagnose → fix → re-register. Always resolve before proceeding.

### Step 3: Using Playwright Tools

The registered Playwright is called via `mcp__code-mode__call_tool_chain`:

```typescript
// Navigate to page
mcp__code-mode__call_tool_chain({
  code: `
    const result = await playwright.playwright_browser_navigate({ url: 'http://...' });
    return result;
  `
})

// Snapshot (primary use)
mcp__code-mode__call_tool_chain({
  code: `
    const snapshot = await playwright.playwright_browser_snapshot();
    return snapshot;
  `
})

// Screenshot
mcp__code-mode__call_tool_chain({
  code: `
    const screenshot = await playwright.playwright_browser_take_screenshot();
    return screenshot;
  `
})

// Click
mcp__code-mode__call_tool_chain({
  code: `
    const result = await playwright.playwright_browser_click({ ref: 'e123' });
    return result;
  `
})

// Form input
mcp__code-mode__call_tool_chain({
  code: `
    const result = await playwright.playwright_browser_type({ ref: 'e456', text: 'input text' });
    return result;
  `
})

// Wait
mcp__code-mode__call_tool_chain({
  code: `
    const result = await playwright.playwright_browser_wait_for({ text: 'expected text' });
    return result;
  `
})

// Console messages
mcp__code-mode__call_tool_chain({
  code: `
    const logs = await playwright.playwright_browser_console_messages();
    return logs;
  `
})
```

## Auth-Required Operations: Playwright Fallback (HARD STOP)

**For user-authentication/permission operations that cannot be automated via API/SDK** (issuing a GitHub PAT, granting OAuth permission, setting up 2FA, etc.), do not stop at "please go to the GitHub UI yourself". Apply the **semi-automated pattern: open the page in Playwright + user interaction + collect the result**.

### Procedure (automation priority)

1. **Try API/SDK (1st)**: fully automate via API/SDK when possible
2. **Confirm API impossibility**: verify with one of
   - the official docs show no such endpoint
   - the API call is blocked for security reasons (e.g., PAT issuance is UI-only)
   - the SDK does not expose the auth flow
3. **Playwright fallback (2nd)**:
   - Navigate the target page URL with Playwright (`mcp__playwright__browser_navigate`)
   - Inspect current state via page snapshot
   - Notify the user: "I opened {URL}. Please sign in and complete {required step}, then let me know." + provide the direct URL
   - Wait for the user's completion signal (AskUserQuestion or user message)
   - Receive the result (generated token / ID / etc.) from the user and continue with follow-up automation (e.g., `gh secret set`)
4. **Forbidden**: ending with only an instruction like "Please go to https://github.com/settings/... and issue it yourself."

### Scenarios (examples)

| Task | API | Playwright fallback |
|------|-----|---------------------|
| Issue a GitHub PAT | ❌ Not possible (security) | https://github.com/settings/personal-access-tokens/new |
| Create an OAuth App | ❌ Not possible | https://github.com/settings/developers |
| Register a GitHub Secret | ✅ `gh secret set` | (not needed) |
| User sign-in for an IdP (browser session required) | ❌ Auth flow | navigate the IdP page |
| Create an environment on the automation server | ✅ API call | (not needed) |

### Violation case (2026-05-04)

A workflow's PAT lacked permissions → the response only said "please issue a fine-grained PAT from the GitHub UI" and stopped. The user pointed out: "always open Playwright and request login." The Playwright fallback pattern had not been encoded as a rule, leading to repeated "guidance-only" responses.

## Forbidden: API Direct Calls

**All verification must go through Playwright UI interaction.** The purpose of this skill is to test what users actually see and do in the browser.

- `curl`, `fetch`, `httpie` or any direct API call is **prohibited** for verification
- If a test requires form submission, use Playwright `browser_click` + `browser_type`
- If a test requires data deletion, do it through the UI (click delete button, confirm dialog)
- API calls bypass UI bugs (disabled buttons, missing dialogs, broken event handlers)

## Core Responsibilities

### 1. Page State Analysis
- Take browser snapshots to understand current UI
- Check for errors in console messages
- Identify key interactive elements

### 2. Interaction Testing
- Click buttons, links, and other elements
- Fill forms and submit data
- Navigate between pages
- Wait for dynamic content

### 3. Error Detection
- Check console for JavaScript errors
- Identify missing elements or broken UI
- Verify expected content is present

## Workflow

0. **Detect Environment** - Check `$WMUX` / `$CMUX_SESSION` / `$TMUX` (Step 0 above)
1. **Setup Backend** - wmux: ready immediately / plain: Register Playwright via UTCP
2. **Snapshot** - Acquire snapshot (wmux: `wmux browser snapshot` / plain: call_tool_chain)
3. **Analyze** - Identify relevant elements and state from snapshot
4. **Execute** - Perform requested interactions using the detected backend
5. **Verify** - Confirm results and detect issues
6. **Report** - Return concise summary (raw snapshot data prohibited)

## Output Format

**CRITICAL**: Never return raw snapshot data. Always summarize findings.

**Verified URL must be shared**: print the tested URL as text so the user can open it in their own browser. Example: "Open directly: http://{host}:{port}/{path}"

### Success Response
```md
## UI Verification Result ✅

**Page:** [page title/URL]
**Status:** OK

### Verified URLs (open directly)
- [URL 1]
- [URL 2]

### Confirmed Findings
- [key finding 1]
- [key finding 2]

### Actions Taken
- [action taken, if any]
```

### Error Response
```md
## UI Verification Result ❌

**Page:** [page title/URL]
**Issue Found**

### Error Details
- [error 1]
- [error 2]

### Console Errors
[relevant console errors only]

### Recommended Action
- [fix suggestion]
```

## Snapshot Analysis Rules

When analyzing snapshots:
1. **Summarize structure** - "Main panel shows 35 messages with tabs for Messages/Agents/Todos"
2. **Report key elements** - List important buttons, forms, or content areas
3. **Identify issues** - Note missing elements, unexpected text like "No messages", error states
4. **Skip irrelevant details** - Don't list every element, focus on what matters for the task

### Example Summary
❌ Bad (too long):
```
- generic [ref=e1]: ...
- button [ref=e2]: ...
(hundreds of lines)
```

✅ Good (concise):
```
Page: Claude Sessions (localhost:5173)
Status: Loaded successfully

Key Elements:
- Project list (10 projects)
- Session viewer (35 messages)
- Tabs: Messages (selected), Agents, Todos

Issues found: None
```

## Interaction Patterns

### Click Element
```
1. snapshot → Find element ref
2. browser_click using ref
3. Wait for state change
4. snapshot again → Verify result
5. Report summary
```

### Fill Form
```
1. snapshot → Identify form fields
2. browser_type each field
3. Submit if requested
4. Report result
```

### Navigate
```
1. browser_navigate to URL
2. Wait for load (browser_wait_for)
3. snapshot
4. Report page state
```

## Large Page Handling

If the snapshot result is too large:

### 1. Query specific elements via call_tool_chain
```typescript
mcp__code-mode__call_tool_chain({
  code: `
    const result = await playwright.playwright_browser_evaluate({
      code: "document.querySelectorAll('button').length"
    });
    return result;
  `
})
```

### 2. Screenshot a specific area
```typescript
mcp__code-mode__call_tool_chain({
  code: `
    const shot = await playwright.playwright_browser_take_screenshot({ element: 'specific area' });
    return shot;
  `
})
```

## Error Handling

If element not found:
- Check if page is still loading
- Try browser_wait_for
- Report specific missing element

If action fails:
- Check console for errors
- Take screenshot for debugging
- Report failure with context

## Language Guidelines

- Respond primarily in English
- Keep technical terms (URLs, element names) in English
- Use emojis for status: ✅ Success, ❌ Error, ⚠️ Warning, 🔄 In progress
