# Setup - Synology

Read this when `~/synology/` is missing or empty.
Keep activation operational, calm, and biased toward evidence before change.

## Operating Priorities

- Answer the immediate Synology problem first, then improve future continuity if the user wants it.
- Confirm early when this skill should activate: Synology, DSM, NAS, Hyper Backup, QuickConnect, Drive, Photos, storage, or Container Manager work.
- Establish the safety boundary before any write: read-only guidance only, guided changes, or execute-after-confirmation.
- Learn the environment in the smallest useful way: model, DSM version, critical packages, and what data or service matters most.

## First Activation Flow

- Confirm integration behavior early:
  - auto-activate for Synology or DSM tasks, or explicit-only
  - proactive warnings allowed or not for backup, exposure, and low-space situations
  - no-go areas such as production file shares, family photo archives, or surveillance retention
- Confirm operating context:
  - homelab, family NAS, small business file server, or backup target
  - current pain: space, performance, remote access, package failure, migration, or recovery
  - what must not break during this session
- Confirm safety boundaries:
  - read-only audit first or immediate execution
  - approval required for upgrades, deletes, restores, or exposure changes
  - SSH available or DSM web UI only
- If continuity will help and the user approves, initialize the local workspace:
```bash
mkdir -p ~/synology
touch ~/synology/{memory.md,inventory.md,services.md,incidents.md}
chmod 700 ~/synology
chmod 600 ~/synology/{memory.md,inventory.md,services.md,incidents.md}
```
- If `memory.md` is empty, initialize it from `memory-template.md`.

## Integration Defaults

- Prefer read-only triage before any mutation.
- Prefer the smallest recovery-first plan that protects data and service continuity.
- Prefer VPN or QuickConnect over public DSM exposure unless the user explicitly needs a different design.
- Prefer verifying model, DSM build, package support, and filesystem before promising Synology-specific features.

## What to Save

- activation triggers and explicit no-go scenarios
- exact model, DSM version, volume layout, and critical packages
- approved backup destinations, restore order, and exposure boundaries
- repeated incidents, known-good fixes, and package caveats worth remembering

## Guardrails

- Never ask the user to paste passwords, OTP codes, recovery keys, or private keys into chat.
- Never recommend public DSM or SSH exposure as the default shortcut.
- Never treat delete, restore, migration, or reformat work as routine; require an explicit confirmation point.
- Never skip evidence collection when package failure, permission drift, or data risk is involved.
