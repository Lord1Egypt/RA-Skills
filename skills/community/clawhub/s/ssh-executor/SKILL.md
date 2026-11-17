---
name: ssh-executor
description: Execute commands on remote hosts over SSH with structured discovery, pluggable credential backends, and safety guardrails. Supports SSH key-based and password-based auth with multiple credential sources (vault, env vars, direct files). Includes 6-step discovery protocol and standardized JSON output. Host-key verification is strict by default. Cross-platform: works on Hermes Agent, OpenClaw, Claude Code, Codex, and any LLM environment with bash + python3.
metadata:
  platforms: ["hermes", "openclaw", "claude-code", "codex", "generic"]
  os: ["linux", "darwin"]
  requires: { bins: ["bash", "python3", "base64"], optional_bins: ["ssh", "ssh-agent", "ssh-add", "ssh-keygen", "sshpass"] }
---

# SSH Executor

Execute remote commands over SSH securely. Platform-agnostic — configure once, use anywhere.

## Scope

| Use for | Don't use for |
|---------|---------------|
| Connecting to Linux servers via alias, IP, user, port | Storing/displaying credentials in chat or logs |
| Inspection commands (read-only) | Running destructive commands without user confirmation |
| Maintenance with explicit `--confirm-dangerous` | Bypassing host-key verification (strict by default) |
| Any credential backend: vault, env vars, key files, password prompts | Exposing private key contents anywhere |

### Credential Sources (Tiered)

The skill works with **any** credential source. Configure what you have — no mandatory vault dependency.

| Tier | Source | How | Example |
|------|--------|-----|---------|
| **1. Vault** | Any vault that outputs to stdout | `--vault-key <name>` + backend script | Bitwarden CLI, 1Password CLI, vault-resolver, HashiCorp Vault |
| **2. Env vars** | Environment variables | `SSH_PASS`, `SSH_SUDO_PASS`, `SSH_KEY` | CI/CD pipelines, containerized agents |
| **3. Direct** | Key files, interactive prompts | `--key <path>`, `--ssh-pass-ask`, `--sudo-pass-ask` | Local development, one-off access |

The default vault backend is **vault-resolver** (Hermes-native, Vaultwarden API). To use another vault:

```bash
# 1Password CLI
export VAULT_RESOLVER_BIN="op"

# Bitwarden CLI
export VAULT_RESOLVER_BIN="bw"

# Custom script (must accept JSON on stdin, output JSON on stdout)
export VAULT_RESOLVER_BIN="/path/to/your/vault-wrapper"
```

See `references/vault-backends.md` for setup guides for each platform.

## Platform Setup

### Hermes Agent / OpenClaw (native)
```bash
# vault-resolver is auto-detected at /opt/data/bin/vault-resolver
# Store a key:
ssh-keys.sh store my-server ~/.ssh/id_rsa
# Use:
ssh-run.sh --host my-server --vault-key my-server -- 'uptime'
```

### Claude Code / Codex / Generic LLM
```bash
# No vault — use env vars or key files:
export SSH_KEY="$(cat ~/.ssh/id_rsa)"
ssh-run.sh --host my-server --user ubuntu --key ~/.ssh/id_rsa -- 'uptime'

# Or with password (requires SSH_EXECUTOR_ALLOW_DANGEROUS=1):
SSH_EXECUTOR_ALLOW_DANGEROUS=1 SSH_PASS="<your-password>" ssh-run.sh --host my-server --user ubuntu -- 'uptime'
```

### CI/CD / GitHub Actions
```bash
ssh-run.sh --host ${{ secrets.SSH_HOST }} \
           --user ${{ secrets.SSH_USER }} \
           --key <(echo "${{ secrets.SSH_KEY }}") \
           -- 'deploy.sh'
```

## Server Discovery

The remote server inventory (aliases, IPs, ports, users) lives in the **wiki** at `/opt/data/wiki/entities/remote-servers.md`. When the user mentions an alias not in `~/.ssh/config`, check this file first — it contains the full table of all known servers.

**Warning:** The actual `~/.ssh/config` may differ from what the wiki documents. In particular, the `User` directive is often **not** present for individual hosts. Always pass `--user <user>` explicitly in that case. The wiki contains the per-host user table.

Do not use this skill to:
- Store or transmit passwords in chat, logs, or memory files
- Expose private key contents in chat, logs, or memory
- Bypass host key verification without explicit user permission (default is strict)
- Run destructive commands without user confirmation
- Use `restore-to-file` unnecessarily — prefer ssh-agent

## Recommended Flow

1. Discover the target: alias, hostname, port, user — from SSH config or the request.
2. Validate the host with the user before connecting.
3. Decide risk level: read-only (safe) or mutating (requires confirmation).
4. Execute with `scripts/ssh-run.sh` and the correct parameters.
5. Report the result: success, exit code, stdout/stderr, next steps.

## stdout/stderr Contract

`ssh-run.sh` and its backends follow a strict output contract:

| Stream | Content | Format |
|--------|---------|--------|
| **stdout** | Pure JSON with command result | `{"success": bool, "exit_code": int, "stdout": "...", "stderr": "...", ...}` |
| **stderr** | Status messages (vault, warnings, progress) | Free text |

**Rule:** stdout is **always** parseable by `json.load()`. It never contains vault messages, ssh warnings, or any non-JSON text. This enables pipelines like:

```bash
result=$(ssh-run.sh --host <your-host> --user <user> --vault-key id-rsa -- 'df -h' 2>/dev/null)
echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['stdout'])"
```

## Security Rules

- **Validate host with user.** Confirm hostname/IP before any connection, especially if inferred from config.
- **Read-only first.** Start with inspection commands. Commands that modify state (sudo, systemctl, rm, apt, docker, firewall, etc.) require `--confirm-dangerous` and explicit user approval.
- **Mandatory re-confirmation for sudo.** Every `--sudo` execution requires explicit user approval, even if the password is already in the vault. This includes consecutive commands on the same host — never automate sudo.
- **Dangerous command heuristic is not exhaustive.** Always treat unknown or chained commands with caution.
- **Private keys never go to chat, logs, stdout, or memory files.** The `ssh-run.sh` JSON output intentionally omits key paths.
- **Vault credentials are resolved in RAM and passed to SSH/sudo only via stdin pipe.** The vault binary path is validated before execution.
- **Key disk exposure is minimized but not eliminated in all paths.** Without `ssh-agent`, `ssh-keys.sh restore` writes decrypted key material to a temp file (`/tmp/ssh-vault-*` or `/dev/shm/ssh-vault-*`) that is cleaned up by trap handlers. `restore-to-file` writes to a caller-specified path. Interruption by `kill -9` prevents cleanup — prefer `ssh-agent` to avoid disk exposure entirely.
- **Sensitive log access requires approval.** Reading `/var/log/auth.log`, `/var/log/secure`, or similar security logs exposes usernames, source IPs, and authentication patterns — treat as privileged telemetry. Always get explicit user approval and consider redacting PII (usernames, IPs) before sharing results.
- **Prefer `/dev/shm` over `/tmp` for temporary key material.** `/dev/shm` is RAM-backed tmpfs and survives reboots less often than `/tmp`. The scripts use `/dev/shm` when available and fall back to a secure temp directory otherwise. Multiplexing sockets (not key material) in `/tmp` are acceptable.

## MCP Permissions Declaration

This skill requires the following capabilities. Deploy with least-privilege toolset restrictions:

| Capability | Scope | Justification |
|-----------|-------|---------------|
| `terminal` | Bash scripts (`ssh-run.sh`, `ssh-keys.sh`, `ssh-run-native.sh`) | SSH command execution |
| `file` | Read `~/.ssh/config`, wiki server inventory, temp files | Configuration resolution |
| `env` | `SSH_PASS`, `SSH_SUDO_PASS`, `SSH_AUTH_SOCK` | Password/env-var auth paths |
| `web` | vault-resolver API calls (localhost only) | Credential resolution |

**Restricted:** Never grant `delegation` or `cronjob` to this skill — SSH execution must always be directly supervised by the user.

### Dangerous Operations Gate

Password-based SSH authentication and `sudo` are gated behind the `SSH_EXECUTOR_ALLOW_DANGEROUS` environment variable. Without it set to `1`, these operations return exit code 98:

```bash
# Enable dangerous operations (password auth + sudo):
export SSH_EXECUTOR_ALLOW_DANGEROUS=1
ssh-run.sh --host <host> --sudo --sudo-pass-vault <name> -- 'systemctl restart nginx'

# Without the env var → exit 98 "requires SSH_EXECUTOR_ALLOW_DANGEROUS=1"
```

This gate ensures the operator explicitly acknowledges the elevated risk at the environment level before any password or sudo operation is possible. Key-based auth (without sudo) does not require this gate.

## Structured Discovery Protocol

For new server investigations or infrastructure mapping, follow this discovery order — each step answers one question before moving on:

| Step | Question | Typical commands |
|------|----------|------------------|
| 1. Identity | Who is this host? What role? | `hostname`, `cat /etc/os-release`, `uname -a` |
| 2. Runtime | What is running? | `docker ps`, `systemctl list-units --type=service`, `ps aux`, `docker compose ps` |
| 3. Origin | Where did it come from? Which repo/tag/volumes? | `docker inspect --format '{{.Config.Image}}' <container>`, `docker inspect --format '{{.Mounts}}' <container>`, `docker compose config` |
| 4. Network | What is listening? | `ss -tlnp`, `docker port <container>`, `iptables -L -n` (with approval) |
| 5. Data | Where is persistent data? | `df -h`, `lsblk`, `docker volume ls`, `mount` |
| 6. Register | What do I know for sure vs. what am I inferring? | Structured report (see below) |

**Narrow commands:** each command should answer **one** question. Avoid `docker inspect` without a field filter — prefer `--format '{{.Config.Image}}'` or `'{{.Mounts}}'`. Avoid `find /` or `grep -r /`.

If at any step you encounter a path with `.env`, `keystore/`, `secrets/`, or credential files — **do not read the contents**, only register its existence.

## Expected Output

When finishing a discovery or mapping, report in this format:

```
Host: <hostname>
Role: <role description>

Runtime:
  - <container/service 1> → image:tag, compose: <path>
  - <container/service 2> → image:tag, compose: <path>

Network:
  - <port>: <protocol> → <description>

Data:
  - <mount>: <host path>

Confirmed facts:
  - ...

Inference / Assumptions:
  - ... (mark explicitly)

Open questions:
  - ...

Required approvals:
  - ...
```

This separates **evidence** from **interpretation** — any downstream operator can reproduce the facts and question the conclusions.

## Backend behavior with `--vault-key`

**As of 2026-07-22:** `--vault-key` **no longer forces the Python/Paramiko backend**. The native backend (`ssh-run-native.sh`) handles vault keys via `ssh-keys.sh restore` → `ssh-agent`. The Python/Paramiko backend (`ssh-client.py`) is used only as a fallback when `openssh-client` is unavailable.

## Connection Multiplexing (ControlMaster)

To avoid audit log spam (`auth.log`) — where multiple SSH connections in a few seconds look like a brute-force attack — the native backend now uses **OpenSSH connection multiplexing**:

```bash
# First command: opens connection + authenticates (1 entry in auth.log)
ssh-run.sh --host <your-host> -- 'hostname'

# Subsequent commands (within 180s): reuse socket (ZERO new entries)
ssh-run.sh --host <your-host> -- 'df -h'
ssh-run.sh --host <your-host> -- 'docker ps'
```

**Parameters:**
- `--control-persist <seconds>` — how long the master socket stays alive after the last command (default: **180s**)
- `--control-close` — close the master socket immediately after the command (for clean audit session termination)

**Socket path:** `/tmp/ssh-mux-%r@%h:%p` (e.g. `/tmp/ssh-mux-root@10.0.0.5:22`)

**Important:** Multiplexing only works when all commands to the same host use the **same** user and port. If alternating between `root@host` and `user@host`, each combination gets its own socket.

Active multiplexing verification: `references/multiplexing-verification.md`.

## Sudo Password Resolution

For commands requiring `sudo` without configuring `NOPASSWD` on the server, the skill supports three password sources, resolved in priority order:

### 1. Vault (most secure)
```bash
# Store once:
vault-resolver write sudo-<your-host> sudo_password="my-password"

# Use:
SSH_EXECUTOR_ALLOW_DANGEROUS=1 ssh-run.sh --host <your-host> --user <user> --vault-key <key-name> \
           --sudo --sudo-pass-vault <your-host> --confirm-dangerous \
           -- 'systemctl restart nginx'
```

### 2. Environment variable (for pipelines)
```bash
SSH_EXECUTOR_ALLOW_DANGEROUS=1 SSH_SUDO_PASS="my-password" ssh-run.sh --host <your-host> --user <user> --vault-key <key-name> \
    --sudo --confirm-dangerous -- 'systemctl restart nginx'
```

### 3. Interactive prompt via LLM
```bash
# LLM calls with --sudo-pass-ask, script fails with instructions
SSH_EXECUTOR_ALLOW_DANGEROUS=1 ssh-run.sh --host <your-host> --user <user> --vault-key <key-name> \
    --sudo --sudo-pass-ask --confirm-dangerous -- 'systemctl restart nginx'
# → exit 97: "Ask the user for the password, then retry with SSH_SUDO_PASS"

# LLM asks user, then retries:
SSH_EXECUTOR_ALLOW_DANGEROUS=1 SSH_SUDO_PASS="<user-provided>" ssh-run.sh ... --sudo --confirm-dangerous -- 'systemctl restart nginx'
```

**Priority:** vault → `SSH_SUDO_PASS` env var → `--sudo-pass-ask`

**Security:**
- Password resolved in RAM, never on disk
- Sent via `echo '<pass>' | sudo -S -p ''` — password never appears on the command line (`ps`)
- `-p ''` suppresses sudo password prompt (avoids stderr pollution)
- Original command is base64-encoded to avoid quote escaping issues
- `--sudo` automatically enables `--confirm-dangerous` (no extra flag needed)
- ⚠️ **Every `--sudo` execution must be re-confirmed by the user.** Even with the password in the vault, the LLM must never run sudo commands without explicit approval on each call. This includes consecutive commands on the same host — each `--sudo` requires fresh confirmation.

**Vault format:** item `sudo-<name>` with field `sudo_password` (plain text, not base64).

## SSH Password Authentication

**⚠️ Security tradeoff:** Password-based SSH is weaker than key-based auth. Use only when keys are not available and the user has explicitly approved. Prefer key-based auth (`--vault-key` or `--key`) whenever possible.

When no SSH key is available, the skill supports password-based authentication via `sshpass`, with the same three-source pattern:

### 1. Vault
```bash
# Store once:
vault-resolver write ssh-<your-host> ssh_password="my-password"

# Use:
SSH_EXECUTOR_ALLOW_DANGEROUS=1 ssh-run.sh --host <your-host> --user <user> --ssh-pass-vault <your-host> -- 'df -h'
```

### 2. Environment variable
```bash
SSH_EXECUTOR_ALLOW_DANGEROUS=1 SSH_PASS="my-password" ssh-run.sh --host <your-host> --user <user> -- 'df -h'
```

### 3. Interactive prompt via LLM
```bash
SSH_EXECUTOR_ALLOW_DANGEROUS=1 ssh-run.sh --host <your-host> --user <user> --ssh-pass-ask -- 'df -h'
# → exit 96: "Ask the user for the password, then retry with SSH_PASS"
```

**Priority:** vault → `SSH_PASS` env var → `--ssh-pass-ask`

When key-based auth is available (`--vault-key` or `--key`), it takes precedence over password auth. Password auth is only attempted when no key is configured.

**Requires:** `sshpass` (`apt install sshpass` / `brew install sshpass`).

**Vault format:** item `ssh-<name>` with field `ssh_password` (plain text).

## Vault Integration

The skill supports pluggable vault backends via the `VAULT_RESOLVER_BIN` environment variable. The default backend is `vault-resolver` (Vaultwarden API, Hermes-native), but you can point it at any CLI that accepts JSON on stdin and returns JSON on stdout.

### Quick setup per platform

| Platform | Vault backend | Setup |
|----------|--------------|-------|
| **Hermes Agent** | vault-resolver (built-in) | Zero config — auto-detected |
| **Bitwarden** | `bw` CLI | `export VAULT_RESOLVER_BIN="bw"` |
| **1Password** | `op` CLI | `export VAULT_RESOLVER_BIN="op"` |
| **HashiCorp Vault** | `vault` CLI | `export VAULT_RESOLVER_BIN="/path/to/vault-wrapper"` |
| **None** | Key files only | Skip `--vault-key`, use `--key` or env vars |

### vault-resolver specifics (Hermes Agent)

Path: `/opt/data/bin/vault-resolver` (hardcoded in scripts; override with `VAULT_RESOLVER_BIN`).

Key storage convention:
- SSH keys: item `ssh-<name>` with field `ssh_private_key` (base64)
- SSH passwords: item `ssh-<name>` with field `ssh_password` (plain text)  
- Sudo passwords: item `sudo-<name>` with field `sudo_password` (plain text)

For self-signed certificate environments: vault-resolver uses `SSL_CTX.check_hostname=False`. **Only safe on trusted local networks** (LAN, VPN, localhost).

See `references/vault-backends.md` for custom backend integration and API contract.

### Usage with --vault-key

```bash
# ALWAYS pass --vault-key to connect with a vault key
scripts/ssh-run.sh --host <your-host> --vault-key id-rsa -- 'command'

# Does NOT work without --vault-key — IdentityFile from SSH config may not exist
```

### Fallback without vault-key (when key is not in vault)

If `--vault-key` fails because the SSH key was never stored in Vaultwarden (`Expecting value` error), use direct SSH with the local key on disk:

```bash
ssh -o StrictHostKeyChecking=yes -i ~/.ssh/id_rsa <user>@<host> '<command>'
```

If this is first contact with the host, verify its fingerprint manually before connecting. Add it to `~/.ssh/known_hosts` via `ssh-keyscan` or accept interactively. Never use `StrictHostKeyChecking=no` for unknown hosts.

This bypasses the vault-resolver dependency. The native backend with `ssh-agent` is the current default. Use this fallback **only for read-only commands** (df, ps, cat, ls). After confirming it works, consider storing the key in the vault:

```bash
ssh-keys.sh store id-rsa ~/.ssh/id_rsa
```

This way, `--vault-key` will work normally in future sessions.

**Warning:** The `ssh-run.sh` wrapper flags commands with `2>/dev/null`, `|`, `&&`, `||` as dangerous (exit 99). When using direct SSH, these redirections work without blocking.

### Known Pitfalls

| Problem | Cause | Solution |
|---------|-------|----------|
| `Permission denied (publickey)` | `--vault-key` not passed; tries IdentityFile from SSH config | Add `--vault-key <name>` |
| `'ssh-id-rsa' not found` | vault-resolver looks in `login.password`, but key is in `notes` | Use `ssh-keys.sh store` to recreate with custom field `ssh_private_key` (see `references/vault-key-format.md`) |
| `Failed to resolve vault key <name>: Expecting value` | The SSH key **does not exist** in Vaultwarden — item `ssh-<name>` was never created, is empty, or has invalid format | Fall back to direct SSH with local key (see "Fallback without vault-key" below), then store the key in vault with `ssh-keys.sh store <name> ~/.ssh/id_rsa` |
| `No module named 'paramiko'` | Python/Paramiko backend (fallback, used only when `openssh-client` is unavailable on the system) but paramiko not installed | `uv pip install --target ~/.openclaw/workspace/.ssh-pylib paramiko` |
| `timed out` (SSH connection) | Wrong port or hostname — Python backend wasn't resolving SSH config | Now resolves HostName/Port/User from `~/.ssh/config` automatically |
| `authentication failed` | (a) SSH key was never deployed to server's `authorized_keys` — Paramiko rejects during key exchange; (b) vault-resolver returned key from wrong field (notes vs field) | (a) Fall back to direct SSH with local key (see "Fallback without vault-key" below) and confirm the key works; then optionally store with `ssh-keys.sh store <name> <path>`; (b) Use `ssh-keys.sh store` to recreate in correct format |
| `ssh-keys.sh` timeout (~30s) | vault-resolver authentication via bw CLI was slow (~18s) | Direct API rewrite reduces to ~2s with session cache |
| `PermissionError: /tmp/.bw_hermes/api_session.json` | vault-resolver cache created by different UID (e.g. 1000 vs 10000) | Set `BITWARDENCLI_APPDATA_DIR` to a writable directory, e.g. `BITWARDENCLI_APPDATA_DIR=/opt/data/tmp/bw-cache` before calling vault-resolver or ssh-run.sh with --vault-key |
| `cat` with redirections or short pipes blocked as "dangerous" (exit 99) | `ssh-run.sh` heuristic detects `2>/dev/null`, pipes `|` or `&&`/`||` as potentially dangerous, even for read-only commands | Simplify the command: remove redirections, split into separate commands, or run with `ssh -i ~/.ssh/id_rsa` directly without the wrapper |
| `find` command with pipe blocked as "dangerous" (exit 99) | False positive from heuristic: `find ... | while read d; do ts=$(stat -c %Y "$d"); ...` contains `stat` + pipes that trigger the dangerous command detector, even though it's read-only | Simplify the command to avoid pipes with `stat`: (a) use `ls -1` + separate loop, (b) run in two SSH calls, or (c) use `--confirm-dangerous` **only when the command is provably read-only** |
| `ControlSocket /tmp/ssh-mux-... already exists` | Master socket from a previous session is still active (within ControlPersist) | Normal and expected — means multiplexing is working. To force a new socket, use `--control-close` on the previous command or wait for TTL to expire |
| **`Host key verification failed` despite correct known_hosts** | SSH config has `UserKnownHostsFile /dev/null` which discards all host keys | The script now forces `UserKnownHostsFile` when `StrictHostKeyChecking=yes`. Ensure host keys are in `${HOME}/.ssh/known_hosts` |
| **Group membership not updated (e.g. `sudo`, `docker`)** | ControlMaster socket caches the group list from the initial connection | Close the socket first: `ssh -O exit <host>` or `--control-close`, then reconnect for a fresh session with updated groups |
| `ControlPersist` doesn't work with different hosts even if same IP | `ControlPath` uses `%h` (hostname), not IP | Use the same alias/hostname in all calls. If you need to switch between alias and IP, standardize on the `~/.ssh/config` alias |
| `sudo: a terminal is required` even with `--pty` | `--pty` allocates a PTY, but if sudo asks for a password, the command hangs waiting for input | Configure `NOPASSWD` in sudoers **or** use `--sudo` with a password source: `--sudo-pass-vault`, `SSH_SUDO_PASS` env var, or `--sudo-pass-ask` |
| `--sudo requires a password source` (exit 97) | No vault item, no env var, and no `--sudo-pass-ask` flag provided | Provide one of: `--sudo-pass-vault <name>`, `SSH_SUDO_PASS` env var, or `--sudo-pass-ask` |
| `Failed to resolve sudo password from vault: sudo-<name>` (exit 97) | The item `sudo-<name>/sudo_password` does not exist in Vaultwarden | Create the item: `vault-resolver write sudo-<name> sudo_password="password"` |
| `SSH password auth requires SSH_EXECUTOR_ALLOW_DANGEROUS=1` (exit 98) | Password-based SSH auth attempted without environment opt-in | Set `export SSH_EXECUTOR_ALLOW_DANGEROUS=1` to acknowledge the elevated risk, then retry. Key-based auth does not require this gate. |
| `sudo requires SSH_EXECUTOR_ALLOW_DANGEROUS=1` (exit 98) | sudo attempted without environment opt-in | Set `export SSH_EXECUTOR_ALLOW_DANGEROUS=1` to acknowledge the elevated risk, then retry with `--confirm-dangerous`. |
| `ssh-run.sh` JSON output contains vault messages ("Retrieving SSH key...") | Old version of `ssh-keys.sh` (< 2026-07-22) wrote info messages to stdout | Update to the current version: all `cmd_restore()` messages now go to stderr. Stdout contains only JSON |
| `--vault-key` loads key but falls back to Python backend (no multiplexing) | `ssh-agent` is not running. `ssh-keys.sh restore` detects the absence and creates a temp file for the Python backend, which lacks ControlMaster | Start `ssh-agent` first: `eval "$(ssh-agent -s)"`. Without an active agent, each `--vault-key` generates a new TCP connection = auth.log spam |
| `Permission denied (publickey)` with wrong resolved_user | `~/.ssh/config` has no `User` directive for the host, and the alias doesn't specify a user. SSH uses the local system user | Pass `--user <user>` explicitly: `ssh-run.sh --host <your-host> --user <user> --vault-key <key-name> -- 'command'`. Or add `User <user>` to the `Host` entry in `~/.ssh/config` |
| `sshpass: command not found` (exit 127) when using `--ssh-pass-*` | `sshpass` is not installed on the system | Install: `apt install sshpass` (Debian/Ubuntu) or `brew install sshpass` (macOS). sshpass is only needed for password-based SSH auth; key-based auth does not require it |
| `Permission denied (password)` with `--ssh-pass-*` | SSH server does not allow password authentication (`PasswordAuthentication no` in sshd_config) | Enable `PasswordAuthentication yes` on the server, or use key-based auth instead |
| `Host key verification failed` (exit 255) on first contact | Default is strict (`StrictHostKeyChecking=yes`). Host not in `~/.ssh/known_hosts`. | Manually verify the host fingerprint, then run: `ssh-keyscan <host> >> ~/.ssh/known_hosts`. Do NOT use `--host-key-checking no` as a shortcut. |
| `paramiko.ssh_exception.SSHException: Server ... not found in known_hosts` (Python backend) | Python backend uses `RejectPolicy` by default — same strict behaviour as native | Use native backend if possible (has multiplexing). If Python is required, verify host fingerprint and add to `~/.ssh/known_hosts`, or use `--host-key-checking no` only with explicit user approval. |
| `restore-to-file` leaves key on disk after crash | `ssh-keys.sh restore-to-file` writes decrypted key to a caller-specified path. Interruption (kill -9) prevents cleanup. | Prefer `ssh-keys.sh restore` (loads into ssh-agent, no disk). Use `restore-to-file` only as last resort. Verify cleanup after use. |
| `shred: command not found` (macOS) during key cleanup | macOS does not ship `shred`. The fallback `rm -f` is used but does not securely overwrite blocks. | Acceptable on macOS (APFS encryption at rest mitigates). On Linux, ensure `coreutils` is installed. |
| `restore-to-file` fails with "Refusing to write private key to system directory" | Path validation rejects system dirs: `/etc`, `/boot`, `/sys`, `/proc`, `/dev`, `/run` | Use a path under `/tmp/` or your home directory. |
| `restore-to-file` warns about non-tmp path | Output path not under `/tmp` or `/dev/shm` — key will persist across reboots | Use `/tmp/` for temporary key material. |
| `⚠️ SECURITY WARNING: Host-key checking disabled` in stderr | `--host-key-checking no` was passed — connection is MITM-vulnerable | Confirm with the user that they understand and accept the risk. Prefer adding the host key to `known_hosts` instead. |
| `Host key verification failed` despite host key in known_hosts | `~/.ssh/config` has `UserKnownHostsFile /dev/null` — SSH ignores known hosts. Strict checking has no trust store. | Native backend now forces `-o UserKnownHostsFile=${HOME}/.ssh/known_hosts` when strict. Grep config for `UserKnownHostsFile` directives pointing to `/dev/null`. See `references/testing-pitfalls-2026-07-23.md`. |
| `ssh-keys.sh restore` exits 1 but prints "✓ loaded" (ghost failure) | `set -e` + trap with `shred -u` on already-deleted temp file. EXIT trap fires after success path deleted file. | Fixed: trap uses `rm -f`. Explicit `shred -u` runs in code paths; trap is safety net. See `references/testing-pitfalls-2026-07-23.md`. |
| Temp key survives `kill -9` | `trap` cannot catch SIGKILL. If the process is hard-killed during `ssh-keys.sh restore`, the temp file at `/dev/shm/ssh-vault-*` (or `/tmp/ssh-vault-*` as fallback) remains. | Use `ssh-keys.sh cleanup` to list stale keys and `ssh-keys.sh cleanup --force` to shred them. The files are also cleaned on next normal invocation when the same key name is restored. |

### Ensuring vault-resolver is accessible

ssh-executor scripts use `/opt/data/bin/vault-resolver` (hardcoded path).

```bash
export PATH="/opt/data/bin:$PATH"
```

## Server-to-Server rsync (without ForwardAgent)

> **⚠️ DEPRECATED PATTERN — see `references/server-to-server-rsync.md` for security warning and preferred alternatives.**

When you need to copy files **between two remote servers** and there is no
ssh-agent running locally (making ForwardAgent impossible), prefer the SSH
tunneled variant (ForwardAgent) or pull-via-jump approach. Copying a private
key to a remote server is a last resort — use only with a dedicated
single-purpose key and explicit user approval.

## Bundled Resources

### `scripts/ssh-run.sh`
Main remote execution script. Automatically selects backend:
- **openssh-client native** when `ssh`/`ssh-agent`/`ssh-add` are available (includes vault-key via `ssh-agent`)
- **Python + Paramiko** as fallback (works without SSH binaries on the system)
- **Connection multiplexing** enabled by default (ControlMaster, 180s) to avoid audit log spam

```bash
scripts/ssh-run.sh --host <host> [--user <user>] [--port <port>] \
                   [--key <path>] [--vault-key <name>] \
                   [--timeout <sec>] [--host-key-checking <yes|no>] \
                   [--confirm-dangerous] \
                   [--control-persist <sec>] [--control-close] \
                   [--sudo --sudo-pass-vault <name>] \
                   -- '<remote command>'

scripts/ssh-run.sh --list-aliases              # list aliases from ~/.ssh/config
```

`--vault-key <name>` retrieves the SSH key from Vaultwarden (item `ssh-<name>`) and loads it into `ssh-agent`. With an active agent, the key stays in memory. Without `ssh-agent`, a temp file in RAM-backed `/dev/shm` is used as fallback (cleaned by trap handlers; see security caveats).
`--control-persist <sec>` how long the multiplexing socket stays alive (default: 180).
`--control-close` closes the master socket immediately after the command.
`--pty` allocates a pseudo-terminal (needed for `sudo` in non-interactive sessions).
`--sudo` runs the command with `sudo` using password from vault, env var, or user prompt.
`--sudo-pass-vault <name>` Vaultwarden item name with the sudo password (`sudo-<name>/sudo_password`).
`--sudo-pass-ask` signals the LLM to ask the user for the password (retry with `SSH_SUDO_PASS` env var).
`--ssh-pass-vault <name>` SSH password from Vaultwarden item `ssh-<name>/ssh_password` (used when no key is configured).
`--ssh-pass-ask` signals the LLM to ask the user for the SSH password (retry with `SSH_PASS` env var).

### `scripts/ssh-keys.sh`
Manages SSH keys in Vaultwarden.

```bash
scripts/ssh-keys.sh store <name> <path>          # store local key in vault
scripts/ssh-keys.sh restore <name>               # load from vault into agent (or temp file)
scripts/ssh-keys.sh restore-to-file <name> <out> # write from vault to file
scripts/ssh-keys.sh cleanup                         # list stale temp key files
scripts/ssh-keys.sh cleanup --force                 # shred stale temp key files
scripts/ssh-keys.sh agent-status                 # show keys loaded in agent
```

### `references/multiplexing-verification.md`
Verification procedure to confirm ControlMaster multiplexing is active: 6-step checklist (socket timestamp, mux PID, ss, auth.log), failure signals, and quick diagnostic command.

### `references/vault-backends.md`
API contract and setup guides for pluggable vault backends: vault-resolver (Hermes), Bitwarden CLI, 1Password CLI, HashiCorp Vault wrapper, and no-vault mode.

### `references/vault-ssh-integration.md`
Detailed architecture of how SSH keys are stored in Vaultwarden and loaded into memory. Read when you need to understand the security model or full flow.

### `references/docker-diagnostics-without-cli.md`

Techniques for diagnosing Docker containers remotely **without** access to the
Docker CLI (user without docker group, without sudo NOPASSWD). Lists 10 command
techniques (`cgroup`, `/proc/PID`, `ip neigh`, `ss`, `/dev/tcp`, docker-compose,
config files) and a real-world MariaDB case with `network_mode: host` that wasn't
listening on any port.
### `references/safety.md`
Detailed security rules for remote execution. Read when in doubt about what is considered destructive or how to handle sensitive hosts.

### `references/security-audit-2026-07-clawhub.md`
Complete ClawHub SkillSpector audit history across versions. Documents all findings, fixes, and false-positive classifications from v2.1.0 (47 findings) through v2.3.6.

---

## Editions (v2.4.0+)

The skill is split into two editions, built from the same source via `build.sh`:

| Edition | Package | Auth | Sudo | Lines |
|---------|---------|------|------|-------|
| **Base** | `ssh-executor-<ver>.zip` | Key only | No | 270 |
| **Full** | `ssh-executor-full-<ver>.zip` | Key + password | Yes | 481 |

**Base** is the default. No sudo, no password auth, no `sshpass` — minimal attack surface.  
**Full** adds sudo + SSH password auth behind `SSH_EXECUTOR_ALLOW_DANGEROUS=1`.

### Source layout

```
scripts/
├── ssh-run-native.sh        ← full (sudo + password)
├── ssh-run-native-base.sh   ← stripped (key-only)
├── ssh-run.sh / ssh-run-base.sh
├── ssh-keys.sh / ssh-client.py  ← shared

SKILL.md / SKILL.base.md     ← full / stripped docs
references/
├── safety.md / safety.base.md
└── ...

build.sh                     ← bash build.sh <version>
```

Design: separate files over marker-based stripping. Simpler to maintain and audit.
ClawHub SkillSpector security audit results (47 findings). Documents all high-confidence vulnerabilities found and how they were fixed in v2.2.0. Read when maintaining or extending the skill to avoid reintroducing known issues: host-key bypass, credential mismanagement, key exfiltration, undeclared MCP capabilities.

### `references/remote-backup-cleanup.md`
Remote backup cleanup pattern with `find -mtime +N -delete`. Covers the permission model (write access to directory vs. file ownership), solutions for `Permission denied`, and diagnostic commands with `namei`. Refer to when deleting old files in remote backup directories.

## Example Requests That Should Trigger This Skill

These phrases require **explicit user invocation** — the skill should NOT auto-trigger from casual conversation about servers.

- "ssh-executor: check uptime on the production server"
- "Run ssh-run.sh to inspect docker ps on the app server"
- "Use the SSH skill to store my id_rsa key as 'prod-key'"
- "Access the server via ssh-executor and check journalctl"
- "ssh-executor: systemctl restart nginx on web-server (with confirmation)"
- "Sync backups from app-server to backup-server using ssh-executor rsync pattern"

The skill triggers on phrases that explicitly reference **ssh-executor** or the **ssh-run.sh / ssh-keys.sh** scripts. Casual mentions of "server", "deploy", or "SSH" alone should NOT activate this skill.
