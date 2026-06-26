# vmctl-ops

`vmctl-ops` is a post-install operational skill for Hermes Agent.

It tells the agent exactly what to do **after `vmctl` is already installed**:
- run mandatory health checks,
- execute a safe smoke VM lifecycle test,
- clean up test artifacts correctly,
- recover state drift if needed,
- report concise operator-ready status.

---

## Why this skill exists

Without a dedicated post-install playbook, agents tend to:
- skip prerequisite checks,
- improvise risky commands,
- leave stale test VMs/state behind,
- misuse `purge` by VM name instead of deleted tombstone name.

This skill standardizes a deterministic, safe flow for immediate validation of a `vmctl` environment.

---

## Scope

### In scope
- `vmctl mode`
- `vmctl preflight`
- `vmctl doctor`
- `vmctl list --all`
- smoke `create` / `status`
- cleanup `delete --force` + `purge <deleted_name>`
- `recover --dry-run` / `recover --apply`

### Out of scope
- Installing `vmctl` itself (bootstrap)
- Host account/role management on ESXi
- Production provisioning with non-test VM names

If `vmctl` is missing, the skill requires the agent to stop and redirect operator to install docs.

---

## Safety model

- **No privilege escalation guidance** in skill commands.
- Uses plain `vmctl ...` command style.
- Enforces test-only naming (`vmctl-test-*`).
- Requires cleanup unless operator explicitly asks to keep test VM.

---

## Typical workflow

1. Health gate (`mode`, `preflight`, `doctor`, `list --all`)
2. Smoke create/status on a test VM
3. Delete and purge test resources
4. Optional recover pass for residual drift
5. Structured short status report

---

## Prerequisites

- `vmctl` already installed and callable in PATH
- vmctl config/secrets already deployed
- ESXi/helper credentials already configured
- Access to `/opt/hermes-vmctl` state directory (for tombstone lookup)

---

## Installation source (for operators)

- Repository: https://github.com/bashrusakh/vmctl
- Latest release page: https://github.com/bashrusakh/vmctl/releases/latest

---

## Install this skill in Hermes

Recommended (pinned to a reviewed commit):

```bash
hermes skills install https://raw.githubusercontent.com/bashrusakh/vmctl/13f3833098d1e79c6fad26e85f9efe3c38fa59e3/skills/devops/vmctl-ops/SKILL.md
```

Alternative (pin to a release tag after review):

```bash
hermes skills install https://raw.githubusercontent.com/bashrusakh/vmctl/v0.1.1/skills/devops/vmctl-ops/SKILL.md
```

Avoid `--yes` unless the exact URL content has already been reviewed and approved.

---

## Use in session

- Load explicitly: `/skill vmctl-ops`
- Or ask naturally: "run post-install smoke for vmctl"

The skill’s execution contract and exact commands are defined in `SKILL.md`.

---

## Files

- `SKILL.md` — executable skill instructions for Hermes Agent
- `README.md` — human-facing publication overview (this file)
