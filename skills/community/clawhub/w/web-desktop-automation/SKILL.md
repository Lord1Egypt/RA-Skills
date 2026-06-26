---
name: web-desktop-automation
description: Use when the user wants browser automation, web scraping, form filling, clicking, or desktop GUI automation, including mixed workflows that move between web pages and local applications.
---

# Web + Desktop Automation

Use this skill when a task may involve:
- Opening or controlling websites
- Reading or extracting page content
- Filling forms, clicking buttons, logging in
- Downloading or uploading files
- Controlling desktop apps with mouse/keyboard
- Combining browser steps with local app steps

## Core rule

Prefer the simplest reliable path:
1. If the task can be done in the browser, use browser automation.
2. If the task needs local apps or OS-level interaction, use desktop automation.
3. If both are needed, split the job into clear phases and verify after each phase.

## Execution strategy

### 1) Classify the task
Decide which of these applies:
- Browser only
- Desktop only
- Mixed browser + desktop

### 2) Browser automation
Use browser automation for:
- Navigation
- Search
- Page reading
- Form filling
- Clicking controls
- File upload/download
- Logged-in web workflows

Prefer stable selectors and explicit waits. Avoid brittle coordinate-based clicking when browser selectors exist.

### 3) Desktop automation
Use desktop automation for:
- Native apps
- Window switching
- Copy/paste between apps
- File manager operations
- UI flows outside the browser

Prefer application/window-aware methods when available. Use image-based or coordinate-based control only when necessary.

### 4) Mixed workflows
Break the task into phases:
- Browser phase
- Desktop phase
- Browser phase again if needed

After each phase, verify the result before continuing.

## Recovery rules

If a step fails:
1. Re-check the current UI state
2. Re-locate the target element or window
3. Try a more stable selector or a different interaction method
4. If the task risks loss of data or irreversible action, stop and ask the user

## Best practices

- Prefer deterministic steps over guessing
- Avoid rapid blind retries
- Capture key state when tasks are long or fragile
- Keep flows small and modular
- Use scripts for repeated actions
- Use `scripts/browser_runner.py` for Playwright browser automation templates
- Use `scripts/desktop_runner.py` for PyAutoGUI desktop automation templates
- Use `scripts/mixed_orchestrator.py` for browser + desktop handoffs
- Put browser-specific patterns in `references/browser-workflows.md`
- Put desktop-specific patterns in `references/desktop-workflows.md`
- Put mixed-flow orchestration examples in `references/mixed-flows.md`
- Put dependency and installation notes in `references/dependencies.md`
- Put a realistic browser-download → desktop-edit → browser-upload flow in `references/mixed-example.md`
- See `requirements.txt` for a minimal install set
- Put dependency and installation notes in `references/dependencies.md`
- Put a realistic browser-download → desktop-edit → browser-upload flow in `references/mixed-example.md`
- Put dependency and installation notes in `references/dependencies.md`
