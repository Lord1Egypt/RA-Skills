---
name: safari-control
description: Use Safari directly on macOS when work must happen in the user's real Safari session instead of a separate automation browser. Best for reading the current tab, inspecting the live session layout, operating Safari menu bar or native toolbar controls, reading page text and structure, running page JavaScript, waiting for page conditions, exporting page artifacts, and performing lightweight DOM interactions in the active Safari tab. If Safari JavaScript from Apple Events is disabled, guide the user to enable it or fall back to desktop-control for visual interaction.
---

# Safari Control

Use this skill when the task must happen in **Safari itself**:

- The user is already logged in there
- Safari extensions, cookies, or profiles matter
- You need the current tab, tab list, page URL, or page text
- A headless browser would not reflect the real session

Do **not** force Safari to behave like Playwright. Prefer Safari's session access and DOM helpers first, Safari native UI automation second, and `desktop-control` only for pointer-heavy UI.

## Core Tool

Run commands from the `safari-control` skill directory so the relative `scripts/` path resolves correctly.

```bash
swift scripts/safari_control.swift <command>
```

## Recommended Flow

Use this exact flow unless the task clearly starts in one specific layer:

1. Check environment and active page:

```bash
swift scripts/safari_control.swift doctor
swift scripts/safari_control.swift current --json
```

`doctor` is the branch point:

- `safari_js=false`: do not use DOM commands until the user enables JavaScript from Apple Events.
- `accessibility=false`: do not use native Safari chrome commands.
- `screenshot_background=false`: use `screenshot --mode foreground` when you need an image.
- If Safari is missing required permissions or features, tell the user before proceeding. In particular, check whether Safari allows Automation, JavaScript in the Smart Search field, and JavaScript from Apple Events. Enabling these unlocks more functionality, but also increases risk because automation and scripted interactions gain more power over the user's Safari session. If the user refuses, do not keep pushing the recommendation and continue with the reduced feature set.

2. If Safari session state matters, inspect it before mutating anything:

```bash
swift scripts/safari_control.swift list-windows --json
swift scripts/safari_control.swift list-tabs --json
```

3. If you need page content or web-page actions, verify DOM access:

```bash
swift scripts/safari_control.swift check-js
swift scripts/safari_control.swift snapshot --interactive-only --limit 30
```

4. Choose the lowest layer that fits:

- Prefer **DOM commands** for page content, forms, links, and standard web controls.
- Use **native Safari controls or menus** for the smart search field, toolbar buttons, tab groups, and menu bar commands.
- Use **desktop-control** only for extension popups, native pickers, pointer-heavy drag/drop, or UI Accessibility cannot expose.
- When you want to draw the user's attention to important content on the page, you may use JavaScript to visually highlight it, such as adding a red outline, background tint, or temporary annotation.

## Command Layers

### 1. Environment and Session

Use for machine-readable state and tab/window management.

```bash
swift scripts/safari_control.swift doctor
swift scripts/safari_control.swift current --json
swift scripts/safari_control.swift list-windows --json
swift scripts/safari_control.swift list-tabs --json
swift scripts/safari_control.swift save-session ./session.json --front-only
swift scripts/safari_control.swift restore-session ./session.json
swift scripts/safari_control.swift new-window https://example.com
swift scripts/safari_control.swift switch-window 2
swift scripts/safari_control.swift switch-tab 2 --window 1
swift scripts/safari_control.swift switch-tab-title 'Dashboard'
swift scripts/safari_control.swift switch-tab-url '/dashboard'
swift scripts/safari_control.swift duplicate-tab
swift scripts/safari_control.swift close-tab --tab 2 --window 1
swift scripts/safari_control.swift close-window --window 2
```

Rules:

- Prefer `--json` for agent-readable output.
- Most read-only page commands support `--window N --tab M`, so you can inspect background tabs without switching focus.
- `save-session` before invasive work when preserving the user's layout matters.
- `restore-session` is additive: it recreates windows and tabs, it does not merge with or close current ones.

### 2. Page Read and Inspect

Use when JavaScript from Apple Events is enabled and the target is inside the web page.

```bash
swift scripts/safari_control.swift snapshot --limit 20 --heading-limit 10 --form-limit 5
swift scripts/safari_control.swift snapshot --interactive-only --limit 30
swift scripts/safari_control.swift interactive --json
swift scripts/safari_control.swift query 'form input' --json
swift scripts/safari_control.swift element-info 'button[type=\"submit\"]'
swift scripts/safari_control.swift find-text 'Buy now' --json
swift scripts/safari_control.swift exists 'button[data-testid=\"submit\"]'
swift scripts/safari_control.swift count 'button'
swift scripts/safari_control.swift get-text --mode article
swift scripts/safari_control.swift extract-links --json
swift scripts/safari_control.swift extract-tables --json
swift scripts/safari_control.swift run-js 'document.title'
swift scripts/safari_control.swift eval-js 'document.querySelectorAll(\"a\").length'
```

Rules:

- Prefer `snapshot` before manual probing on unfamiliar pages.
- Prefer `snapshot --interactive-only` when you only need actionable controls and want smaller output.
- Prefer `get-text --mode article` before `body`; it is usually less noisy.
- Prefer `element-info` when a selector exists but behaves unexpectedly.

### 3. Page Actions and Waits

Use for standard DOM interactions after confirming the target is inside the page.

```bash
swift scripts/safari_control.swift focus 'input[name=\"email\"]'
swift scripts/safari_control.swift focus-text 'Email' --selector 'input, textarea, select'
swift scripts/safari_control.swift fill 'input[name=\"email\"]' 'user@example.com'
swift scripts/safari_control.swift click 'button[type=\"submit\"]'
swift scripts/safari_control.swift click-text 'Continue' --exact
swift scripts/safari_control.swift select-option 'select[name=\"country\"]' CN --by value
swift scripts/safari_control.swift check '#agree'
swift scripts/safari_control.swift uncheck '#agree'
swift scripts/safari_control.swift upload 'input[type=\"file\"]' ./avatar.png
swift scripts/safari_control.swift submit 'form'
swift scripts/safari_control.swift wait-selector 'form' --visible
swift scripts/safari_control.swift wait-text 'Success'
swift scripts/safari_control.swift wait-count '.result-item' 10 --op ge
swift scripts/safari_control.swift wait-title 'Success'
swift scripts/safari_control.swift wait-url '/success'
swift scripts/safari_control.swift wait-download 'report-*.csv'
swift scripts/safari_control.swift reload
swift scripts/safari_control.swift back
swift scripts/safari_control.swift forward
```

Rules:

- Prefer `exists`, `count`, `wait-*`, and `snapshot` to branch explicitly before acting.
- After an action, wait on a concrete condition instead of sleeping.
- Use `press-key` and `press-shortcut` only for page-level DOM handlers, not Safari chrome.
- `back`, `forward`, and `reload` return structured before/after state for change detection.

### 4. Native Safari UI

Use when the target is Safari chrome, not the page.

```bash
swift scripts/safari_control.swift list-menu-bar --json
swift scripts/safari_control.swift list-menu-items View --json
swift scripts/safari_control.swift click-menu View 'Reload Page'
swift scripts/safari_control.swift list-native-controls --json
swift scripts/safari_control.swift focus-native-control WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD --field identifier --exact
swift scripts/safari_control.swift set-native-value WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD 'https://example.com' --field identifier --exact
swift scripts/safari_control.swift press-native-control ReloadButton --field identifier --exact
swift scripts/safari_control.swift perform-native-action WEB_BROWSER_ADDRESS_AND_SEARCH_FIELD AXConfirm --field identifier --exact
swift scripts/safari_control.swift list-native-menu-items NewTabGroupButton --field identifier --exact --json
swift scripts/safari_control.swift click-native-menu-item NewTabGroupButton 'New Empty Tab Group' --field identifier --exact
swift scripts/safari_control.swift native-open-url https://example.com
swift scripts/safari_control.swift native-search 'open claw'
swift scripts/safari_control.swift native-search 'open claw' --confirm-mode both
swift scripts/safari_control.swift press-system-shortcut Cmd+L
swift scripts/safari_control.swift press-system-key Enter
```

Rules:

- The menu examples in this section assume Safari is running with an English UI.
- Start with `list-native-controls --json` before guessing identifiers.
- The native control JSON now includes `pressable`, `focusable`, `settable`, and `menuable` fields. Use those before choosing `press-native-control`, `focus-native-control`, `set-native-value`, or menu actions.
- `native-open-url` and `native-search` default to `--confirm-mode ax`. Use `enter` or `both` only if Safari's native confirm path is insufficient on that machine.
- Use `list-menu-items` or `list-native-menu-items` before clicking when Safari is localized.

## Common Task Templates

### Read the current page

```bash
swift scripts/safari_control.swift doctor
swift scripts/safari_control.swift check-js
swift scripts/safari_control.swift snapshot --interactive-only --limit 30
swift scripts/safari_control.swift get-text --mode article
```

### Fill a form in the real Safari session

```bash
swift scripts/safari_control.swift current --json
swift scripts/safari_control.swift snapshot --interactive-only --limit 30
swift scripts/safari_control.swift fill 'input[name=\"email\"]' 'user@example.com'
swift scripts/safari_control.swift click 'button[type=\"submit\"]'
swift scripts/safari_control.swift wait-url '/success'
```

### Operate Safari's own address bar or toolbar

```bash
swift scripts/safari_control.swift doctor
swift scripts/safari_control.swift list-native-controls --json
swift scripts/safari_control.swift native-open-url https://example.com
swift scripts/safari_control.swift press-native-control ReloadButton --field identifier --exact
```

## Export and Evidence

Use when you need durable files instead of transient terminal output.

```bash
swift scripts/safari_control.swift screenshot ./safari.png
swift scripts/safari_control.swift screenshot ./safari-foreground.png --mode foreground
swift scripts/safari_control.swift snapshot-with-screenshot ./safari.png --path ./snapshot.json
swift scripts/safari_control.swift save-html ./page.html
swift scripts/safari_control.swift save-text ./page.txt --mode article
swift scripts/safari_control.swift save-links ./links.json
swift scripts/safari_control.swift save-tables ./tables.json
swift scripts/safari_control.swift save-snapshot ./snapshot.json --interactive-only
swift scripts/safari_control.swift save-page-bundle ./page-bundle --interactive-only --zip
```

Rules:

- `auto` screenshot mode tries background capture first and falls back to foreground.
- `snapshot-with-screenshot` and `save-page-bundle` can read a background tab via `--window` / `--tab`, but the screenshot still comes from the visible Safari window.

## JavaScript Access Requirement

If `check-js` reports disabled, tell the user to enable:

1. Safari Settings
2. Advanced
3. Developer features if needed
4. Developer
5. `Allow JavaScript from Apple Events`

Then retry `check-js`.

If native Safari automation or script-driven workflows are blocked, also tell the user to verify Safari settings such as:

1. Allow Automation
2. Allow JavaScript in the Smart Search field
3. Allow JavaScript from Apple Events

Explain that these settings enable more Safari-control features, but they also grant more power to automation and scripted interactions. If the user declines, continue with only the features that remain available.

## Release and Distribution

These are maintenance commands, not the normal interaction path:

```bash
swift scripts/safari_control.swift build ./dist
swift scripts/safari_control.swift build ./dist --zip
swift scripts/safari_control.swift release
swift scripts/safari_control.swift release --name safari-control-demo --notes 'Internal preview build'
swift scripts/safari_control.swift version
```

Use these when you want a compiled binary, a release directory, zip artifacts, or build metadata with git and environment information.

## Limits

- Safari scripting is strong for session state, structured page inspection, waits, and standard DOM interactions.
- Safari scripting is not a robust replacement for full browser automation.
- Complex form workflows, native pickers, extension UIs, canvas apps, and pointer-heavy interactions should move to `desktop-control`.
- `upload` is for small files injected into `input[type=file]`, not large native picker workflows.
- `wait-download` is filesystem polling, not a Safari download API.
- `export-cookies` exposes `document.cookie`, not HttpOnly cookies or the full Safari cookie jar.
- `export-storage` only sees the current origin.
