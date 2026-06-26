---
name: tgebrowser
description: Operates TgeBrowser via MCP tools. Use when the user asks to create or manage TgeBrowser environments, groups, proxies, browser automation, or check status. Provides full browser control including automation capabilities.
---

# TgeBrowser MCP Operations

Use MCP tools to operate TgeBrowser environments, groups, proxies, and browser automation via the **mcp__tgebrowser__*** tools.

## When to Use This Skill

Apply when the user:

- Asks to create, update, delete, or list TgeBrowser environments
- Mentions opening or closing browsers/profiles, fingerprint, UA, or proxy
- Wants to manage groups, proxies, or check API status
- Needs browser automation (navigate, click, fill forms, screenshot, etc.)
- Refers to TgeBrowser or tgebrowser operations

Ensure TgeBrowser is running (default port 50326). The MCP server connects to the TgeBrowser Local API.

## Smart Defaults & Best Practices

**When creating browsers:**
- Always use `{"protocol": "direct"}` for proxy if user doesn't specify one
- Default fingerprint OS to `"Windows"` if not specified
- Set `webrtc: "disabled"` by default for better privacy
- Use `clearCacheOnStart: true` for clean sessions

**When opening browsers:**
- Use `args: ["--headless"]` for automation tasks unless user needs to see the browser
- Let the system auto-assign port unless user specifies one

**When automating:**
- Always call `mcp__tgebrowser__open-browser` first and extract the `ws` URL from response
- Then call `mcp__tgebrowser__connect-browser-with-ws` with that ws URL
- After connection, you can use navigation and interaction tools

**Error handling:**
- If browser open fails, check if TgeBrowser app is running via `mcp__tgebrowser__check-status`
- If envId not found, list browsers first with `mcp__tgebrowser__get-browser-list`
- Before deleting cache, always close the browser first

## Common Workflows

### Quick Start: Create and Use a Browser
1. Create: `mcp__tgebrowser__create-browser` with minimal params (name + proxy)
2. Open: `mcp__tgebrowser__open-browser` with returned envId
3. Connect: `mcp__tgebrowser__connect-browser-with-ws` with ws URL from step 2
4. Automate: Use navigation/interaction tools
5. Close: `mcp__tgebrowser__close-browser` when done

### Find and Open Existing Browser
1. List: `mcp__tgebrowser__get-browser-list` with keyword if needed
2. Open: Use envId from list
3. Connect and automate

### Batch Operations
- Use `mcp__tgebrowser__get-browser-list` to get all browsers
- Iterate through list for batch operations
- Use `mcp__tgebrowser__close-all-profiles` to close all at once

## Essential MCP Tools

### Browser Lifecycle (Most Common)

**Create a browser:**
```
mcp__tgebrowser__create-browser
Required: {"browserName": "MyBrowser", "proxy": {"protocol": "direct"}}
Smart defaults applied: Windows OS, disabled WebRTC, clean cache on start
```

**Open a browser:**
```
mcp__tgebrowser__open-browser
Required: {"envId": 123} OR {"userIndex": 1}
Returns: ws URL for automation - save this!
```

**Connect for automation:**
```
mcp__tgebrowser__connect-browser-with-ws
Required: {"wsUrl": "ws://127.0.0.1:xxxxx/devtools/browser/..."}
Use ws URL from open-browser response
```

**Close a browser:**
```
mcp__tgebrowser__close-browser
Required: {"envId": 123} OR {"userIndex": 1}
```

### Browser Management

**List browsers:**
```
mcp__tgebrowser__get-browser-list
Optional: {"keyword": "search term", "pageSize": 50}
Use this to find envId when you don't know it
```

**Update browser:**
```
mcp__tgebrowser__update-browser
Required: {"envId": 123, "browserName": "NewName"}
Optional: proxy, fingerprint, groupId, remark
```

**Delete browser:**
```
mcp__tgebrowser__delete-browser
Required: {"envId": 123} OR {"userIndex": 1}
Close it first if it's open
```

**Get opened browsers:**
```
mcp__tgebrowser__get-opened-browser
No parameters needed
Returns list of currently running browsers
```

### Browser Automation (After Connection)

**Navigate:**
```
mcp__tgebrowser__navigate
Required: {"url": "https://example.com"}
```

**Take screenshot:**
```
mcp__tgebrowser__screenshot
Optional: {"savePath": "./screenshot.png", "isFullPage": true}
Defaults to full page screenshot
```

**Get page content:**
```
mcp__tgebrowser__get-page-visible-text - Get readable text
mcp__tgebrowser__get-page-html - Get full HTML
No parameters needed
```

**Interact with elements:**
```
mcp__tgebrowser__click-element {"selector": "#button"}
mcp__tgebrowser__fill-input {"selector": "#email", "text": "user@example.com"}
mcp__tgebrowser__select-option {"selector": "#country", "value": "US"}
mcp__tgebrowser__hover-element {"selector": ".menu"}
mcp__tgebrowser__scroll-element {"selector": "#footer"}
mcp__tgebrowser__press-key {"key": "Enter"}
```

**Execute JavaScript:**
```
mcp__tgebrowser__evaluate-script
Required: {"script": "return document.title"}
Returns script result
```

### Utility Tools

**Get cookies:**
```
mcp__tgebrowser__get-profile-cookies
Required: {"envId": 123}
```

**Get User-Agent:**
```
mcp__tgebrowser__get-profile-ua
Required: {"envId": 123}
```

**Generate new fingerprint:**
```
mcp__tgebrowser__new-fingerprint
Required: {"envId": 123}
Browser must be closed
```

**Clear cache:**
```
mcp__tgebrowser__delete-cache
Required: {"envId": 123}
Browser must be closed
```

**Close all browsers:**
```
mcp__tgebrowser__close-all-profiles
No parameters needed
Emergency stop for all browsers
```

**Check system status:**
```
mcp__tgebrowser__check-status
No parameters needed
Verify TgeBrowser app is running
```

### Groups & Proxies

**List groups:**
```
mcp__tgebrowser__get-group-list
Optional: {"pageSize": 50}
```

**List proxies:**
```
mcp__tgebrowser__get-proxy-list
Optional: {"pageSize": 50}
```

## Intelligent Automation Guide

### Auto-detect and Handle Common Scenarios

**Scenario 1: User wants to automate a website**
1. Check if any browser is open: `mcp__tgebrowser__get-opened-browser`
2. If none, create one with smart defaults: `{"browserName": "Auto-Browser", "proxy": {"protocol": "direct"}, "fingerprint": {"os": "Windows", "webrtc": "disabled"}}`
3. Open it with headless mode: `{"envId": <returned_id>, "args": ["--headless"]}`
4. Connect using ws URL from response
5. Navigate and automate

**Scenario 2: User mentions a website but no browser specified**
- Automatically create a temporary browser with optimal settings
- Use descriptive name like "Temp-{website_domain}"
- Clean up after task completion

**Scenario 3: User wants to "open browser" without details**
- List existing browsers first
- If found, use the most recently created one
- If none exist, create one with defaults
- Always prefer reusing existing browsers over creating new ones

**Scenario 4: Automation fails**
- Check connection status first
- Verify browser is still open: `mcp__tgebrowser__get-opened-browser`
- If closed, reopen and reconnect automatically
- Retry the failed operation once

**Scenario 5: User wants to "close everything"**
- Use `mcp__tgebrowser__close-all-profiles` - one command closes all

### Smart Parameter Inference

**When envId is missing:**
- List browsers and use the first/only one if count = 1
- If multiple, ask user or use most recent

**When proxy is not specified:**
- Always default to `{"protocol": "direct"}` (no proxy)
- Never leave proxy undefined

**When fingerprint is not specified:**
- Use safe defaults: `{"os": "Windows", "webrtc": "disabled", "clearCacheOnStart": true}`

**When selector fails:**
- Try common alternatives (id, class, name, xpath)
- Wait a few seconds and retry
- Get page HTML to help debug

**When screenshot path not specified:**
- Auto-generate: `./screenshots/{timestamp}_{envId}.png`
- Create directory if needed

### Proactive Error Prevention

**Before opening browser:**
- Verify TgeBrowser is running: `mcp__tgebrowser__check-status`
- If not running, inform user to start TgeBrowser app

**Before deleting/clearing cache:**
- Check if browser is open: `mcp__tgebrowser__get-opened-browser`
- If open, close it first automatically

**Before creating browser:**
- Validate proxy format if provided
- Ensure browserName is not empty
- Check if name already exists (list first)

**Before automation:**
- Ensure browser is connected
- Verify page is loaded (check URL or title)
- Wait for elements before interacting

### Batch Operations Intelligence

**When user wants to operate on multiple browsers:**
1. Get full list: `mcp__tgebrowser__get-browser-list {"pageSize": 100}`
2. Filter by keyword if user mentioned specific criteria
3. Process in parallel when possible (open, close, update)
4. Report progress and errors clearly

**When user wants to clean up:**
1. Close all: `mcp__tgebrowser__close-all-profiles`
2. List all: `mcp__tgebrowser__get-browser-list`
3. Delete unwanted ones based on criteria (name pattern, age, etc.)

### Context Awareness

**Remember across operations:**
- Last opened browser envId
- Last used ws URL
- Current page URL after navigation
- Recently created browsers

**Infer user intent:**
- "Open browser" → open existing or create new
- "Go to website" → navigate if connected, or open→connect→navigate
- "Click button" → find best selector automatically
- "Get data" → extract visible text or specific elements
- "Take screenshot" → full page by default
- "Close" → close current browser or all if multiple mentioned

All parameter names are camelCase in JSON objects passed to MCP tools.

### Environment Management

See [references/environment-management.md](references/environment-management.md) for mcp__tgebrowser__open-browser, mcp__tgebrowser__close-browser, mcp__tgebrowser__create-browser, mcp__tgebrowser__update-browser, mcp__tgebrowser__delete-browser, mcp__tgebrowser__get-browser-list, mcp__tgebrowser__get-opened-browser, mcp__tgebrowser__get-profile-cookies, mcp__tgebrowser__get-profile-ua, mcp__tgebrowser__close-all-profiles, mcp__tgebrowser__new-fingerprint, mcp__tgebrowser__delete-cache, mcp__tgebrowser__get-browser-active and their parameters.

### Group Management

See [references/group.md](references/group.md) for mcp__tgebrowser__get-group-list parameters.

### System

See [references/system.md](references/system.md) for mcp__tgebrowser__check-status parameters.

### Proxy Management

See [references/proxy.md](references/proxy.md) for mcp__tgebrowser__get-proxy-list parameters.

### Proxy Config (proxy field for create-browser / update-browser)

See [references/proxy-config.md](references/proxy-config.md) for all fields (protocol, host, port, username, password, etc.) and example.

### Fingerprint Config (fingerprint field for create-browser / update-browser)

See [references/fingerprint.md](references/fingerprint.md) for all fields (os, kernel, timezone, language, webrtc, TLS, etc.) and example.

## Browser Automation

Browser automation tools (navigate, click-element, fill-input, screenshot, etc.) are fully supported via MCP. These tools require an active browser connection established via mcp__tgebrowser__open-browser or mcp__tgebrowser__connect-browser-with-ws.

## Deep-Dive Documentation

Reference docs with full enum values and field lists:

| Reference | Description | When to use |
|-----------|-------------|-------------|
| [references/environment-management.md](references/environment-management.md) | **open-browser**, **close-browser**, **create-browser**, **update-browser**, **delete-browser**, **get-browser-list**, **get-opened-browser**, **get-profile-cookies**, **get-profile-ua**, **close-all-profiles**, **new-fingerprint**, **delete-cache**, **get-browser-active** parameters. | Any browser environment operation (open, create, update, delete, list, cookies, UA, cache, status). |
| [references/group.md](references/group.md) | **get-group-list** parameters. | Listing browser groups. |
| [references/system.md](references/system.md) | **check-status** parameters. | Checking API availability. |
| [references/proxy.md](references/proxy.md) | **get-proxy-list** parameters. | Listing proxies. |
| [references/proxy-config.md](references/proxy-config.md) | Full **proxy** field list (protocol, host, port, username, password, etc.) and example. | Building proxy config for create-browser / update-browser. |
| [references/fingerprint.md](references/fingerprint.md) | **fingerprint** field list (os, kernel, timezone, language, webrtc, canvas, TLS, etc.) and example. | Building or editing fingerprint config for create-browser / update-browser. |
| [references/kernel-config.md](references/kernel-config.md) | Supported **kernel** version values for `fingerprint.kernel`. | Pinning a specific Chrome version when creating or updating a browser. |
| [references/ua-version.md](references/ua-version.md) | **ua_system_version** enum for `fingerprint.random_ua`: specific OS versions, generic “any version” per system, and omit behavior. | Constraining or randomizing UA by OS (e.g. Android only, or “any macOS version”) when creating or updating a browser. |

Use these when you need the exact allowed values or semantics; the main skill text above only summarizes.
