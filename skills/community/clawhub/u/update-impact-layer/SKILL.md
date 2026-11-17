---
name: "openclaw-update"
description: "Before or after OpenClaw updates, track local overwrite risks and bounded integration checks around the native updater."
homepage: "https://github.com/clawSean/update-impact-layer"
---

# Clawkeeper

Use this as a thin local-operations layer around OpenClaw's native update system. The installed updater owns target selection, admission, backup integration, activation, restart coordination, reports, repair, recovery, and cleanup. Do not recreate those mechanisms here.

## Use current native authority

1. Read `openclaw update --help`, `openclaw update status --json`, and the installed update docs before planning. Treat their current commands, warnings, report, and `nextAction` as newer than this skill.
2. On the Gateway hosting the active agent, use the native Gateway update action, Control UI, or `/update` when available. Otherwise use `openclaw update` or `openclaw update wizard` from the installation owner's terminal. Never replace the native path with a custom supervisor, raw package-manager install, or hand-written rollback controller.
3. Require the installation owner's explicit approval before an update, repair, restart, downgrade, plugin mutation, live config write, or recovery cleanup. Read-only status, dry-run, docs, and local-ledger maintenance do not authorize mutation.

## Keep one small local impact ledger

Use the environment's existing operations/project record when one exists. Otherwise create one only when the owner wants durable update tracking. Read [references/local-impact-layer.md](references/local-impact-layer.md) for the entry shape and inclusion rules.

Record only facts the native updater cannot know:

- a live non-native patch or packaged-file override that an update can replace;
- a temporary migration or compatibility obligation tied to a current deployment;
- a quiet external integration whose real behavior needs one bounded smoke test after relevant updates.

Exclude native configuration, ordinary plugins handled by native convergence, inactive experiments, upstream PRs not deployed locally, generic health checks, and old incidents. Remove an entry when its deviation is retired, upstreamed, or fully owned by native OpenClaw.

Recording an impact never starts an update.

## Prepare a rollout

1. Run `openclaw update --dry-run --json` and read the native status/report. Use the target, warnings, ownership, capability changes, and recommended next action from that output; do not generate a parallel universal checklist.
2. Select only local-ledger entries relevant to the proposed target or changed component. For each selected entry, identify its canonical owner and the smallest pre-update and post-update proof. Stop if a live deviation lacks a recoverable source or a required compatibility gate fails.
3. For a significant update, use the current native backup command and verify the archive, such as `openclaw backup create --verify` when supported. A verified backup is a recovery point, not permission to ignore a failed native preflight.
4. Keep any local run note short: link the native run/report, list selected local impacts, record the verified recovery point, and name the bounded checks. Do not copy the native report into another document.

## Run and verify

1. Let the native update workflow own activation, service handoff, restart, Doctor, plugin convergence, and recovery. Follow its current prompts and `nextAction`; invoke repair or mutating Doctor modes only when the native workflow calls for them and approval covers them.
2. Start verification from the native completion report and `openclaw update status --json`. Confirm the intended version/build is serving and the Gateway is ready before local integration checks.
3. Run only the selected local proofs. Verify the behavior that matters—not merely that a process or plugin loaded—and reuse each integration's existing health check or project test.
4. Record the result beside each selected ledger entry. Update its tested baseline, retain a concrete unresolved obligation, or remove it if native OpenClaw now owns the behavior.
5. Treat recovery cleanup as a separate destructive decision because it can retire rollback material. Preview it first and require explicit acceptance of that loss.

## Failure handling

Read the native report before acting. Report the failed native gate, current serving version, recovery point, affected local impacts, and native next action. Do not improvise a package-only downgrade after target code may have migrated durable state; use the installed schema-aware repair, recovery, or verified-backup guidance.
