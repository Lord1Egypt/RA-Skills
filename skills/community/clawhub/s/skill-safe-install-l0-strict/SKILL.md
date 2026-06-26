---
name: skill-safe-install-l0-strict
description: Strict secure-install workflow for ClawHub/OpenClaw skills. Use when asked to install a skill safely, inspect skill permissions, review third-party skill risk, or run a pre-install security audit. Enforce full review + sandbox + explicit consent gates, with no author-based trust bypass.
---

# Skill Safe Install (L0 Strict)

Enforce a conservative, auditable install workflow.

## Purpose

Use this skill to reduce accidental or risky third-party skill installs:
- Force risk review before installation.
- Require sandbox verification before formal install.
- Require explicit user confirmation before sensitive actions.
- Avoid hidden trust escalation (no author-based bypass, no implicit allowBundled writes).

## Non-negotiable rules

1. Never skip steps.
2. Never auto-trust by author, popularity, or “official-looking” name.
3. Never modify persistent config (`openclaw.json`) without explicit user consent in the current conversation.
4. If risk cannot be evaluated, treat as high risk and pause.

## Workflow (Step 0 → Step 6)

### Step 0 — Confirm target

- Resolve exact skill slug and (if available) version.
- If input is ambiguous, ask for confirmation before install.

Suggested checks:
- `clawhub search <query>`
- Verify exact slug/version from results.

### Step 1 — Duplicate/state check

- Check whether the skill is already installed.
- Check current trust state (whether already in `skills.allowBundled`).

Suggested checks:
- `clawhub list`
- Read `~/.openclaw/openclaw.json` (or platform-equivalent config path)

### Step 2 — Mandatory security review (no whitelist bypass)

Run inspect and summarize at least:

1. Maintainer/source and recent update signal
2. Required secrets/credentials (API keys, OAuth, tokens)
3. Network/system access scope
4. Command execution or file-system mutation risk
5. Persistence behavior (config edits, auto-run, always-on behavior)

Suggested check:
- `clawhub inspect <skill>`

#### Risk rating rubric

- **LOW**: Text/process guidance only, no credentials, no system mutation.
- **MEDIUM**: Requires limited credentials or external API access with clear scope.
- **HIGH**: Broad command execution, config mutation, or multi-system OAuth.
- **CRITICAL**: Destructive capability, privilege escalation, stealth persistence, or unclear behavior.

#### Gate policy

- LOW / MEDIUM: Continue to sandbox.
- HIGH: Continue only after explicit confirmation.
- CRITICAL: Do not install by default; require explicit override and warn strongly.

### Step 3 — Sandbox install (isolated workdir)

Install in a temporary isolated directory first.

- Use isolated workdir (do not install to primary skill directory yet).
- Confirm install result and basic behavior.
- If sandbox fails, stop.

Example pattern:
- `clawhub --workdir <temp_dir> --dir skills install <skill>`

### Step 4 — User confirmation checkpoint

Before formal install, present:
- Chosen skill slug/version
- Risk rating + top risks
- Sandbox result
- Exact next action

Proceed only after explicit “yes/install/继续”.

### Step 5 — Formal install

Run formal install only after Step 4 consent.

Example:
- `clawhub install <skill>`

If install fails, stop and report error + rollback advice.

### Step 6 — Optional trust persistence (`allowBundled`)

Default is **do not write** trust list.

Only perform this step when user explicitly asks to persist trust.

Required safeguards:
1. Backup config with timestamp.
2. Show exactly what key will change (`skills.allowBundled`).
3. Append skill slug only if absent (idempotent).
4. Confirm backup path and rollback command.

Do not use hidden or implicit trust writes.

## Output format (required)

- `[Step 0/6] Target: ...`
- `[Step 1/6] State: ...`
- `[Step 2/6] Review: risk=LOW|MEDIUM|HIGH|CRITICAL; findings=...`
- `[Step 3/6] Sandbox: pass|fail`
- `[Step 4/6] Consent: pending|approved|denied`
- `[Step 5/6] Install: pass|fail`
- `[Step 6/6] Trust write: skipped|pending|written`

## Refusal conditions

Stop and ask for confirmation/override when any condition is met:
- Skill identity is ambiguous.
- Inspect output is unavailable or incomplete.
- Risk is HIGH/CRITICAL and user has not explicitly approved.
- Requested config mutation lacks explicit consent.
