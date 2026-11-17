---
title: "Targeted ldm install skips LDM OS self-update"
status: done
priority: P1
owner: Codex
repo: wip-ldm-os-private
created: 2026-05-11
---

# Targeted LDM Install Skips LDM OS Self-Update

## Problem

Dogfooding the Codex Remote Control install prompt exposed an installer version skew problem.

This machine had:

```text
LDM OS local: 0.4.85-alpha.3
LDM OS current alpha: 0.4.85-alpha.12
Codex Remote Control local: 0.0.2-alpha.20
Codex Remote Control current alpha: 0.0.2-alpha.21
```

Running:

```bash
ldm install --alpha --dry-run wip-codex-remote-control
```

correctly previewed the Remote Control package, but it did not show the newer skill destination path output that had already shipped in later LDM OS alpha builds. It also did not warn that the local LDM OS installer was behind.

## Root Cause

`ldm install` without a target enters the catalog install path and runs the LDM OS CLI self-update block before continuing.

`ldm install <target>` stays on the targeted install path and skips that self-update block entirely.

As a result, app installs can be driven by an outdated installer even when the user is already opting into the same release track with `--alpha` or `--beta`.

## Expected Behavior

All `ldm install` variants should run the LDM OS CLI preflight before installing a target.

For real installs:

```bash
ldm install --alpha wip-codex-remote-control
```

should update LDM OS first when a newer LDM OS alpha is available, then re-run the same app install with the updated CLI.

For dry runs:

```bash
ldm install --alpha --dry-run wip-codex-remote-control
```

must not update anything, but it should warn that a newer LDM OS installer exists and that the dry run is using the currently installed CLI.

## Product Rule

Targeted app installs should not silently run on stale installer behavior.

The install prompt remains the product path. The installer should make the prompt more trustworthy by disclosing installer version skew during dry runs and by self-updating before real targeted installs.

## Acceptance

- Targeted real installs run the same LDM OS self-update preflight as bare `ldm install`.
- Targeted dry runs do not self-update, but they warn when the local LDM OS CLI is behind the selected track.
- The selected track is respected: stable checks `@latest`, alpha checks `@alpha`, beta checks `@beta`.
- The install command re-runs the original user command after self-update.
- Regression tests cover targeted install self-update placement and dry-run warning behavior.
- Follow-up runtime coverage verifies the dry-run warning with a mocked npm lookup and a local target path containing spaces.
