---
name: simple-verifier
description: Fast lightweight verification pass for recent work. Use proactively after medium or large tasks, coding passes, app changes, or long replies when you need a quick check for missed asks, partial completion, stale status, or unsupported 'done' claims without a long audit.
---

# Simple Verifier

## Overview

Run a fast verification pass on recently completed work. Keep it short, strict, and evidence-based. Do not redo the work. Do not add new content. Only check whether the ask was actually satisfied.

## What to verify

### 1. Original ask
Restate the user request briefly in checklist form.

### 2. Quick completeness check
For each requested part, ask:
- was it actually done?
- was it only discussed instead of completed?
- were promised files, commands, or outputs really produced?

### 3. Quick unsupported-claim check
Flag anything claimed as complete without clear support from:
- tool output
- code changes
- created files
- observed runtime behavior

### 4. Quick stale-status check
If the agent says something is blocked, active, or done, check whether the latest evidence still supports that claim.

## Output format

Use this compact structure:

### Request
- short checklist of what was asked

### Complete
- items clearly completed

### Missing / partial
- items not fully done

### Unsupported / stale
- claims not supported by evidence or no longer true

### Verdict
- ✅ complete
- ⚠️ gaps
- ❓ unverified

## Rules

- Keep it concise.
- Prefer 'not verified' over guessing.
- Do not invent missing context.
- Do not redo the task.
- If the request is too large to verify confidently, say that and list what remains uncertain.
