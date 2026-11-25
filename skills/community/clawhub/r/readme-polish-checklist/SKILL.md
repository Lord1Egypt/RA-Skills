---
name: readme-polish-checklist
version: 1.0.0
description: Audit and fix a project README so a stranger can install and use the project in five minutes. Use before publishing a repo or after any major change.
---

# Readme Polish Checklist

## Overview

A README has one job: get a competent stranger from clone to working in minutes. This checklist tests it the way a stranger would — by following it literally.

## When to use

Before open-sourcing, after restructuring a project, or when users keep asking questions the README should answer.

## Workflow

1. **The 30-second test** — can a reader say what this is and who it is for after the first screen?
2. **The install test** — follow the install steps literally, in a clean environment if possible; every undocumented prerequisite is a bug
3. **The first-run test** — is there one copy-paste example that works end to end?
4. **The map** — does it explain the layout well enough that a contributor knows where a change belongs?
5. **The honesty pass** — remove claims about features that are partial, planned, or dead; mark experimental parts as experimental
6. **The exits** — license, how to report issues, and where the docs live

## Guardrails

- Never leave a badge, screenshot, or example that no longer matches the project
- Do not document aspirational features in the present tense
- If setup needs a secret or account, say exactly where to get it — never imply it is optional when it is required

## Output format

A fixed README plus a short list of what was wrong (missing prerequisite, stale claim, broken example) for the record.

---

Part of the Manteclaw free skill series. These workflow skills are free forever; Manteclaw's paid automation tools (runnable code, not just prompts) live at payhip.com/Manteclaw.
