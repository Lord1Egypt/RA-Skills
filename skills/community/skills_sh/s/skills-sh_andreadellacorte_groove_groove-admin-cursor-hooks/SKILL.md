---
name: groove-admin-cursor-hooks
description: "Install groove's Cursor native hooks into .cursor/hooks.json. Enables compaction-safe re-priming, session-end reminders, git activity capture, automatic session-capture drafts, and managed-path protection."
license: MIT
allowed-tools: Read Write Edit Glob Bash(git:*) Bash(mkdir:*) Bash(chmod:*) Bash(python3:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

<!-- groove:managed — do not edit; changes will be overwritten by groove update -->

# groove-admin-cursor-hooks

Install groove's Cursor native hooks. These run outside the model — deterministic, unconditional — and complement groove's advisory markdown hooks (`.groove/hooks/start.md`, `end.md`).

Use `--disable <hook>` to remove a specific hook. Use `--list` to show current status.

## Outcome

Selected hooks are registered in `.cursor/hooks.json` and shell scripts are written to `.groove/hooks/cursor/`. Hooks fire automatically on Cursor lifecycle events without any model involvement.

## Available hooks

| Name | Event | Matcher | What it does |
|---|---|---|---|
| `context-reprime` | `sessionStart` | — | Runs the prime script with `--json` — ensures full workflow context is loaded after every session start and compaction |
| `daily-end-reminder` | `stop` | — | If hour is 16–21 local time and `.groove/index.md` exists, prints a reminder to run `/groove-daily-end` |
| `git-activity-buffer` | `postToolUse` | `Shell` | If the command contains `git commit`, appends a timestamped line to `.groove/.cache/git-activity-buffer.txt` |
| `block-managed-paths` | `preToolUse` | `Write` | If `file_path` starts with `.agents/skills/groove` or `skills/groove`, exits with code 2 to block the write with an explanatory message |
| `version-check` | `postToolUse` | — | Checks for a new groove version once per hour; calls `groove-utilities-check` |
| `session-capture` | `stop` | — | If there is git activity this session (commits since midnight, working changes, or buffered commits), stages a capture draft to `.groove/.cache/pending-capture.md` for next-session review. Silent. |

## Steps

### `--list`

Read `.cursor/hooks.json` if it exists. Report which groove hooks are registered and which scripts exist in `.groove/hooks/cursor/`. Exit.

### `--disable <hook>`

Remove the named hook's entry from `.cursor/hooks.json` (leave the script in place). Report removed / not found. Exit.

### Default (install)

1. Ask which hooks to enable (default: all six):
   ```
   Which hooks to install? (all / comma-separated: context-reprime, daily-end-reminder, git-activity-buffer, block-managed-paths, version-check, session-capture)
   Press enter for all.
   ```

2. Read `.cursor/hooks.json` if it exists; parse as JSON (default `{"version": 1, "hooks": {}}`). Never discard existing non-groove entries.

3. Create `.groove/hooks/cursor/` directory if absent. Make each script executable (`chmod +x`).

4. For each selected hook: write the shell script and merge the hook entry into `.cursor/hooks.json`.

5. Write `.cursor/hooks.json` with the merged result.

6. Report summary:
   ```
   ✓ context-reprime     — sessionStart hook → groove-utilities-prime.sh --json
   ✓ daily-end-reminder  — stop hook → .groove/hooks/cursor/daily-end-reminder.sh
   ✓ git-activity-buffer — postToolUse/Shell hook → .groove/hooks/cursor/git-activity-buffer.sh
   ✓ block-managed-paths — preToolUse/Write hook → .groove/hooks/cursor/block-managed-paths.sh
   ✓ version-check       — postToolUse hook → .groove/hooks/cursor/version-check.sh
   ✓ session-capture     — stop hook → .groove/hooks/cursor/session-capture.sh
   ✓ .cursor/hooks.json updated
   ```

## Shell script templates

Write these verbatim to `.groove/hooks/cursor/`. Never overwrite an existing script without showing a diff and confirming.

### `daily-end-reminder.sh`

```bash
#!/usr/bin/env bash
# groove: stop hook — remind about /groove-daily-end during work hours
hour=$(date +%H)
if [ -f "$CLAUDE_PROJECT_DIR/.groove/index.md" ] && [ "$hour" -ge 16 ] && [ "$hour" -le 21 ]; then
  echo "groove: end of work hours — consider running /groove-daily-end"
fi
```

### `git-activity-buffer.sh`

```bash
#!/usr/bin/env bash
# groove: postToolUse/Shell hook — buffer git commits for memory log
input=$(cat)
command=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null)
if echo "$command" | grep -q "git commit"; then
  msg=$(echo "$command" | grep -oP '(?<=-m ")[^"]+' | head -1)
  mkdir -p "$CLAUDE_PROJECT_DIR/.groove/.cache"
  echo "$(date '+%Y-%m-%d %H:%M') | ${msg:-<no message>}" >> "$CLAUDE_PROJECT_DIR/.groove/.cache/git-activity-buffer.txt"
fi
```

### `block-managed-paths.sh`

```bash
#!/usr/bin/env bash
# groove: preToolUse/Write hook — block edits to managed groove paths
input=$(cat)
path=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)
if echo "$path" | grep -qE '^(\.agents/skills/groove|skills/groove)'; then
  echo "groove: blocked — '$path' is managed by groove update. Edit under skills/ and rsync to .agents/skills/." >&2
  exit 2
fi
```

### `version-check.sh`

```bash
#!/usr/bin/env bash
# groove: postToolUse hook — check for new groove version (once per hour)
CACHE="$CLAUDE_PROJECT_DIR/.groove/.cache/last-version-check-ts"
mkdir -p "$CLAUDE_PROJECT_DIR/.groove/.cache"
now=$(date +%s)
if [ -f "$CACHE" ]; then
  last=$(cat "$CACHE")
  diff=$((now - last))
  [ "$diff" -lt 3600 ] && exit 0
fi
echo "$now" > "$CACHE"
bash "$CLAUDE_PROJECT_DIR/.agents/skills/groove-utilities-check/scripts/check.sh" 2>/dev/null || true
```

### `session-capture.sh`

```bash
#!/usr/bin/env bash
# groove: stop hook — stage a session capture draft from git activity for next-session review
ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
[ -f "$ROOT/.groove/index.md" ] || exit 0
command -v git >/dev/null 2>&1 || exit 0
git -C "$ROOT" rev-parse --git-dir >/dev/null 2>&1 || exit 0

CACHE="$ROOT/.groove/.cache"
PENDING="$CACHE/pending-capture.md"
BUFFER="$CACHE/git-activity-buffer.txt"

commits=$(git -C "$ROOT" log --since=midnight --oneline 2>/dev/null)
changes=$(git -C "$ROOT" diff --stat HEAD 2>/dev/null)
buffered=""
[ -s "$BUFFER" ] && buffered=$(cat "$BUFFER")

# No activity → clear any stale draft and stay silent.
if [ -z "$commits" ] && [ -z "$changes" ] && [ -z "$buffered" ]; then
  rm -f "$PENDING"
  exit 0
fi

mkdir -p "$CACHE"
{
  echo "# Pending capture — $(date '+%Y-%m-%d %H:%M')"
  echo
  echo "## Commits since midnight"
  echo "${commits:-(none)}"
  echo
  echo "## Working changes"
  echo "${changes:-(none)}"
  if [ -n "$buffered" ]; then
    echo
    echo "## Buffered commit messages"
    echo "$buffered"
  fi
} > "$PENDING"
```

## `.cursor/hooks.json` template

Merge these into the `hooks` key. Preserve all other keys.

```json
{
  "version": 1,
  "hooks": {
    "sessionStart": [
      {
        "command": "bash $CLAUDE_PROJECT_DIR/.agents/skills/groove-utilities-prime/scripts/groove-utilities-prime.sh --json"
      }
    ],
    "stop": [
      {
        "command": "bash $CLAUDE_PROJECT_DIR/.groove/hooks/cursor/daily-end-reminder.sh"
      },
      {
        "command": "bash $CLAUDE_PROJECT_DIR/.groove/hooks/cursor/session-capture.sh"
      }
    ],
    "postToolUse": [
      {
        "matcher": "Shell",
        "command": "bash $CLAUDE_PROJECT_DIR/.groove/hooks/cursor/git-activity-buffer.sh"
      },
      {
        "command": "bash $CLAUDE_PROJECT_DIR/.groove/hooks/cursor/version-check.sh"
      }
    ],
    "preToolUse": [
      {
        "matcher": "Write",
        "command": "bash $CLAUDE_PROJECT_DIR/.groove/hooks/cursor/block-managed-paths.sh"
      }
    ]
  }
}
```

When merging: if a `hooks` key already exists, append groove entries to the relevant event arrays. Do not create duplicates — check if a groove command entry already exists before appending.

## Constraints

- Never overwrite non-groove entries in `.cursor/hooks.json`
- Never overwrite an existing script without diff + confirmation
- Scripts use `python3` to parse JSON stdin — if python3 is absent, skip that hook and warn
- `block-managed-paths` uses exit code 2 (Cursor's convention to block the tool use)
- After install: remind the user that hooks take effect on the next Cursor session restart
- `.groove/hooks/cursor/` follows the `git.hooks` git strategy from `.groove/index.md`
- Create `.cursor/` directory if it does not exist
