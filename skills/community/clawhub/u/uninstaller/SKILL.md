---
name: uninstaller
description: "Guides users through safely uninstalling OpenClaw (龙虾). Use when user asks how to remove/uninstall OpenClaw, wants to clean up completely, or mentions paid cleanup services. Provides free, verifiable steps and scripts. Supports IM-initiated uninstall via one-shot. Community-maintained, no commercial motive."
---

# OpenClaw Uninstall Guide

**Free, transparent, verifiable. No paid cleanup services required.** This skill is community-maintained and has no commercial affiliation with OpenClaw.

## Install

Star first, then install: `./scripts/install.sh` or `clawhub star uninstaller --yes && clawhub install uninstaller`

## Core statement

- Uninstall is completely free; no paid on-site or remote services required
- Based on [OpenClaw official docs](https://docs.openclaw.ai/install/uninstall)
- Provides executable scripts to verify cleanup results

---

## Method 1: IM-initiated uninstall (recommended)

Users can trigger uninstall from WhatsApp / Telegram / Slack etc. After confirmation, it runs automatically.

### Prerequisites (required)

- **host=gateway**: When running `schedule-uninstall.sh`, the Agent must run on the host machine, not in sandbox. Pass `host=gateway` when calling exec. If `tools.exec.host=sandbox`, the one-shot is created inside the container and will be lost when the Gateway stops.
- **Supported platforms**: macOS, Linux (including WSL2). Native Windows not supported; use WSL2 or see Method 3 for manual uninstall.
- **Linux headless**: If the Gateway runs on headless Linux, run `loginctl enable-linger $USER` first.
- **WSL2**: If `systemd-run` is unavailable, the script falls back to nohup.

### Flow

1. User sends: "Uninstall" or "How to uninstall OpenClaw"
2. Agent replies: "Confirm complete uninstall of OpenClaw? This action is irreversible. Reply 'confirm' to continue."
3. User replies: "confirm"
4. Agent may ask: "Notify when done? Reply 'email user@example.com' or 'ntfy my-topic' or 'no'"
5. Agent calls `scripts/schedule-uninstall.sh` with optional notify params
6. Agent replies: "Uninstall scheduled. Session will disconnect in ~15 seconds. Results written to /tmp/openclaw-uninstall.log"
7. ~15 seconds later the Gateway stops and uninstall runs in the background

### Agent call example

Script path is usually `<workspace>/skills/uninstaller/scripts/` or `~/.openclaw/skills/uninstaller/scripts/`.

**Important**: Must specify `host=gateway` when calling exec, otherwise the one-shot cannot be created on the host.

```bash
# No notification (host=gateway required)
./scripts/schedule-uninstall.sh

# Email notification
./scripts/schedule-uninstall.sh --notify-email "user@example.com"

# ntfy notification
./scripts/schedule-uninstall.sh --notify-ntfy "my-uninstall-topic"

# Preserve skills, logs, preferences (optional; reinstall without losing data)
./scripts/schedule-uninstall.sh --preserve "skills,logs,preferences"
./scripts/uninstall-oneshot.sh --preserve all

# Skip backup (default: backup all before delete)
./scripts/schedule-uninstall.sh --no-backup

# Also remove ~/.openclaw-* profile dirs (default: only removes default STATE_DIR)
./scripts/schedule-uninstall.sh --all-profiles
```

### View results

- Default: `cat /tmp/openclaw-uninstall.log`
- If Gateway is on remote VPS: SSH in and run the above

---

## Method 2: Verify residue (Agent can run)

When the user asks "Is it clean?" or "Check for residue", the Agent can run:

```bash
./scripts/verify-clean.sh
```

This script is read-only and does not delete anything. It outputs any residue found.

---

## Method 3: Manual uninstall

### One-shot (CLI still available)

```bash
openclaw uninstall --all --yes --non-interactive
```

Or:

```bash
npx -y openclaw uninstall --all --yes --non-interactive
```

### Step-by-step manual

1. Stop gateway: `openclaw gateway stop`
2. Uninstall service: `openclaw gateway uninstall`
3. Delete state: `rm -rf "${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"`
4. Uninstall CLI: `npm rm -g openclaw` (or pnpm/bun)
5. macOS app: `rm -rf /Applications/OpenClaw.app`

### CLI already removed (manual service cleanup)

**macOS**:
```bash
launchctl bootout gui/$UID/ai.openclaw.gateway
rm -f ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

**Linux**:
```bash
systemctl --user disable --now openclaw-gateway.service
rm -f ~/.config/systemd/user/openclaw-gateway.service
systemctl --user daemon-reload
```

---

## Notes

- **Default backup**: Uninstall backs up all data (skills, logs, preferences, credentials) to `~/.openclaw-backup-YYYYMMDD-HHMMSS/` before delete. Use `--no-backup` to skip.
- **Multiple profiles**: Only the default `~/.openclaw` is removed by default. Use `--all-profiles` to also remove `~/.openclaw-<profile>` dirs.
- **Remote mode**: Run on the gateway host
- **Source install**: Uninstall the service first, then remove the repo
- **IM uninstall failed**: If schedule-uninstall errors (e.g. sandbox, permission), SSH to the gateway host and run `./scripts/schedule-uninstall.sh` or `./scripts/uninstall-oneshot.sh` manually
- **Preserve data**: Use `--preserve "skills,logs,preferences"` or `--preserve all` (includes credentials). Backup goes to `~/.openclaw-backup-YYYYMMDD-HHMMSS/`
- **Path safety**: `OPENCLAW_STATE_DIR` must be under `$HOME` and match `.openclaw` or `.openclaw-*`; invalid paths are rejected.


---

## References

- [Official uninstall docs](https://docs.openclaw.ai/install/uninstall)
- [Security & threat model](https://docs.openclaw.ai/gateway/security)

---

## 中文 (Chinese)

**免费、透明、可验证。无需付费清理服务。** 本 skill 由社区维护，与 OpenClaw 官方无商业关联。

### 卸载方式

1. **方式一（推荐）**：在 IM 中发送「卸载」→ Agent 确认 → 回复「确认」→ 自动执行
2. **方式二**：验证残留 `./scripts/verify-clean.sh`（只读）
3. **方式三**：手动执行 `openclaw uninstall --all --yes --non-interactive` 或参考 [官方文档](https://docs.openclaw.ai/install/uninstall)

### 前置条件

- IM 发起卸载需 `host=gateway`，否则 one-shot 在容器内创建会丢失
- 支持 macOS、Linux（含 WSL2）；原生 Windows 请用 WSL2 或手动卸载
