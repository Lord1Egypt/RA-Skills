---
name: Safari Browser Control
slug: safari
version: 1.0.0
homepage: https://clawic.com/skills/safari
description: Control Safari on macOS with AppleScript, safaridriver, screenshots, tab navigation, and real-browser read, click, and type workflows.
changelog: Initial release with AppleScript control patterns, safaridriver setup, screenshot loops, and Safari permission checks.
metadata: {"clawdbot":{"emoji":"🧭","requires":{"bins":["osascript","safaridriver","screencapture"],"config":["~/safari/"]},"os":["darwin"],"configPaths":["~/safari/"]}}
---

## When to Use

User needs the agent to control the real Safari browser on macOS, not a generic headless browser. Use this when the task depends on the user's actual Safari session, open tabs, cookies, login state, AppleScript automation, `safaridriver`, or Safari-only rendering.

Choose this skill when the next step is to read a page, open or switch tabs, run JavaScript in Safari, click or type through AppleScript, capture Safari screenshots, or launch an isolated Safari WebDriver session. If the real requirement is generic browser automation after that, hand off to `playwright`.

## Architecture

Memory lives in `~/safari/`. If `~/safari/` does not exist, run `setup.md`. See `memory-template.md` for structure and starter files.

```text
~/safari/
|-- memory.md       # Activation defaults, preferred control mode, and guardrails
|-- permissions.md  # Automation, Develop menu, and screenshot preflight state
|-- sessions.md     # Real-session vs WebDriver session notes and target tabs
|-- snippets.md     # Known-good AppleScript and shell patterns worth reusing
|-- recipes.md      # High-value task recipes such as read, click, fill, capture
`-- incidents.md    # Permission failures, blocked JS, and repeat breakages
```

## Quick Reference

Load only the smallest file needed for the current blocker.

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Permissions and preflight checks | `preflight-and-permissions.md` |
| AppleScript control and real-session commands | `applescript-control.md` |
| `safaridriver`, WebDriver, and BiDi usage | `webdriver-and-bidi.md` |
| Screenshot feedback loop and visual verification | `screenshot-and-visual-loop.md` |
| Failure patterns and recovery order | `troubleshooting.md` |

## Requirements

- macOS with Safari installed and `osascript`, `safaridriver`, and `screencapture` available.
- Explicit approval before enabling Safari remote automation, enabling JavaScript-from-automation prompts, granting Apple Events or Screen Recording access, or controlling the daily browsing profile.
- Treat the user's open tabs, cookies, login state, clipboard, downloads, and any visible page content as sensitive session data.

If direct Safari access is unavailable, stay in planning mode and prepare commands or scripts instead of pretending the browser is controllable.

## Control Modes

This skill covers two distinct control surfaces:

- **AppleScript mode** for the user's real Safari session: current tabs, real cookies, logged-in pages, JavaScript execution, and screenshots of what the user actually has open.
- **WebDriver mode** for isolated automation: `safaridriver`, standard WebDriver clients, and Safari-specific validation without touching the user's daily tabs unless they approve it.

Do not blur the two. Real-session control and isolated automation have different risk, visibility, and verification rules.

## Data Storage

Keep only durable Safari operating context in `~/safari/`:
- approved control mode defaults and whether daily-session control is allowed
- permission state for Apple Events, Screen Recording, Develop menu, and remote automation
- known-good snippets, task recipes, and incidents worth reusing
- recurring no-go actions such as "never control banking tabs" or "never type blindly"

## Core Rules

### 1. Choose the Control Surface Before Sending Any Command
- Decide first whether the task needs the real Safari session or an isolated WebDriver session.
- Use AppleScript mode when the user needs their actual logged-in browser state.
- Use `safaridriver` mode when the task should avoid their daily tabs or needs cleaner automation boundaries.

### 2. Run a Preflight Before Touching the Browser
- Verify Safari is installed, the expected permissions are present, and the target window or session exists.
- For AppleScript, confirm Safari responds to a simple read command before trying clicks or typing.
- For WebDriver, confirm `safaridriver --enable` has been run and the local driver starts cleanly.

### 3. Read and Verify Before You Click or Type
- Start with title, URL, DOM text, or screenshot checks so the target surface is explicit.
- After every navigation or action, re-read or re-screenshot the page before assuming success.
- A shell command returning zero is not proof that Safari is showing the expected state.

### 4. Treat the Real Safari Session as High-Trust State
- The real Safari window may contain logged-in accounts, active drafts, and sensitive tabs.
- Ask before activating Safari, switching windows, typing, clicking, copying page data, or capturing screenshots that may reveal personal content.
- Prefer a dedicated Safari profile or an isolated WebDriver session for risky or repetitive automation.

### 5. Use AppleScript for Real State, WebDriver for Clean State
- `osascript` can inspect and control the user's live Safari windows and tabs.
- `safaridriver` gives a cleaner automation boundary but does not automatically inherit the user's existing Safari tab state.
- Do not promise real-session continuity from WebDriver mode unless you verified that exact setup.

### 6. Never Type Blindly Into Safari
- Before keystrokes, focus the correct tab and confirm the intended element or page state.
- Prefer DOM-based input with verification over raw keystrokes when possible.
- If Safari focus is uncertain, stop and recover state before sending more input.

### 7. Route Adjacent Problems to the Right Skill
- Use this skill for Safari control, Safari session inspection, and Safari-specific WebDriver setup.
- Hand off deep AppleScript design to `applescript`, macOS permission debugging to `macos`, generic browser scripting to `playwright`, and credential or WebAuthn logic to `passkey`.

## Safari Traps

- Treating `safaridriver` as if it automatically controls the tabs the user already has open -> session assumptions go wrong fast.
- Typing through `System Events` without verifying Safari focus -> input lands in the wrong field or wrong app.
- Clicking by guessed selectors without reading the page first -> automation hits the wrong element or stale DOM.
- Capturing screenshots without warning when the real session contains sensitive tabs -> privacy failure.
- Enabling automation on the daily profile and leaving it there -> unnecessary exposure and flaky state.
- Assuming a command succeeded because Safari opened -> always re-read or re-screenshot the target page.

## External Endpoints

This skill makes no external requests on its own.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | None | N/A |

No data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- None from this skill itself

**Data that stays local:**
- optional Safari control notes in `~/safari/`
- permission state, approved recipes, and incident notes approved by the user

**This skill does NOT:**
- send undeclared network requests
- recommend bypassing paywalls, anti-fraud controls, or account protections
- claim browser control without verifying permissions and target state
- store passwords, raw history exports, or full browsing archives in its own memory files

## Scope

This skill ONLY:
- helps control Safari safely through AppleScript, screenshots, and `safaridriver`
- structures real-session and isolated-session workflows into reversible steps
- keeps durable notes for approved modes, snippets, and recurring incidents

This skill NEVER:
- act as a generic search-engine skill
- claim live browser state it cannot verify
- store secrets, credentials, or full browsing history in its own memory files
- modify its own skill files

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `applescript` - Write safer AppleScript when Safari control moves beyond known-good snippets.
- `macos` - Handle Apple Events, Screen Recording, app focus, and native system diagnostics on Mac.
- `playwright` - Automate browser flows once the task no longer depends on the user's real Safari session.
- `ios` - Bridge Safari-adjacent workflows when the target moves to iPhone or iPad.
- `passkey` - Diagnose Safari sign-in and WebAuthn behavior without guessing at credential rules.

## Feedback

- If useful: `clawhub star safari`
- Stay updated: `clawhub sync`
