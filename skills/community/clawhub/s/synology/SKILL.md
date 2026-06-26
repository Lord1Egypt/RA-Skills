---
name: Synology
slug: synology
version: 1.0.0
homepage: https://clawic.com/skills/synology
description: Plan, harden, and recover Synology NAS and DSM setups with storage design, backup discipline, remote access, and Container Manager workflows.
changelog: Initial release with DSM-first planning, safer storage and backup decisions, remote access guardrails, and recovery playbooks.
metadata: {"clawdbot":{"emoji":"S","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/synology/"]}}
---

## When to Use

Use this skill when the user needs Synology-specific execution, not generic NAS or Linux advice. It covers DSM planning, storage layout, shared folders, remote access, Hyper Backup, Snapshot Replication, Synology Drive, package health, Container Manager, migrations, upgrades, and incident recovery.

This skill should activate whenever the real question is "what should be changed on this Synology box, in what order, and how do we avoid losing data or exposing DSM."

## Architecture

This skill works statelessly for one-off Synology questions. If the user wants continuity across sessions, memory lives in `~/synology/`. If `~/synology/` does not exist, run `setup.md`, explain planned local notes in plain language, and ask for confirmation before creating files. See `memory-template.md` for structure.

```text
~/synology/
|- memory.md        # Model, DSM version, workloads, and guardrails
|- inventory.md     # Volumes, shares, packages, and exposure notes
|- services.md      # Container Manager, Drive, Photos, backup, and app notes
`- incidents.md     # Failures, recoveries, and postmortems worth reusing
```

## Quick Reference

Load only the smallest file that matches the task.

| Topic | File | Use it for |
|-------|------|------------|
| Setup flow and saved defaults | `setup.md` | Activate safely and decide whether continuity is useful |
| Memory schema and status values | `memory-template.md` | Create durable notes without storing secrets |
| Volumes, Btrfs, SHR, and shared folder decisions | `storage-and-shares.md` | Capacity, snapshots, permissions, and migration planning |
| Hyper Backup, snapshots, rsync, and restore order | `backup-and-recovery.md` | Real backup strategy and recovery sequencing |
| QuickConnect, VPN, reverse proxy, and exposure guardrails | `remote-access-and-networking.md` | Remote access and network change safety |
| Package health, Synology Drive, Photos, and Container Manager | `packages-and-containers.md` | App selection, package triage, and container caveats |
| Incident triage and evidence collection | `troubleshooting.md` | Fast diagnosis before risky changes |

## Requirements

- No credentials required for planning, review, or architecture work
- Live DSM changes may require admin access to the web UI and optional SSH access
- Confirm whether the target NAS is production, homelab, or backup-only before changing anything
- Require explicit confirmation before deletions, package removals, share permission rewrites, exposure changes, restore operations, or storage migrations

## Data Storage

Store only context that improves later Synology work:

- exact model, DSM version, and which packages matter
- filesystem and volume facts that change recommendations
- approved backup destinations, restore priorities, and exposure boundaries
- recurring failures, confirmed fixes, and package-specific caveats

Do not store passwords, QuickConnect credentials, OTP codes, serial numbers, or copied support bundles with secrets.

## Core Rules

### 1. Identify the Box Before Giving Synology Advice
- Lock the exact model, DSM version, volume layout, filesystem, and installed packages before promising features or commands.
- Synology guidance changes materially with model family, DSM version, and whether the workload depends on Btrfs-only features.
- If that context is missing, ask for it before acting like every NAS behaves the same.

### 2. Separate Read-Only Diagnosis From Writes
- Start with inventory: storage health, free space, package status, backup state, and remote exposure.
- State whether the next step is read-only, additive, mutating, or destructive.
- Never jump straight from "it looks slow" to deleting data, changing shares, or reinstalling packages.

### 3. Treat SHR and RAID as Availability, Not Backup
- Disk redundancy protects against some hardware failures, not ransomware, accidental deletion, bad sync, or site loss.
- Every serious plan needs restore-tested backup layers such as Hyper Backup, Snapshot Replication, rsync, or an external copy.
- If restore testing is missing, say the backup posture is incomplete.

### 4. Internet Exposure Is Opt-In
- Prefer VPN or QuickConnect for remote admin convenience over raw DSM port forwarding.
- Reverse proxy and public access are explicit design choices that need MFA, update discipline, and blast-radius awareness.
- Never recommend exposing DSM, SSH, or package dashboards to the public internet by default.

### 5. Verify Feature Gates Before Recommending Synology Features
- Snapshot Replication, immutable backup patterns, and some data-protection workflows depend on model support, filesystem, package availability, and licensing.
- Container Manager guidance depends on compatible models and package availability on the target DSM build.
- When a recommendation depends on support status, verify it before presenting it as available.

### 6. Protect Production State Before Upgrades or Rebuilds
- Before DSM upgrades, package reinstalls, share moves, or container rewrites, confirm the recovery path and the configuration that must survive.
- Export or record key settings, confirm backup freshness, and define rollback before touching live services.
- If the user cannot explain how to undo the change, the plan is not ready.

### 7. End With an Execution Record
- Finish non-trivial work with a short record: target NAS, read-only findings, chosen action, validation steps, rollback path, and open risks.
- Save only that durable summary under `~/synology/` if the user wants continuity.
- This keeps later Synology work grounded in facts instead of re-discovering the same box every time.

## Safety Checklist

Before high-impact Synology changes:

- confirm the exact NAS, volume, share, and package being changed
- state whether the step is read-only, additive, mutating, or destructive
- confirm backup freshness and whether restore has ever been tested
- capture current screenshots, package versions, or config exports before upgrades or reinstalls
- ask for explicit confirmation before delete, downgrade, restore, remote exposure, or major permission changes

## Common Traps

- Treating Synology like generic Ubuntu with disks attached -> wrong service assumptions and risky cleanup advice
- Confusing SHR or RAID with backup -> false confidence until deletion, corruption, or ransomware happens
- Promising snapshots or replication without confirming filesystem and package support -> recovery plan fails when it matters
- Opening DSM or SSH to the internet "just for now" -> turns convenience into attack surface
- Recommending package reinstalls before collecting evidence -> destroys the only clues needed to fix the issue safely
- Blaming performance on CPU alone -> full volumes, indexing, broken thumbnails, parity checks, or bad remote sync often matter more
- Restoring everything at once after an incident -> increases downtime and can overwrite evidence or good data

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://www.synology.com | Page requests and product references only unless the user asks for account or package actions | Verify current DSM, packages, compatibility, and official guidance |
| https://kb.synology.com | Page requests and query text only | Confirm current product behavior and troubleshooting steps |
| https://account.synology.com | Browser session data only when the user explicitly performs account-linked tasks | Synology account, package, and service operations approved by the user |
| https://quickconnect.to | QuickConnect identifiers and connection metadata only when the user explicitly tests remote access | Remote access routing and connectivity checks |

No other data should be sent externally unless the user explicitly approves third-party backup, VPN, DNS, or monitoring services.

## Security & Privacy

Data that may leave your machine:
- documentation lookups against Synology-owned sites
- account and session traffic only when the user explicitly performs Synology account or remote-access actions
- QuickConnect identifiers and connection metadata only when remote access is actively configured or tested

Data that stays local:
- model, package, backup, and recovery notes in `~/synology/`
- screenshots, exports, or runbooks the user chooses to keep locally

This skill does NOT:
- ask the user to paste DSM passwords, OTP codes, or private keys into chat
- claim SHR, RAID, or sync are backups when they are not
- expose DSM or SSH publicly by default
- promise package, filesystem, or model features without verification when support matters

## Trust

This skill depends on Synology-owned documentation, account surfaces, and remote-access services when the user explicitly uses them.
Only install and use it if you trust Synology with the approved operations and related metadata.

## Scope

This skill ONLY:
- plans and executes Synology DSM and NAS workflows with explicit safety gates
- covers storage, backup, remote access, package health, and Container Manager decisions
- keeps lightweight local memory in `~/synology/` when the user wants continuity
- emphasizes restore-first thinking for incidents and migrations

This skill NEVER:
- pretend all Synology models and DSM builds support the same features
- treat redundancy as backup
- run destructive storage or exposure changes without explicit confirmation
- replace specialized camera automation, enterprise SAN design, or off-platform Kubernetes guidance

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `backups` - Backup strategy, retention, and restore planning beyond one vendor
- `self-host` - Self-hosted service decisions around ownership, risk, and maintenance
- `docker` - Container architecture once the Synology host and storage plan are stable
- `home-server` - Home lab and household service tradeoffs once the NAS becomes a platform
- `wireguard` - Private remote access when QuickConnect is not the right fit

## Feedback

- If useful: `clawhub star synology`
- Stay updated: `clawhub sync`
