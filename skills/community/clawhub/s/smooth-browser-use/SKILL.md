---
name: smooth-browser-use
description: Use when operating browser-based workflows that need smooth, human-like navigation, reliable text entry, real paste/input events, form validation, translators, AI detectors, Moodle editors, rich text fields, React/Vue/SPA forms, or any web page where front-end state must update correctly. Also use when a browser page is blank, stuck, stale, desynchronized, or should be refreshed back to a clean state before retrying.
---

# Smooth Browser Use

## Overview

Use browser pages the way a careful human would: wait for the real UI, click visible controls, paste through the page, and verify the page's own state before continuing.

Accessibility `set_value` can make text visible without firing the page's `paste`, `input`, `change`, validation, translation, word-count, or enable-button logic. Treat it as a narrow tool, not the default for web app text entry.

When a browser page is stuck, stale, or desynchronized, refresh back to a clean initial state before retrying.

## Smooth Workflow

1. Load the page and wait for the real app UI, not just the address bar or a blank shell.
2. Use `get_app_state` before interacting after navigation, reloads, user interruptions, or failed clicks.
3. Prefer visible controls and keyboard operations over direct accessibility value injection.
4. After each meaningful action, verify the page reacted before moving on.
5. If the page state looks wrong, refresh early instead of compounding bad state.

## State Checks

Do not trust visible text alone. Trust the page's own state indicators:

- Word or character counters update.
- Translation output changes.
- Analyze, detect, submit, or continue buttons become enabled.
- The page shows a completed result instead of placeholder text.
- Error banners disappear after retry or refresh.

If visible text and page indicators disagree, treat the page as desynchronized.

## Text Entry

1. Put the intended text on the system clipboard when the text is long.
2. Click the actual visible input area, text area, editor, or page-provided Paste button.
3. Use keyboard paste (`Cmd+V` on macOS) or the page's Paste button so the site receives a real paste event.
4. If replacing existing text, use the page's clear/delete control first when available. Otherwise focus the field, use `Cmd+A`, then paste.
5. Verify the page reacted using its own indicators. Do not proceed only because the accessibility tree shows the value.
6. If the page still does not react, click out and back in, press a harmless navigation key, or re-paste through the page's Paste button.
7. If the page remains inconsistent, refresh and retry from a clean state.

Use `set_value` only for low-risk browser chrome fields such as the address bar, or for simple native fields where no page-side logic is needed. Avoid it for translators, detectors, rich editors, SPAs, and assignment text boxes.

## Page Recovery

When a page is blank, stuck loading, shows a generic error, or has stale state:

1. Refresh the page once and wait for the initial UI to return.
2. If the page keeps stale or broken state, refresh again or open the same URL in a new tab/window.
3. After refresh, do not assume previous text is valid. Clear the field or start from the page's initial state.
4. Re-enter text using the Text Entry workflow.
5. Re-check the page's own indicators before continuing.

For error screens with a visible retry control, try the page's retry button once. If it does not restore a consistent state, refresh the page.

## Failure Signals

Stop and recover when any of these happen:

- Text is visible but the counter says `0 Words`, `0 Characters`, or "enter text to scan."
- A detector/analyzer button stays disabled after text appears.
- A translator input contains text but no translation starts.
- The page says "Something went wrong" after text insertion.
- The accessibility value changed but the on-screen app state did not.
- The page remains blank after navigation.

## Browser Tool Notes

- Call `get_app_state` before interacting after user interruption, page reload, or a failed click.
- Prefer visible clicking plus keyboard operations for web content.
- Use clipboard plus `Cmd+V` for long text to avoid partial typing and to trigger paste handlers.
- After every significant input, read the screen or accessibility tree again and verify the web app reacted.

## Examples
For Baidu Translate:

1. Load or refresh the translator page.
2. Click the source text area.
3. Paste using `Cmd+V`.
4. Confirm the character count changes and translated output starts updating.
5. If text appears but no translation starts, clear the field, refresh, and paste again through the real UI.
