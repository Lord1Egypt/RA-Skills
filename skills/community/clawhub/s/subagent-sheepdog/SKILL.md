---
name: subagent-sheepdog
description: Launch verification and watchdog discipline for delegated, backgrounded, browser-driven, and long-running tasks. Prevents false "running" claims, clarifies failed_to_start vs failed_after_work_started, and treats heartbeat as a watchdog rather than the main progress loop.
metadata:
  {
    "openclaw": {
      "emoji": "🛎️"
    }
  }
---

# Subagent Sheepdog

Use this skill whenever work is:
- delegated to a subagent or child session
- launched as a background process
- driven through browser automation
- long-running enough that progress reporting matters
- vulnerable to "ghost delegation" (claimed launch, but no real work underway)

Do **not** use this skill for tiny direct tasks where startup verification would add noise.

## Purpose

This skill prevents a common failure mode in agent systems:

> an agent launches something, gets back a session/process/tab handle, and falsely reports that work is running even though startup already failed or never truly began.

It enforces clear state transitions, truthful communication, and watchdog-style recovery behavior.

---

## Core Rule

**Do not claim work is running until startup is verified.**

A session id, process id, browser tab, or tool handle alone is **not** proof that work actually started.

Treat the period after launch and before verification as:
- `launching_unverified`

Only after verification may the task become:
- `running`

If startup fails before real execution begins, classify it as:
- `failed_to_start`

If work began and failed later, classify it as:
- `failed_after_work_started`

---

## Task States

Use these states consistently:

- `launching_unverified`
- `running`
- `delayed`
- `failed_to_start`
- `failed_after_work_started`
- `completed`

### State meanings

#### `launching_unverified`
Launch was attempted, but startup health is not yet confirmed.

#### `running`
Startup was verified and meaningful execution is underway.

#### `delayed`
Work is still running, but later than expected.

#### `failed_to_start`
The launch path failed before real work began.

#### `failed_after_work_started`
Real work began, then later failed.

#### `completed`
Task finished successfully with real output or result.

---

## Required Launch Sequence

Whenever this skill applies, follow this sequence:

1. Announce launch briefly
2. Attempt launch
3. Enter `launching_unverified`
4. Verify startup health
5. If verified, mark `running`
6. If not verified, mark `failed_to_start`
7. Retry only if the fix is obvious and mechanical
8. Re-verify before claiming success

---

## Verification Rules By Work Type

### A. Subagent / child-session launches

Do not claim success unless you verify at least:
- the spawn call succeeded
- the child session actually exists
- the child is active or otherwise accepted
- the runtime did not reject the launch immediately

Examples of `failed_to_start` here:
- invalid spawn parameters
- unsupported runtime combination
- missing thread binding
- rejected session mode
- missing required agent/runtime field

### B. Background exec / process launches

Do not claim success unless you verify at least:
- the process exists
- the process did not immediately exit
- the working directory is valid
- the executable exists
- no immediate fatal startup error is present in the initial result/log

Examples of `failed_to_start` here:
- `command not found`
- `no such file or directory`
- permission denied at startup
- invalid working directory
- immediate non-zero exit
- rejected runtime host/sandbox mismatch

### C. Browser-driven work

Do not claim browser work is underway unless you verify at least the relevant part of the path:
- browser/session exists
- target page actually loaded
- expected page or UI element is present
- no login wall, interstitial, or error page blocked progress

Examples of `failed_to_start` here:
- browser opened but target page failed to load
- redirected to login before task could begin
- error page prevented interaction
- required UI element never appeared

If the page loaded and meaningful interaction began before failure, use `failed_after_work_started` instead.

---

## Heartbeat Behavior

Heartbeat is a **watchdog**, not the main progress loop.

Use heartbeat to:
- surface overdue tasks
- detect stalled work
- detect ghost delegation
- catch startup failures that were not properly reported

Do **not** use heartbeat to:
- aggressively poll every active task
- replace direct milestone updates
- substitute for proper launch verification

### Ghost delegation

A ghost delegation is when work was described as launched, but:
- no real worker exists
- startup failed immediately
- browser setup never reached a usable page
- the agent implied progress without verified execution

Heartbeat should surface that clearly instead of returning a normal all-clear.

---

## Communication Rules

Prefer concise truth over reassuring fiction.

### Good launch-phase language
- “Launching now. Verifying startup.”
- “Launch attempted; checking whether the worker actually started.”
- “Startup is being verified before I call this running.”

### Good failure language
- “Startup failed. No work started. Cause: {reason}.”
- “The launch was rejected before execution began. No work started.”
- “The browser path failed before meaningful interaction began. No work started.”

### Good running language
- “Verified: work is actually running now.”
- “Startup is confirmed. First milestone ETA ~{time}.”

### Good delayed language
- “Work is still running, but slower than expected.”
- “The task is active but behind the original ETA.”

### Good late failure language
- “Work did start, but failed later. Cause: {reason}.”

### Bad language
- “Started successfully” before verification
- “Working on it” when only a handle exists
- “It’s analyzing now” before startup health is confirmed
- any ETA that implies verified execution before verification happened

---

## Retry Policy

Retry only when the fix is obvious and mechanical.

Examples:
- correcting a known launch parameter
- switching to the proper thread-bound mode
- fixing a wrong working directory
- switching to an available executable/runtime

If retrying:
1. report the original failure
2. say you are retrying
3. return to `launching_unverified`
4. verify again before claiming success

Do not loop forever.

---

## Best-Next-Step Rule

When blocked, recommend **one best next step** instead of dumping a large menu unless the user explicitly asks for options.

Good:
- “Best next step: switch to one-shot run mode because persistent thread binding is unavailable here.”

Less good:
- giving 4–6 loosely ranked possibilities without guidance

---

## Generic Example

### Bad
“Background worker launched and running now.”

(But only a session id exists; no verification was done.)

### Good
“Launch attempted; verifying startup.”

Then either:
- “Verified: the worker is actually running now.”

or:
- “Startup failed. No work started. Cause: missing thread binding for session mode.”

---

## Browser Example

### Bad
“Opened the browser and I’m working on the site now.”

(But the browser only opened a login wall.)

### Good
“Browser launched, but the target workflow did not start. The page redirected to login before the task could begin. No work started.”

---

## Completion Standard

A task should only be described as completed when there is evidence of a real result, such as:
- output artifacts
- a verified state change
- a final summary tied to actual work performed

---

## Summary

This skill teaches a simple discipline:

- launch carefully
- verify startup
- report truthfully
- use heartbeat as backup
- distinguish failed launch from failed work

The result is better trust, clearer status reporting, and fewer ghost tasks.
