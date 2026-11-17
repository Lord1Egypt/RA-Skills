---
title: "ldm doctor issue counter does not match the number of visible warnings"
status: open
priority: P2
owner: unassigned
reviewer: Installer CC Partner
repo: wip-ldm-os-private
created: 2026-05-14
---

## What it does

`ldm doctor`'s "N issue(s) found" footer matches the number of visible warnings in the output. The user can see every issue the counter is counting.

## What it fixes

Today (alpha.30): `ldm doctor` printed "10 issue(s) found" but only ONE warning line was visible in the output (LaunchAgent plist drift). The other 9 issues are invisible to the user. Either the counter is wrong or 9 warnings are being suppressed in the renderer. Either way, the user has no way to know what doctor thinks is broken. This is a trust failure: the footer claims there are problems the user can't act on.

## How to dogfood

1. Run `ldm doctor` on any LDM OS install.
2. Count the visible `!` or warning-formatted lines in the output.
3. The footer count must match. Today it does not.

## Problem

Either the renderer is dropping warnings, the counter is double-counting, or there's a separate "internal issue" category that gets tallied but not shown. Diagnose first, then fix to one of:

1. Show all counted issues (the renderer surfaces every issue the counter sees).
2. Stop counting hidden ones (the counter only tallies what the renderer will show).

The fix direction is the implementer's call after diagnosis, but the end state must be: counter matches visible output.

## Acceptance

- `ldm doctor` output on any install state has a footer count matching the number of warning-formatted lines above it.
- Regression test simulates an install state with multiple issues; asserts the footer count equals the rendered-warning count.
- Dogfood: Parker runs `ldm doctor` on his machine and the footer matches the visible warnings (whatever the count is).

## Out of scope

- Fixing any of the underlying issues themselves; this ticket is about reporting accuracy.
- Adding new issue categories or remediation hints. Scope is reconcile-count-with-visible only.

## Related

- `2026-05-14--cc-mini--ldm-doctor-fix-crash-startsWith.md` (sibling, same 2026-05-13/14 dogfood, same `ldm doctor` surface).
