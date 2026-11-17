---
title: "ldm status and install dry-run should share update detection"
status: open
priority: P3
owner: Installer Cody
repo: wip-ldm-os-private
created: 2026-05-12
---

# `ldm status` and `ldm install --dry-run` should not drift

## Problem

Dogfood on 2026-05-12 showed two different installed-state answers on the same machine:

- `ldm status` budget-skipped all update checks.
- `ldm install --dry-run` resolved the available updates in seconds.

The bounded-concurrency fix makes `ldm status` useful again, but the code paths are still separate. `cmdStatus()` has its own npm probe runner, while `cmdInstallCatalog()` builds its dry-run update plan through install-specific logic, different timeouts, and track handling.

That split is fragile. The two commands answer the same user question during the install prompt: "what do I have and what is new?" If they disagree, the agent starts rebuilding state manually or explaining two conflicting tables.

## Expected behavior

When run back-to-back against the same registry state and the same selected track, these commands should report the same available update set:

```bash
ldm status
ldm install --dry-run
```

They do not need identical formatting. They do need to agree on which installed components have updates.

## Proposed fix

Extract a shared update-detection helper used by both `cmdStatus()` and `cmdInstallCatalog()`.

The shared helper should own:

- registry entry normalization;
- npm package name resolution;
- dist-tag selection for stable, beta, and alpha;
- timeout and concurrency behavior;
- skipped or unavailable probe reporting.

`cmdStatus()` can keep its status-oriented summary formatting. `cmdInstallCatalog()` can keep its install-plan and dry-run formatting. The update list underneath should come from one function.

## Acceptance

- `ldm status` and `ldm install --dry-run` produce the same available update list when run back-to-back against the same registry state.
- Track selection stays correct for stable/latest, beta, and alpha.
- Unpublished or private extensions are reported consistently instead of silently disappearing from one command.
- Regression test stages a fixture registry, runs both commands, and asserts the available-update package set matches.
- No real install happens during the test.

## Recommendation

No release required by itself if this stays as a structural follow-up. If it changes runtime update detection, cut alpha and dogfood the install prompt again.

## Related

- `2026-05-12--cc-mini--ldm-status-bounded-concurrency-for-npm-probes.md`
- `2026-05-12--cc-mini--ldm-status-per-check-elapsed-time.md`
