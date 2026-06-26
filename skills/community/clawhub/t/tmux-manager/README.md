# tmux-manager

A powerful tmux session manager that lets you define your development environments in YAML and spin them up instantly with a single command.

## Features

- **YAML-based configuration** — Define sessions, windows, panes, layouts, and hooks in one file
- **Session and window groups** — Target whole sessions with `session_group`, or open only specific windows across sessions with `window_group`
- **Pre/Post hooks** — Run commands before/after session creation (docker compose, notifications, etc.) with optional `abort` on failure
- **Environment variables** — Set session or window-level environment variables
- **Live session inspection** — Tail output or send commands to running sessions
- **Idempotent operations** — Skip sessions that are already running, or force restart with `--restart`
- **Dry-run mode** — Preview what would happen without making changes

## Quick Start

```bash
# Copy sample config (replace SKILL_DIR with where the skill is installed)
cp $SKILL_DIR/scripts/tmux-sessions.yaml.sample \
   $SKILL_DIR/scripts/tmux-sessions.yaml

# Edit config with your sessions
nvim $SKILL_DIR/scripts/tmux-sessions.yaml

# Create all sessions
uv run $SKILL_DIR/scripts/tmux-manager.py --all
```

## Example Configuration

```yaml
sessions:
  - name: Project_1
    session_group: Project_1
    working_dir: ~/Projects/Project_1
    windows:
      - name: claude
        window_group: claude
        command: "claude --dangerously-skip-permissions --continue"
      - name: gemini
        window_group: gemini
        command: "gemini -y --resume"
      - name: shell

  - name: Project_2
    session_group: Project_2
    working_dir: ~/Projects/Project_2
    env:
      NODE_ENV: development
      PORT: 3000
    windows:
      - name: claude
        window_group: claude
        command: "claude --dangerously-skip-permissions --continue"
      - name: gemini
        window_group: gemini
        command: "gemini -y --resume"
      - name: shell
        window_group: shell
```

## Common Commands

```bash
# List all sessions and their status
uv run $SKILL_DIR/scripts/tmux-manager.py --all --list

# Create all sessions in a session-group (all windows)
uv run $SKILL_DIR/scripts/tmux-manager.py --session-group work

# Create sessions but only windows in a window-group
uv run $SKILL_DIR/scripts/tmux-manager.py --window-group dev

# Restart sessions
uv run $SKILL_DIR/scripts/tmux-manager.py --all --restart

# Kill sessions
uv run $SKILL_DIR/scripts/tmux-manager.py --all --kill

# Send command to a session (active window)
uv run $SKILL_DIR/scripts/tmux-manager.py --send-keys -s my-project "npm test"

# Send command to a specific window
uv run $SKILL_DIR/scripts/tmux-manager.py --send-keys -s my-project:shell "npm test"

# Tail live output from a session
uv run $SKILL_DIR/scripts/tmux-manager.py --tail -s my-project

# List available groups
uv run $SKILL_DIR/scripts/tmux-manager.py --list-groups

# Snapshot a pane (native tmux — no wrapper needed)
tmux capture-pane -p -t my-project

# Kill all tmux sessions (native tmux — no wrapper needed)
tmux kill-server
```

## Requirements

- `tmux` — Terminal multiplexer
- `uv` — Python package/script runner (`brew install uv` or see https://docs.astral.sh/uv/)

Dependencies (`pyyaml`) are managed automatically by `uv` via inline script metadata.

## License

MIT License — Feel free to use, modify, and distribute.

---

**Skill for OpenClaw**

## Troubleshooting

### Error: Config file not found

Make sure `tmux-sessions.yaml` is in the same directory as `tmux-manager.py`, or use `--config` to specify a path.

### Session not starting

Use `--validate` to check your config:

```bash
uv run $SKILL_DIR/scripts/tmux-manager.py --validate
```

