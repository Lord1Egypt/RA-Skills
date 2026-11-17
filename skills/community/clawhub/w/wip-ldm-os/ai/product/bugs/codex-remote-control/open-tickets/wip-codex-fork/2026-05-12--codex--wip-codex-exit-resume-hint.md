---
title: "WIP Codex exit footer should say codex-wip resume"
status: open
priority: P1
owner: Cody
repo: openai-codex-private
created: 2026-05-12
surface: WIP Codex fork / TUI exit footer
---

# WIP Codex Exit Resume Hint

## Problem

When a session is running in WIP Codex, the exit footer still prints the stock resume command:

```text
To continue this session, run codex resume 019dfa1e-0c3d-7f01-86b9-9a22cd452bde
```

For WIP Codex dogfood, that hint is wrong. The user is intentionally running the patched `codex-wip` runtime because Remote Control co-presence requires the WIP Codex fork.

The footer should say:

```text
To continue this session, run codex-wip resume 019dfa1e-0c3d-7f01-86b9-9a22cd452bde
```

## Why This Matters

Remote Control live co-presence currently depends on WIP Codex, not stock Codex. A stock `codex resume` hint sends the user back into the wrong runtime after they exit a dogfood session.

That creates two problems:

- the resumed session may not expose the WIP App Server behavior Remote Control needs;
- the user has to remember to manually rewrite the hint to `codex-wip resume ...`.

The command footer should teach the correct recovery path for the binary that is actually running.

## Expected Behavior

When the running executable is `codex-wip`, the exit footer prints:

```text
codex-wip resume <thread-id>
```

When the running executable is stock `codex`, the exit footer still prints:

```text
codex resume <thread-id>
```

If the executable name cannot be detected, fallback to `codex`.

## Suggested Fix

Find the TUI exit footer code that emits:

```text
To continue this session, run codex resume ...
```

Replace the hardcoded `codex` command with the current executable name or a small helper that resolves the resume command.

Preferred behavior:

1. inspect `std::env::args().next()` or `std::env::current_exe()`;
2. take only the file name, not the full path;
3. allow `codex-wip` to flow through unchanged;
4. fallback to `codex` if detection is empty or invalid.

Do not special-case Remote Control. This is a WIP Codex fork TUI hint bug.

## Acceptance

- Exiting a `codex-wip` session prints `codex-wip resume <thread-id>`.
- Exiting stock `codex` still prints `codex resume <thread-id>`.
- Unit or snapshot coverage proves the footer chooses the command name from the active binary or helper input.
- No Remote Control daemon, relay, installer, or hosted MCP changes.
- No public repo direct edits. Fix lands through `openai-codex-private` and its normal fork/release path.

## Validation Evidence To Capture

After implementation, capture a local exit footer from WIP Codex showing:

```text
To continue this session, run codex-wip resume <thread-id>
```

Also run the focused TUI or snapshot tests that cover the footer formatting.
