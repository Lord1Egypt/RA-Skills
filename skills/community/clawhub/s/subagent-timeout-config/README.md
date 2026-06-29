# subagent-timeout-config

> One-click subagent timeout configurator for [OpenClaw](https://docs.openclaw.ai).
> Three preset profiles + custom values + auto-backup + optional gateway restart.

## The problem

OpenClaw timeouts are split across **three nested JSON fields** that must be
tuned together:

```json
{
  "agents": {
    "defaults": {
      "timeoutSeconds": 30,           // per-tool-call wait
      "subagents": {
        "runTimeoutSeconds": 1800     // per-subagent task budget
      }
    }
  },
  "acp": {
    "runtime": {
      "ttlMinutes": 30                // ACP session lifetime
    }
  }
}
```

**Hidden trap**: `ttlMinutes * 60 ≥ runTimeoutSeconds` — violate this and
ACP sessions die before subagents finish.

Default OpenClaw values (30s / 30min / 30min) are too tight for many
real-world tasks: codex/claude-code planning runs, large refactors, complex
analysis pipelines. Manually editing JSON + remembering the constraint +
restarting Gateway is friction every OpenClaw user hits.

This skill does it in one command.

## Install

### Via [clawhub](https://clawhub.com)
```bash
clawhub install subagent-timeout-config
```

### Via [skills.sh](https://skills.sh)
```bash
npx skills install subagent-timeout-config
```

### Manual
```bash
git clone https://github.com/Songhonglei/better-agent-skills.git
cp -r better-agent-skills/skills/subagent-timeout-config ~/.openclaw/skills/
```

## Quick start

Tell your agent: **"set subagent timeout to patient"** or **"配置 subagent
超时为 patient 档位"** — the skill takes care of the rest.

Or directly:

```bash
# List available profiles
python3 <skill-install-path>/scripts/set_timeout.py --list

# Preview before applying
python3 <skill-install-path>/scripts/set_timeout.py --profile patient --dry-run

# Apply (auto-backup + auto-restart)
python3 <skill-install-path>/scripts/set_timeout.py --profile patient

# Check current
python3 <skill-install-path>/scripts/set_timeout.py --status
```

## Profiles

| Profile | timeoutSeconds | runTimeoutSeconds | ttlMinutes | Use case |
|---|---|---|---|---|
| `quick` | 60s (1min) | 3600s (1h) | 60min (1h) | Fast feedback, interactive debugging |
| `normal` | 180s (3min) | 7200s (2h) | 120min (2h) | Everyday development |
| `patient` | 300s (5min) | 10800s (3h) | 180min (3h) | Long-running tasks, big codebases |

Aliases: `impatient` / `fast` → `quick`, `slow` → `patient`.

## Safety features

- **Auto-backup** of the original config to `<config>.bak.<YYYYMMDD-HHMMSS>`
- **Atomic write** (`.tmp` + rename) — no half-written JSON on crash
- **Constraint validation** before any write — refuses invalid combos
- **Restart opt-out** via `--no-restart` (won't interrupt running tasks)
- **`--dry-run` preview** that shows exact field-level diff

## CLI Reference

| Flag | Description |
|------|-------------|
| `--profile <name>` | `quick` / `normal` / `patient` (+ aliases) |
| `--custom T,R,TTL` | Custom values, 3 comma-separated integers |
| `--status` | Show current configuration |
| `--list` | List all preset profiles |
| `--config <path>` | Override config path (default `~/.openclaw/openclaw.json`) |
| `--dry-run` | Preview only; no write/restart |
| `--no-restart` | Apply but don't restart Gateway |

Exit codes: `0` = success, `1` = error.

## Trigger phrases (English / 中文)

- "set subagent timeout", "configure timeout", "openclaw timeout"
- "my subagent keeps timing out", "subagent dying mid-task"
- 「配置 subagent 超时」「调整超时」「subagent 总是被杀」
- 「设置超时档位」「subagent 跑不完」

## Files

```
subagent-timeout-config/
├── SKILL.md            # Skill manifest (read by agents)
├── README.md           # This file
├── LICENSE             # MIT
└── scripts/
    └── set_timeout.py  # The configurator
```

## Requirements

- Python 3.8+ (standard library only)
- `openclaw` CLI on PATH (for auto-restart; pass `--no-restart` if absent)

## License

MIT — see [LICENSE](./LICENSE).

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
