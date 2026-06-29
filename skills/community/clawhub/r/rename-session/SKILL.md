---
name: rename-session
description: >
  Rename or auto-generate a friendly label for an OpenClaw-style session by
  editing sessions.json directly. Supports random labels (zh/en with locale
  auto-detect), multi-agent auto-detection, listing sessions,
  retry with verification, and XDG-compliant history storage.
  适用场景:在 OpenClaw / 任何兼容的 session 管理体系中给会话起名/改名/换花名/重命名 session/给会话加 label。
---

# rename-session

- **Version**: 1.0.0
- **License**: MIT
- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/better-agent-skills

Minimal, zero-dependency tool to rename a session label in
`<agents-root>/<agent>/sessions/sessions.json` (OpenClaw-style layout).

## Quick start

```bash
# List all sessions under the only agent under ~/.openclaw/agents/
python3 scripts/rename_session.py --list

# Rename a session with a literal label
python3 scripts/rename_session.py agent:main:main "My new session name" --agent main

# Auto-generate a random label (auto-detects language from $LANG)
python3 scripts/rename_session.py agent:main:main --random --agent-name Ashley

# Force Chinese label
python3 scripts/rename_session.py agent:main:main --random --lang zh --agent-name Ashley

# Force English label
python3 scripts/rename_session.py agent:main:main --random --lang en --agent-name Ashley
```

## CLI

| Flag | Description | Default |
|---|---|---|
| `session_key` | Session key, e.g. `agent:main:main` | required (unless `--list`) |
| `new_label` | New literal label | required unless `--random` |
| `--random` | Auto-generate a random label | false |
| `--list` | List all session keys under the agent and exit | false |
| `--lang zh\|en` | Language for `--random` vocabulary | auto-detect from `$LC_ALL`/`$LC_MESSAGES`/`$LANG`, fall back to `en` |
| `--agent-name <name>` | Agent display name used in random label | `Ashley` |
| `--agent <id>` | Agent ID. Auto-detected when only one exists | auto |
| `--root <path>` | Agents root | `$RENAME_SESSION_ROOT` or `~/.openclaw/agents` |

## Configuration via environment

| Env var | Purpose | Default |
|---|---|---|
| `RENAME_SESSION_ROOT` | Override agents root | `~/.openclaw/agents` |
| `XDG_DATA_HOME` | Where history is stored | `~/.local/share` |

History file: `$XDG_DATA_HOME/rename-session/history.json` (keeps last 10
labels to avoid immediate repeats when using `--random`).

## Random label format

```
<scene><agent-name><mood-emoji><state-word><state-emoji>
```

Example outputs:

- `zh`: `春光明媚Ashley🌸元气满满💻`
- `en`: `March Breeze Ashley🌸 Energized💻`

70% of the time the scene is month-aware (e.g. March produces spring words).

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Success (rename verified or list completed) |
| 1 | Failure (3 retries exhausted, missing session, or file errors) |
| 2 | Bad CLI arguments |

## Failure reasons

| Output | Explanation |
|---|---|
| `sessions.json not found at ...` | Agent does not exist or has no sessions yet |
| `session key '...' not found` | The specified session key does not exist |
| `File permission issues` | Cannot write to sessions.json |
| `Disk is full or read-only` | Filesystem write blocked |
| `Another process is continuously modifying sessions.json` | Concurrent writers; retry later |

## Notes

- Changes take effect immediately in the file; refresh the session list in
  your client to see the new label.
- Multi-agent: when more than one agent is detected under the root,
  `--agent <id>` is required.
- All randomized output uses standard Python `random` (no external deps).

See `references/TESTING.md` for the test plan.
