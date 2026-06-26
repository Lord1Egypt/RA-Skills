---
name: tmux-manager
description: Manage tmux sessions using the tmux-manager.py script. Use when asked to create, kill, restart, list, or inspect tmux sessions, send commands to sessions, tail session output, or validate the sessions config file.
metadata:
  {
    "openclaw":
      {
        "emoji": "💻",
        "requires": { "bins": ["uv", "tmux"] },
        "install":
          [
            {
              "id": "uv-brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
            {
              "id": "tmux-brew",
              "kind": "brew",
              "formula": "tmux",
              "bins": ["tmux"],
              "label": "Install tmux (brew)",
            },
          ],
      },
  }
---

# tmux-manager

Manages tmux sessions from a YAML config file. The script and its default config live together — the script always looks for `tmux-sessions.yaml` in the same directory as itself.

**Script:** `{baseDir}/scripts/tmux-manager.py`
**Default config:** `{baseDir}/scripts/tmux-sessions.yaml`
**Sample config:** `{baseDir}/scripts/tmux-sessions.yaml.sample`

To deploy: copy `tmux-manager.py` to any directory, place a `tmux-sessions.yaml` next to it, and run it with `uv run` from anywhere.

---

## Usage

```
uv run {baseDir}/scripts/tmux-manager.py (--all | -s SESSION [...] | --session-group GROUP [...] [--window-group GROUP [...]] | --window-group GROUP [...]) [--kill | --restart] [--dry-run] [--list] [--config FILE]
uv run {baseDir}/scripts/tmux-manager.py --send-keys -s SESSION[:WINDOW] COMMAND
uv run {baseDir}/scripts/tmux-manager.py --tail -s SESSION[:WINDOW]
uv run {baseDir}/scripts/tmux-manager.py --validate [--config FILE]
uv run {baseDir}/scripts/tmux-manager.py --list-groups [--config FILE]
```

---

## Flags

### Selectors

| Flag | Meaning |
|---|---|
| `--all` | Target every session in the config |
| `--session-group GROUP` | Target sessions by `session_group` (repeatable, comma-separated) — all windows created |
| `--window-group GROUP` | Filter to only matching windows (repeatable, comma-separated) — can be combined with `--session-group` |
| `-s SESSION` | Target a specific session by name (repeatable) |

`--all` and `-s` are mutually exclusive with everything else. `--session-group` and `--window-group` can be used together to scope both sessions and windows.

### Actions — default is create

| Flag | Meaning |
|---|---|
| *(no action flag)* | Create targeted sessions; skip ones already running |
| `--kill` | Kill targeted sessions |
| `--restart` | Kill then recreate targeted sessions |
| `--list` | Show status table (running/stopped) — no changes made |
| `--dry-run` | Preview what would happen — no changes made |

### Output / Inspection

| Flag | Meaning |
|---|---|
| `--tail -s SESSION[:WINDOW]` | Stream live pane output (Ctrl+C to stop) |

### Send Commands

| Flag | Meaning |
|---|---|
| `--send-keys -s SESSION[:WINDOW] "cmd"` | Send a shell command to a running session or specific window |

### Config & Validation

| Flag | Meaning |
|---|---|
| `--config FILE` | Use an alternative config file |
| `--validate` | Check config for errors and warnings (no selector needed) |
| `--list-groups` | List all session groups and window groups (no selector needed) |

---

## Examples

```bash
uv run {baseDir}/scripts/tmux-manager.py --all                              # create all sessions
uv run {baseDir}/scripts/tmux-manager.py --all --kill                       # kill all sessions in config
uv run {baseDir}/scripts/tmux-manager.py --all --restart                    # restart all sessions
uv run {baseDir}/scripts/tmux-manager.py --all --dry-run                    # preview what would be created
uv run {baseDir}/scripts/tmux-manager.py --all --list                       # list status of all sessions
uv run {baseDir}/scripts/tmux-manager.py --session-group work                     # create sessions in session-group 'work'
uv run {baseDir}/scripts/tmux-manager.py --session-group work --restart           # restart sessions in session-group 'work'
uv run {baseDir}/scripts/tmux-manager.py --session-group work --list              # list status of sessions in session-group 'work'
uv run {baseDir}/scripts/tmux-manager.py --kill --session-group work              # kill all sessions in session-group 'work'
uv run {baseDir}/scripts/tmux-manager.py --window-group dev                       # create sessions, only 'dev' windows
uv run {baseDir}/scripts/tmux-manager.py --window-group dev --restart             # restart with only 'dev' windows
uv run {baseDir}/scripts/tmux-manager.py --window-group claude,gemini             # multiple groups, comma-separated
uv run {baseDir}/scripts/tmux-manager.py --window-group claude --window-group gemini  # equivalent
uv run {baseDir}/scripts/tmux-manager.py --session-group TargetTracer,N8N --window-group claude,gemini  # combined
uv run {baseDir}/scripts/tmux-manager.py -s my-session                            # create only my-session
uv run {baseDir}/scripts/tmux-manager.py --kill -s my-session                     # kill only my-session
uv run {baseDir}/scripts/tmux-manager.py --restart -s my-session                  # restart only my-session
uv run {baseDir}/scripts/tmux-manager.py --send-keys -s my-session "cmd"               # send to active window
uv run {baseDir}/scripts/tmux-manager.py --send-keys -s my-session:claude "cmd"        # send to specific window
uv run {baseDir}/scripts/tmux-manager.py --tail -s my-session                     # stream live pane output
uv run {baseDir}/scripts/tmux-manager.py --validate                               # validate config file
uv run {baseDir}/scripts/tmux-manager.py --list-groups                            # list all groups
uv run {baseDir}/scripts/tmux-manager.py --all --config ~/my-sessions.yaml        # use a specific config
```

---

## Behaviour Notes

- **Idempotent creates** — sessions already running are skipped. Use `--restart` to force recreate.
- **`--kill` requires a selector** — use `--all --kill` to kill everything managed by this config.
- **`--tail` / `--send-keys`** accept only a single `-s SESSION[:WINDOW]` target.
- **`SESSION[:WINDOW]`** — append `:windowname` to target a specific window, e.g. `my-session:claude`. Without it, the active window is used.
- **`--validate`** does not require a selector — warns on unknown fields, catching typos like `window_grou` or `sesion_group`.
- **`--list-groups`** does not require a selector — reads config only.
- **`pre_hook` / `post_hook`** run on the host shell, not inside tmux.
- **`pre_hook_fail: abort`** — stops session creation if the pre_hook exits non-zero. Default is `warn` (prints warning, continues).
- **`--window-group`** — sessions already running are skipped unless `--restart` is used. On restart, only the matching windows are created.
- **`--session-group` + `--window-group` combined** — narrows to the specified sessions first, then opens only the matching windows within them.
- **Sessions without a `session_group`** are only reachable via `--all` or `-s`.

---

## Native tmux equivalents

These operations don't need a wrapper — use tmux directly:

| Operation | Native command |
|---|---|
| Kill all tmux sessions | `tmux kill-server` |
| Snapshot pane output | `tmux capture-pane -p -t SESSION[:WINDOW]` |

---

## Sample Config (`tmux-sessions.yaml.sample`)

```yaml
sessions:

  # ── Project session (no env vars) ─────────────────────────────────────────
  - name: Project_1
    session_group: Project_1
    working_dir: ~/Projects/Project_1
    # focus: claude             # which window to select after creation (optional)
    windows:
      - name: claude
        window_group: claude    # targeted by: --window-group claude
        command: "claude --dangerously-skip-permissions --continue"
      - name: gemini
        window_group: gemini    # targeted by: --window-group gemini
        command: "gemini -y --resume"
      - name: shell             # no window_group — only opened via --session-group or --all
        # no command = opens a plain shell

  # ── Project session (with env vars) ───────────────────────────────────────
  - name: Project_2
    session_group: Project_2
    working_dir: ~/Projects/Project_2
    env:
      NODE_ENV: development
      PORT: 3000
    windows:
      #- name: server           # uncomment to add a dev server window
      #  command: "npm run dev"
      - name: claude
        window_group: claude
        command: "claude --dangerously-skip-permissions --continue"
      - name: gemini
        window_group: gemini
        command: "gemini -y --resume"
      - name: shell
        window_group: shell
        # no command = opens a plain shell

  # ── Single-window utility session ─────────────────────────────────────────
  - name: monitoring
    session_group: system
    working_dir: ~
    command: "htop"
```

---

## Full Config Reference

| Field | Level | Description |
|---|---|---|
| `name` | session | Required. Must be unique. |
| `session_group` | session | Optional. String or list. Used with `--session-group` — targets the whole session. A session can belong to multiple groups. |
| `working_dir` | session / window | Starting directory. Window value overrides session. |
| `focus` | session | Window name to select after creation. |
| `pre_hook` | session | Shell command run before session is created. |
| `pre_hook_fail` | session | `warn` (default) or `abort` — whether a failed pre_hook stops session creation. |
| `post_hook` | session | Shell command run after session is created. |
| `env` | session / window | Map of env vars. Window env sent as `export` statements. |
| `command` | session / window | Program to run. On session level, creates a single-window session. |
| `windows` | session | List of windows. Overrides session-level `command`. |
| `window_group` | window | Optional. String or list. Used with `--window-group` — only matching windows are created. A window can belong to multiple groups. |
| `panes` | window | List of panes to split the window into. Each can have `command` and `working_dir`. |
| `layout` | window | Pane layout: `tiled`, `even-horizontal`, `even-vertical`, `main-horizontal`, `main-vertical`. |
