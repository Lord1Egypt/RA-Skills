---
name: vmctl-ops
description: Use when vmctl is already installed and the agent must immediately run safe post-install checks and first lifecycle actions without guessing.
version: 1.0.0
author: Leonid + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vmctl, esxi, post-install, validation, operations]
    related_skills: [esxi-standalone-vmctl-delivery]
    required_commands: [vmctl]
    required_paths:
      - /opt/hermes-vmctl/config/vmctl.yaml
      - /opt/hermes-vmctl/state
      - /opt/hermes-vmctl/state/deleted
    credential_expectations:
      - ESXi/helper credentials are preconfigured by the installer.
      - vmctl runtime secrets are available to the execution user.
    minimum_permissions:
      - vmctl mode/preflight/doctor/list for diagnostics
      - vmctl create/status for test VM lifecycle validation
      - vmctl delete/purge/recover for state cleanup/reconciliation
---

# vmctl Post-Install Operations

## Overview
This skill defines what the agent should do **right after vmctl installation** on the Hermes host.

Goal: quickly verify that vmctl is operational, run a safe smoke cycle, clean artifacts, and report status in operator-friendly form.

Installation source (performed by operator):
- Repository: https://github.com/bashrusakh/vmctl
- Latest release page: https://github.com/bashrusakh/vmctl/releases/latest

Important:
- This is a **post-install** skill.
- If vmctl is not installed, the agent must stop and ask operator to install from the repo/release link above.
- Do not attempt bootstrap installation. If `vmctl` is missing, stop and redirect operator to repo/release install docs.

## When to Use
- vmctl was just installed or reinstalled.
- ESXi/helper credentials are already configured.
- Operator asks: "run a test", "check after install", "why is it not working".

Do **not** use for:
- bootstrap installation itself;
- modifying ESXi host accounts/roles;
- production VM provisioning with non-test names.

## Default Execution Mode
- Run as plain `vmctl` CLI (no privilege escalation or forced user switching in this skill).
- Workdir: `/opt/hermes-vmctl`
- Do not guess values; use config/secrets already deployed by installer.

## Runtime Requirements
- Required binary: `vmctl` must be available in PATH.
- Required config path: `/opt/hermes-vmctl/config/vmctl.yaml`.
- Required state paths: `/opt/hermes-vmctl/state` and `/opt/hermes-vmctl/state/deleted`.
- Required credential context: ESXi/helper credentials are already configured by installer.

## Minimum Permissions and Credential Scope
- Minimum needed operations: `mode`, `preflight`, `doctor`, `list`, `create`, `status`, `delete`, `purge`, `recover`.
- This skill must not be used for account/role management or bootstrap installation.
- Expected credential scope should be limited to vmctl helper workflow and test VM lifecycle operations.
- Prefer test-only VM names (`vmctl-test-*`) and avoid touching non-test resources unless operator explicitly asks for it.

## Quick Reference

```bash
# baseline checks
vmctl mode
vmctl preflight
vmctl doctor
vmctl list --all

# recover state drift
vmctl recover --dry-run
vmctl recover --apply
```

## Procedure

## Phase 1 — Mandatory health gate
Run in order:

```bash
vmctl mode
vmctl preflight
vmctl doctor
vmctl list --all
```

Rules:
1. If `preflight` or `doctor` is red -> stop and report blocker.
2. If `list --all` shows pending/failed from old runs, recover/cleanup before new create-tests.

## Phase 2 — Safe smoke create test
Use a test name only:
- `vmctl-test-<purpose>-<timestamp>`

Minimal smoke command:

```bash
vmctl create \
  --name vmctl-test-smoke-<timestamp> \
  --template alma10 \
  --cpu 2 \
  --ram-mb 4096 \
  --disk-gb 40 \
  --user hermes \
  --ssh-key-file /tmp/vmctl_test_key.pub
```

Then:

```bash
vmctl status <name>
```

Success criteria:
- state is `ready`
- IPv4 exists
- no exception from create/status

## Phase 3 — Cleanup policy
Delete+purge test VM after smoke run unless operator asked to keep it.

```bash
vmctl delete <name> --force
```

Important: `purge` uses **deleted tombstone name**, not original VM name.

```bash
# discover tombstone
python3 - <<'PY'
import glob, os
vm='<name>'
paths=glob.glob('/opt/hermes-vmctl/state/deleted/*.json')
c=[p for p in paths if vm in os.path.basename(p)]
if c:
    c.sort(key=os.path.getmtime, reverse=True)
    print(os.path.basename(c[0])[:-5])
PY

vmctl purge <deleted_name>
```

## Recovery flow (if state drift exists)
If ESXi has managed VM but state is missing:

```bash
vmctl recover --dry-run
vmctl recover --apply
```

Then run delete/purge again.

## Operator Output Format
Report concise facts:
- preflight: pass/fail
- doctor: pass/fail
- create: pass/fail + vm name
- cleanup: deleted + purged / blocked
- residual check: `recover --dry-run` actions count

## Common Pitfalls
1. Running commands with hardcoded elevated wrappers from old docs.
2. Purging by original VM name -> `deleted tombstone not found`.
3. Reusing stale test names -> clone/file already exists errors.
4. Treating orphan datastore folders as vmctl-managed state.

## Verification Checklist
- [ ] `mode` confirms helper-only effective mode.
- [ ] `preflight` is green.
- [ ] `doctor` is green.
- [ ] smoke `create` reaches `ready`.
- [ ] test VM removed by `delete --force`.
- [ ] tombstone purged by deleted-name.
- [ ] `recover --dry-run` has no unexpected actions.
