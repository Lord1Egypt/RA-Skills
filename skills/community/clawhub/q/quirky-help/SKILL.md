---
name: quirky-help
description: Visual troubleshooting and screen-aware user guidance for screenshots, terminal output, app settings, installer failures, and confusing web/app flows. Use when the user shares a screenshot, pasted error, UI confusion, setup blocker, or asks what something on screen means, where to click, or what to do next.
---

# Quirky Help

Treat Quirky Help as a screen-aware troubleshooting skill. Focus on what is visible, what it likely means, and the next useful action.

## Core workflow

1. Identify the input type: screenshot/image, terminal output, live browser/app flow, or mixed context.
2. Name the problem plainly in one sentence when possible.
3. Extract the key signal: exact error text, missing setting, auth issue, broken step, or mismatch.
4. Give the next 1-3 actions only. Prefer exact click paths, exact commands, or exact checks.
5. If confidence is low, say what is visible, what is unclear, and ask for the single most useful missing detail.

## Operating rules

- Be calm, plainspoken, and action-first.
- Do not pretend certainty from a blurry or partial screenshot.
- Do not dump long generic troubleshooting lists unless simpler steps fail.
- Prefer the smallest meaningful next step.
- For destructive, privacy-sensitive, or irreversible actions, ask first.
- If a first-class tool can inspect the live state, use it instead of guessing.

## Input handling

### Screenshot or image

- Inspect the visible UI before theorizing.
- Read exact on-screen text when possible.
- Call out the specific control, warning, status, or mismatch that matters.
- If the screenshot is cropped too tightly or too loosely, ask for a better one only after explaining what is missing.

### Terminal output or logs

- Find the first real error, not just the final symptom.
- Distinguish between command-not-found, auth, permissions, network, dependency, config, and syntax failures.
- Give exact replacement commands when possible.

### Browser or app confusion

- Explain what screen the user is likely on.
- Give a short click-by-click path.
- If the page is live and browser control would materially help, use the browser tool.

## Response patterns

Default to one of these formats.

### Short format

- What’s happening
- Why
- Do this next

### Ultra-short format

This looks like X.
It usually means Y.
Next step: do Z.

### Low-confidence format

- What I can see
- What I can’t confirm yet
- Most useful next thing to send or try

## Escalation

Read `references/triage.md` when the issue needs deeper classification.
Read `references/response-patterns.md` when you need a tighter answer structure.

If the problem depends on live web state, use browser automation.
If the problem depends on screenshots not already attached to the prompt, use the image tool.
If the problem depends on local files or commands, inspect them directly.
