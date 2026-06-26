---
name: ssh-executor
description: Execute commands on remote hosts over SSH using SSH aliases, ssh config, tmux sessions, and private keys. Use when the user asks to SSH into a host, inspect Linux or server state remotely, run one-off remote shell commands, reuse an SSH alias, or drive a tmux-based remote workflow. Prefer for key-based SSH access and remote diagnostics. Do not use for password storage, private-key exfiltration, silent host-key bypass, or destructive changes without explicit confirmation.
metadata:
  { "openclaw": { "os": ["linux", "darwin"], "requires": { "bins": ["ssh", "bash", "python3"] } } }
---

# SSH Executor

Use this skill to run remote commands safely over SSH.

## Provenance

- **Author:** Community skill (see [clawhub.ai](https://clawhub.ai) for the original listing)
- **Homepage:** This package — verify checksums from a trusted distribution source
- **Integrity:** The release zip includes a `.sha256` checksum for the compiled `.skill` file. Verify before installation.
- **Review:** All bundled source is plain-text and visible. Review `scripts/ssh-run.sh` and `SKILL.md` before first use.

## Quick start

1. Gather the host alias, username, port, and key path from the user's instructions or local SSH config.
2. Prefer SSH aliases from `~/.ssh/config` instead of raw IPs when available.
3. **Validate the target host with the user** before running any command, especially if the host was inferred or listed from config rather than explicitly requested.
4. Default to read-only commands first.
5. Require explicit user confirmation before destructive or state-changing commands.
6. Use the bundled `scripts/ssh-run.sh` helper for execution.
7. Return stdout, stderr, exit code, and resolved SSH metadata clearly.

## Safety rules

- **Validate the host with the user.** Before connecting, confirm the exact hostname or alias with the user, especially if it was inferred from context or discovered via `--list-aliases`. Do not assume a host is the right target.
- **Prefer read-only commands first.** Default to inspection before any state change.
- **Explicit confirmation is required for any mutation** — every command that modifies state (files, services, packages, data, containers, network, firewall, or anything using `sudo`) needs the user to see and approve the exact command **in full** before the agent passes `--confirm-dangerous`.
- **The dangerous-command heuristic is not exhaustive.** The pattern check may miss novel or obfuscated destructive commands. When in doubt, treat the command as dangerous and ask for confirmation.
- **Prefer least-privilege SSH accounts.** If the remote host has a dedicated read-only or low-privilege account, use that for inspection. Only escalate for clearly authorized mutation.
- Prefer key-based auth. Do not ask the user to paste passwords into chat unless they explicitly insist and understand the risk.
- Do not reveal or copy private-key contents into chat, logs, or memory files.
- Do not disable host-key checking silently.
- Prefer the host's existing ssh config when possible.
- Treat these as destructive unless the user clearly asked for them: `rm`, `mv`, `chmod`, `chown`, `systemctl restart|stop|disable`, `reboot`, `shutdown`, package installs/upgrades, `docker compose down`, schema changes, file writes, or anything using `sudo`.
- For destructive work, confirm the exact command before running it, then pass `--confirm-dangerous`.
- If a command can be split into inspect first and mutate later, do the inspect step first.

## Workflow

### 1. Resolve target

Collect or infer:
- host or SSH alias
- user, if not already encoded in the alias
- port, if non-default
- key path, if needed
- timeout
- desired host-key policy
- optional ssh config path

If a known SSH alias already exists, prefer it over a raw host/IP.

Only inspect `~/.ssh/config` when the user already uses SSH aliases or asks you to resolve them.

To inspect available aliases from the default ssh config:

```bash
scripts/ssh-run.sh --list-aliases
```

To inspect aliases from a custom config file:

```bash
scripts/ssh-run.sh --list-aliases --config ~/.ssh/config
```

### 2. Decide risk level

- **Read-only**: `hostname`, `uname -a`, `uptime`, `df -h`, `journalctl -n 100`, `docker ps`
- **Mutating**: package management, service restarts, file edits, deletes, deploys

Read-only commands can usually run immediately.
Mutating commands need explicit confirmation.

### 3. Run command

Use:

```bash
scripts/ssh-run.sh --host <host-or-alias> [--user <user>] [--port <port>] [--key <path>] [--timeout <seconds>] [--config <ssh-config>] [--host-key-checking accept-new|yes] -- '<command>'
```

If the command is mutating and the user explicitly approved it:

```bash
scripts/ssh-run.sh --host <host-or-alias> --confirm-dangerous -- '<command>'
```

Examples:

```bash
scripts/ssh-run.sh --host web-1 -- 'hostname && uptime'
```

```bash
scripts/ssh-run.sh --host 192.168.1.50 --user root --port 2222 --key ~/.ssh/id_ed25519 --timeout 15 --host-key-checking yes -- 'df -h && free -h'
```

```bash
scripts/ssh-run.sh --host prod-app --confirm-dangerous -- 'sudo systemctl restart myapp'
```

### 4. Report result

Summarize briefly:
- whether the SSH connection succeeded
- exit code
- resolved host/user/port when useful
- key findings from stdout/stderr
- next safe step

## Install and test

This skill lives under the workspace `skills/` directory so OpenClaw can discover it in future sessions.

Suggested smoke tests for the bundled helper:

```bash
bash -n scripts/ssh-run.sh
scripts/ssh-run.sh --help
scripts/ssh-run.sh --list-aliases
```

## Resources

- `scripts/ssh-run.sh`: key-based SSH wrapper with structured JSON output, alias support, and dangerous-command confirmation
- `references/safety.md`: extra guidance for safe remote execution
