# VAIBot Guard Policy (MVP)

This is the *baseline* policy for VAIBot Guardrails + Audit Trail.

## Goals

- Deny high-risk actions by default.
- Require an explicit **run plan** for any execution.
- Produce an append-only, tamper-evident audit trail.

## Enforcement model (MVP)

- All command execution must go through `vaibot-guard-exec` wrapper.
- Wrapper calls the local guard service (`vaibot-guard-service`) for a decision.
- Guard service returns one of: `allow | deny | approve`.

## Default deny categories (MVP)

The following are denied outright (non-exhaustive):

- **Persistence / system mutation**: `systemctl`, `service`, `launchctl`, `crontab`, editing system unit files
- **Credential access / key material**: touching `~/.ssh`, `id_rsa`, cloud credential dirs
- **Package installs**: `apt`, `apt-get`, `dnf`, `yum`, `brew`, `pacman`

## Approval-required categories (MVP)

These require explicit approval (returned as `approve`):

- **Network egress** primitives: `curl`, `wget`
- **Filesystem mutation** in sensitive paths (outside workspace)

## Run plan requirements

A run plan must include:

- `intent` (string)
- `expectedOutputs` (string[])

Optional but recommended:

- `risk` (low|medium|high)
- `rollback`
- `commands` (structured list)

## Audit trail

- Each exec request logs:
  - timestamp, session id, command, args
  - decision + reason
  - hash-chained `prevHash`

