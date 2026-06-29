---
name: subagent-timeout-config
description: >
  One-click subagent timeout configurator for OpenClaw. Configures the three
  related fields (agents.defaults.timeoutSeconds + subagents.runTimeoutSeconds
  + acp.runtime.ttlMinutes) atomically with built-in TTL constraint validation
  (ttlMinutes * 60 ≥ runTimeoutSeconds). Three preset profiles — quick
  (60s/1h/1h, fast feedback), normal (3min/2h/2h, everyday dev), patient
  (5min/3h/3h, long-running tasks) — plus --custom for arbitrary values.
  Auto-backup before write, optional gateway auto-restart, --dry-run preview.
  Triggers: "set subagent timeout", "subagent 超时", "配置 timeout", "调整超时",
  "subagent timeout config", "openclaw timeout", "tool call timeout".
---

# subagent-timeout-config

- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/better-agent-skills
- **License**: MIT

One-click timeout configurator for [OpenClaw](https://docs.openclaw.ai)
subagents. Set the three related timeout fields atomically with built-in
constraint validation, automatic backup, and optional gateway restart.

> ⚠️ **OpenClaw-only by default** — reads/writes `~/.openclaw/openclaw.json`.
> Use `--config <path>` to target a different runtime's JSON config file.

---

## Why this skill exists

OpenClaw timeouts are split across **three nested fields** that must be tuned
together:

| Field | Path | What it controls |
|---|---|---|
| `timeoutSeconds` | `agents.defaults.timeoutSeconds` | Per-tool-call wait |
| `runTimeoutSeconds` | `agents.defaults.subagents.runTimeoutSeconds` | Per-subagent task budget |
| `ttlMinutes` | `acp.runtime.ttlMinutes` | ACP session lifetime |

**Hidden trap**: `ttlMinutes * 60` must be `≥ runTimeoutSeconds`, otherwise
sessions die before subagents finish. Default OpenClaw values (30s / 30min /
30min) are too tight for many real-world tasks (codex/claude-code planning,
large refactors, complex analysis).

This skill picks the right combination in one command, validates the
constraint, backs up the original config, and restarts the gateway.

---

## Preset Profiles

| Profile | timeoutSeconds | runTimeoutSeconds | ttlMinutes | Use case |
|---|---|---|---|---|
| `quick` | 60s (1min) | 3600s (1h) | 60min (1h) | Fast feedback, interactive debugging |
| `normal` | 180s (3min) | 7200s (2h) | 120min (2h) | Everyday development |
| `patient` | 300s (5min) | 10800s (3h) | 180min (3h) | Long-running tasks, big codebases |

Aliases: `impatient` / `fast` → `quick`, `slow` → `patient`.

---

## Usage

### Preview before applying (recommended first time)

```bash
python3 <skill-install-path>/scripts/set_timeout.py --profile normal --dry-run
```

### Apply a profile (with auto-restart)

```bash
python3 <skill-install-path>/scripts/set_timeout.py --profile patient
```

### Apply without restarting Gateway

```bash
python3 <skill-install-path>/scripts/set_timeout.py --profile normal --no-restart
# Then later, when you're ready:
openclaw gateway restart
```

### Custom values

```bash
# Format: timeoutSeconds,runTimeoutSeconds,ttlMinutes
python3 <skill-install-path>/scripts/set_timeout.py --custom 240,9000,150
```

### Check current configuration

```bash
python3 <skill-install-path>/scripts/set_timeout.py --status
```

### List all profiles

```bash
python3 <skill-install-path>/scripts/set_timeout.py --list
```

### Target a non-default config path

```bash
python3 <skill-install-path>/scripts/set_timeout.py \
  --profile normal --config /path/to/your/openclaw.json
# Or via env:
OPENCLAW_CONFIG=/path/to/openclaw.json python3 <...>/set_timeout.py --profile normal
```

---

## Workflow (when the agent invokes this skill)

1. Ask the user which profile suits their task (or accept `--custom`).
2. Show `--dry-run` diff first when the user is unsure.
3. Apply with default settings (auto-backup + auto-restart).
4. Confirm new settings via `--status`.
5. If validation fails (e.g. TTL too small), explain the constraint and offer
   a corrected value.

---

## Safety Features

- **Auto-backup**: Before every write, the original config is copied to
  `<config>.bak.<YYYYMMDD-HHMMSS>`. Restore by `cp` if needed.
- **Atomic write**: New config is written to a `.tmp` file then renamed,
  so a crash mid-write never leaves a corrupt JSON.
- **Constraint validation**: Refuses to apply invalid combos (e.g. ttlMinutes
  too small for runTimeoutSeconds). Validation runs **before** any file
  modification — `--dry-run` and real applies both validate.
- **Restart opt-out**: `--no-restart` lets you defer the Gateway restart
  (useful when you have a long-running task you don't want to interrupt).

---

## CLI Reference

| Flag | Description |
|------|-------------|
| `--profile <name>` | Apply preset: `quick` / `normal` / `patient` (+ aliases) |
| `--custom T,R,TTL` | Apply custom values (3 comma-separated integers) |
| `--status` | Print current configuration |
| `--list` | List all available profiles |
| `--config <path>` | Override config file path (default `~/.openclaw/openclaw.json`) |
| `--dry-run` | Preview diff; do not write file or restart Gateway |
| `--no-restart` | Skip `openclaw gateway restart` after writing |

Exit codes: `0` = success, `1` = error (bad args, IO, validation failure).

---

## Dependencies

- Python 3.8+ (standard library only — no pip dependencies)
- `openclaw` CLI on PATH (only needed for the auto-restart step; use
  `--no-restart` if you don't have it)

---

## What This Skill Is NOT

- **Not** a generic timeout tool — it only knows about OpenClaw's three
  specific fields. For other agent runtimes' config formats, use `--config`
  to point at a custom JSON path but be aware the schema is OpenClaw-specific.
- **Not** a persistent daemon — it's a one-shot CLI invocation.
- **Not** a profile editor — to add a new preset, edit `PROFILES` in
  `scripts/set_timeout.py`.

---

## Key Files

| File | Purpose |
|------|---------|
| `scripts/set_timeout.py` | Configurator: profiles, validation, backup, restart |
