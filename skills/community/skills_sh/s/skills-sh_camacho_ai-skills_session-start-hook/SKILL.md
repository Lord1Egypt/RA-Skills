---
name: session-start-hook
description: Creating and developing startup hooks for Claude Code. Use when the user wants to set up a repository for Claude Code, create a SessionStart hook to ensure their project can run tests and linters during sessions (CLI, web, or API).
---

# Startup Hook Skill for Claude Code

Create SessionStart hooks that install dependencies so tests and linters work in Claude Code sessions (CLI, web, or API).

## Hook Basics

### Input (via stdin)
```json
{
  "session_id": "abc123",
  "source": "startup|resume|clear|compact",
  "transcript_path": "/path/to/transcript.jsonl",
  "permission_mode": "default",
  "hook_event_name": "SessionStart",
  "cwd": "/workspace/repo"
}
```

### Async Mode
```bash
#!/bin/bash
set -euo pipefail

echo '{"async": true, "asyncTimeout": 300000}'

npm install
```

The hook runs in background while the session starts. Using async mode reduces latency, but introduces a race condition where the agent loop might depend on something that is being done in the startup hook before it completed.

### Environment Variables

Available environment variables:
- `$CLAUDE_PROJECT_DIR` - Repository root path
- `$CLAUDE_ENV_FILE` - Path to write environment variables
- `$CLAUDE_CODE_REMOTE` - If running in a remote environment (i.e. Claude code on the web)

Use `$CLAUDE_ENV_FILE` to persist variables for the session:
```bash
echo 'export PYTHONPATH="."' >> "$CLAUDE_ENV_FILE"
```

Use `$CLAUDE_CODE_REMOTE` to only run a script in a remote env:
```bash
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi
```

## Workflow

Make a todo list for all the tasks in this workflow and work on them one after another

### 1. Analyze Dependencies

Find dependency manifests and analyze them. Examples:
- `package.json` / `package-lock.json` → npm
- `pyproject.toml` / `requirements.txt` → pip/Poetry
- `Cargo.toml` → cargo
- `go.mod` → go
- `Gemfile` → bundler

Additionally, read though any documentation (i.e. README.md or similar) to see if you can get additional context on how the environment setup works

### 2. Design Hook

Create a script that installs dependencies.

**Key principles:**
- Don't use async mode in the first iteration. Only switch to it if the user asks for it
- Write the hook only for the web unless user asks otherwise (see $CLAUDE_CODE_REMOTE)
- The container state gets cached after the hook completes, prefer dependency install methods that take advantage of that (i.e. prefer npm install over npm ci)
- Be idempotent (safe to run multiple times)
- Non-interactive (no user input)

**What NOT to put in a SessionStart hook:**
- Do NOT copy skills between user scope (`~/.claude/skills/`) and project scope (`.claude/skills/`) — that's what `./dotfiles/sync.sh` is for.

**Skills freshness check (install if missing or outdated):**
```bash
SKILLS_DIR="$HOME/.claude/skills"
REPO_SKILLS_DIR="${CLAUDE_PROJECT_DIR}/dotfiles/claude/skills"
SKILLS_REPO="${AI_SKILLS_REPO:-camacho/ai-skills}"

skills_stale() {
  [[ ! -d "$SKILLS_DIR" ]] && return 0   # missing → stale
  if [[ -d "$REPO_SKILLS_DIR" ]]; then
    # Compare repo snapshot to installed — if different, stale
    ! diff -rq "$REPO_SKILLS_DIR" "$SKILLS_DIR" >/dev/null 2>&1 && return 0
  fi
  return 1  # up to date
}

if skills_stale; then
  echo "Skills missing or outdated — installing from $SKILLS_REPO..."
  if command -v npx &>/dev/null; then
    npx skills install "$SKILLS_REPO" --scope personal \
      || echo "Warning: skills install failed — project-scope skills still available" >&2
  else
    echo '{"message": "Skills are outdated but npx not found.\n\nRun: ./dotfiles/sync.sh push", "continue": true}'
  fi
fi
```

The check is local (fast `diff`) — network only when stale. The default repo (`camacho/ai-skills`) can be overridden with `AI_SKILLS_REPO`.

**Dotfiles-missing check (surface as a session prompt, not a stderr warning):**
```bash
# Surface a visible prompt if user dotfiles are missing — informational only
if [[ ! -d "$HOME/.claude/skills" ]]; then
  echo '{"message": "~/.claude/skills not found.\n\nRun: ./dotfiles/sync.sh push\n\nThis sets up user-level skills and configs from the dotfiles repo.", "continue": true}'
  exit 0
fi
```

Using the hook's JSON `message` field (instead of stderr) surfaces this inside Claude's session context where the user will see and act on it. `"continue": true` keeps the session running — this is informational, not a blocker.

### 3. Create Hook File

```bash
mkdir -p .claude/hooks
cat > .claude/hooks/session-start.sh << 'EOF'
#!/bin/bash
set -euo pipefail

echo '{"async": true, "asyncTimeout": 300000}'
# Install dependencies here
EOF

chmod +x .claude/hooks/session-start.sh
```

### 4. Register in Settings

Add to `.claude/settings.json` (create if doesn't exist):
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh"
          }
        ]
      }
    ]
  }
}
```

If `.claude/settings.json` exists, merge the hooks configuration.

### 5. Validate Hook

Run the hook script directly:

```bash
CLAUDE_CODE_REMOTE=true ./.claude/hooks/session-start.sh
```

IMPORTANT: Verify dependencies are installed and script completes successfully.

### 6. Validate Linter

IMPORTANT: Figure out what the right command is to run the linters and run it for an example file. No need to lint the whole project. If there are any issues, update the startup script accordingly and re-test.

### 7. Validate Test

IMPORTANT: Figure out what the right command is to run the tests and run it for one test. No need to run the whole test suite. If there are any issues, update the startup script accordingly and re-test.

### 8. Commit and push

Make a commit and push it to the remote branch

## Wrap up

We're all done. In your last message to the user, Provide a detailed summary to the user with the format below:

* Summary of the changes made
* Validation results
  1. Session hook execution (include details if it failed)
  2. linter execution (include details if it failed)
  3. test execution (include details if it failed)
* Hook execution mode: Syncronous
  * inform user that hook is running syncronous and the below trade-offs. Let them know that we can change it to async if they prefer faster session startup.
    * Pros: Guarantees dependencies are installed before your session starts, preventing race conditions where Claude might try to run tests or linters before they're ready
    * Cons: Your remote session will only start once the session start hook is completed
* inform user that once they merge the session start hook into their repo's default branch, all future sessions will use it.
