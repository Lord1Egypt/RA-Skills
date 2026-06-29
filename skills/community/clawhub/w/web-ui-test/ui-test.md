# UI Test (web-browser topic)

Analyze browser snapshots, click/fill/verify UI, diagnose page state. Part of the `web-browser` skill.

> **Backend**: detect the browser backend first via **SKILL.md Step 0** (wmux/cmux panel → user-visible, plain → Playwright MCP). The **user-visibility HARD STOP** also lives in SKILL.md Step 0 — apply it before any browser launch. This topic covers the UI-testing procedure itself.
>
> For closed shadow DOM `::part` cascade diagnosis → [cdp-trace.md](./cdp-trace.md). For browser-login-assisted token issuance → [credential-issue.md](./credential-issue.md).

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
