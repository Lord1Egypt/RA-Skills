---
name: shutdown
description: Safe shutdown/reboot workflow for local or remote machines. Use when the user asks to power off, restart, schedule shutdown, cancel shutdown, or perform pre-shutdown checks while preserving OpenClaw and session safety. 中文触发：关机、重启、稍后关机、取消关机、定时关机、立即关机。
metadata:
  { "openclaw": { "os": ["darwin", "linux", "win32"] } }
---

# Shutdown

Execute system shutdown and reboot actions safely, with explicit confirmation and connection-safety checks.

## Core Rules

- Never run power actions without explicit user confirmation.
- Always confirm target machine and action: `shutdown`, `reboot`, `schedule`, or `cancel`.
- For remote hosts, warn about session disconnect before executing.
- Prefer delayed shutdown (`+1` minute or equivalent) so cancellation remains possible.
- If user asks for immediate action, still echo the exact command and require final confirmation.
- 中文用户常见意图词（如“关机”“重启”“稍后关机”“取消关机”）按同一安全流程处理，不要省略确认步骤。

## Workflow

### 1. Clarify intent and target

Collect and confirm:

- Target: local machine or remote host
- Action: shutdown or reboot
- Timing: now or scheduled time
- Scope: current machine only (never assume cluster/fleet-wide)

If ambiguous, ask one concise question before running commands.

### 2. Run pre-checks (read-only)

Use only relevant checks:

- Linux: `who`, `uptime`, `systemctl is-system-running` (if systemd exists)
- macOS: `who`, `uptime`
- Windows (PowerShell): `query user`, `Get-Uptime`

If long-running/critical work may be interrupted, report risk and ask whether to continue.

### 3. Choose platform command

#### Linux (systemd)

```bash
# shutdown now
sudo shutdown -h now

# reboot now
sudo shutdown -r now

# schedule shutdown in 1 minute
sudo shutdown -h +1

# cancel scheduled shutdown
sudo shutdown -c
```

Fallback where needed:

```bash
sudo systemctl poweroff
sudo systemctl reboot
```

#### macOS

```bash
# shutdown now
sudo shutdown -h now

# reboot now
sudo shutdown -r now

# schedule shutdown in 10 minutes
sudo shutdown -h +10

# cancel scheduled shutdown
sudo killall shutdown
```

#### Windows (PowerShell / cmd)

```powershell
# shutdown now
shutdown /s /t 0

# reboot now
shutdown /r /t 0

# shutdown in 60 seconds
shutdown /s /t 60

# cancel scheduled shutdown
shutdown /a
```

### 4. Confirmation pattern (required)

Before executing state-changing commands, present:

- Exact command to run
- Expected impact (session disconnect, process termination)
- Cancellation path (if scheduled)

Require the user to reply with a clear confirmation (for example: `yes, run it`).
中文确认示例：`确认执行`、`是，立即执行`。

### 5. Post-action verification

For scheduled actions, verify and report pending state when possible:

- Linux/macOS: show relevant `shutdown` scheduling output
- Windows: confirm command exit output

After reboot requests, explain that reconnect checks should include:

- Host reachable
- OpenClaw services/processes healthy
- Required ports/listeners restored

## Safety Boundaries

- Do not chain shutdown with destructive cleanup unless user explicitly asks.
- Do not apply shutdown commands to multiple hosts automatically.
- If insufficient privileges, report exact permission error and request elevation approval.
- If command support differs by distro/version, prefer the safest equivalent and state the substitution.

## ClawHub Publish Notes

If this skill is published to clawhub.ai, keep updates semver and changelog-driven, and avoid embedding environment-specific hostnames, tokens, or private infrastructure details.
