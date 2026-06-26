---
name: coding-agent
description: 'Delegate coding tasks to Codex, Claude Code, or Pi agents via background process. Use when: (1) building/creating new features or apps, (2) reviewing PRs (spawn in temp dir), (3) refactoring large codebases, (4) iterative coding that needs file exploration. NOT for: simple one-liner fixes (just edit), reading code (use read tool), thread-bound ACP harness requests in chat (use sessions_spawn with runtime:"acp"), or any work in the OpenClaw workspace (never spawn agents here). Claude Code: use --print --permission-mode bypassPermissions (no PTY). Codex/Pi/OpenCode: pty:true required.'
---

# Coding Agent

Use **bash** (with optional background mode) for all coding agent work.

## PTY: Codex/Pi/OpenCode yes, Claude Code no

For **Codex, Pi, and OpenCode**, PTY is required (interactive terminal apps):

```bash
# Codex/Pi/OpenCode
bash pty:true command:"codex exec 'Your prompt'"
```

For **Claude Code** (`claude` CLI), use `--print --permission-mode bypassPermissions` instead.
`--print` mode keeps full tool access and avoids interactive confirmation:

```bash
# Claude Code (no PTY needed)
cd /path/to/project && claude --permission-mode bypassPermissions --print 'Your task'

# Background execution: use background:true on the exec tool
```

### Bash Tool Parameters

| Parameter    | Type    | Description                                                                 |
| ------------ | ------- | --------------------------------------------------------------------------- |
| `command`    | string  | The shell command to run                                                    |
| `pty`        | boolean | Allocates a pseudo-terminal for interactive CLIs (required for Codex/Pi)    |
| `workdir`    | string  | Working directory (agent sees only this folder's context)                   |
| `background` | boolean | Run in background, returns sessionId for monitoring                         |
| `timeout`    | number  | Timeout in seconds (kills process on expiry)                                |
| `elevated`   | boolean | Run on host instead of sandbox (if allowed)                                 |

### Process Tool Actions

| Action      | Description                                          |
| ----------- | ---------------------------------------------------- |
| `list`      | List all running/recent sessions                     |
| `poll`      | Check if session is still running                    |
| `log`       | Get session output (with optional offset/limit)      |
| `write`     | Send raw data to stdin                               |
| `submit`    | Send data + newline (like typing and pressing Enter) |
| `send-keys` | Send key tokens or hex bytes                         |
| `paste`     | Paste text (with optional bracketed mode)            |
| `kill`      | Terminate the session                                |

---

## Quick Start: One-Shot Tasks

```bash
# Quick chat (Codex needs a git repo!)
SCRATCH=$(mktemp -d) && cd $SCRATCH && git init && codex exec "Your prompt here"

# In a real project
bash pty:true workdir:~/Projects/myproject command:"codex exec 'Add error handling to the API calls'"
```

**Why git init?** Codex refuses to run outside a trusted git directory. A temp repo solves this for scratch work.

---

## The Pattern: workdir + background + pty

For longer tasks, use background mode:

```bash
# Start agent in target directory
bash pty:true workdir:~/project background:true command:"codex exec --full-auto 'Build a snake game'"
# Returns sessionId for tracking

# Monitor progress
process action:log sessionId:XXX

# Check if done
process action:poll sessionId:XXX

# Send input (if agent asks a question)
process action:submit sessionId:XXX data:"yes"

# Kill if needed
process action:kill sessionId:XXX
```

**Why workdir matters:** Agent wakes up in a focused directory and doesn't wander off reading unrelated files.

---

## Codex CLI

Preferred agent for single tasks. Pass the requirements clearly — Codex handles execution well.

### Flags

| Flag            | Effect                                             |
| --------------- | -------------------------------------------------- |
| `exec "prompt"` | One-shot execution, exits when done                |
| `--full-auto`   | Sandboxed but auto-approves in workspace           |
| `--yolo`        | No sandbox, no approvals (fastest, most dangerous) |

### Building/Creating

```bash
# Quick one-shot
bash pty:true workdir:~/project command:"codex exec --full-auto 'Build a dark mode toggle'"

# Background for longer work
bash pty:true workdir:~/project background:true command:"codex --yolo 'Refactor the auth module'"
```

### Reviewing PRs

**Never review PRs in the OpenClaw workspace or the live project folder.** Clone to temp or use git worktree.

```bash
# Clone to temp for safe review
REVIEW_DIR=$(mktemp -d)
git clone https://github.com/user/repo.git $REVIEW_DIR
cd $REVIEW_DIR && gh pr checkout 130
bash pty:true workdir:$REVIEW_DIR command:"codex review --base origin/main"
# Clean up after: trash $REVIEW_DIR

# Or use git worktree (keeps main intact)
git worktree add /tmp/pr-130-review pr-130-branch
bash pty:true workdir:/tmp/pr-130-review command:"codex review --base main"
```

### Batch PR Reviews (parallel)

```bash
# Fetch all PR refs
git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'

# One Codex per PR
bash pty:true workdir:~/project background:true command:"codex exec 'Review PR #86. git diff origin/main...origin/pr/86'"
bash pty:true workdir:~/project background:true command:"codex exec 'Review PR #87. git diff origin/main...origin/pr/87'"

# Monitor all
process action:list

# Post results
gh pr comment <PR#> --body "<review content>"
```

---

## OpenCode

```bash
bash pty:true workdir:~/project command:"opencode run 'Your task'"
```

---

## Claude Code

No PTY required. Use when explicitly requested or for tasks that benefit from tighter integration.

```bash
# Foreground
bash workdir:~/project command:"claude --permission-mode bypassPermissions --print 'Your task'"

# Background
bash workdir:~/project background:true command:"claude --permission-mode bypassPermissions --print 'Your task'"
```

---

## Pi

```bash
bash pty:true workdir:~/project command:"pi 'Your task'"

# Non-interactive mode
bash pty:true command:"pi -p 'Summarize src/'"

# Different provider/model
bash pty:true command:"pi --provider openai --model gpt-4o-mini -p 'Your task'"
```

---

## Parallel Issue Fixing with git worktrees

```bash
# Create worktrees for each issue
git worktree add -b fix/issue-78 /tmp/issue-78 main
git worktree add -b fix/issue-99 /tmp/issue-99 main

# Launch agents in parallel
bash pty:true workdir:/tmp/issue-78 background:true command:"pnpm install && codex --yolo 'Fix issue #78: <description>. Commit and push.'"
bash pty:true workdir:/tmp/issue-99 background:true command:"pnpm install && codex --yolo 'Fix issue #99. Implement only the in-scope edits and commit after review.'"

# Monitor
process action:list
process action:log sessionId:XXX

# Create PRs
cd /tmp/issue-78 && git push -u origin fix/issue-78
gh pr create --repo user/repo --head fix/issue-78 --title "fix: ..." --body "..."

# Cleanup
git worktree remove /tmp/issue-78
git worktree remove /tmp/issue-99
```

---

## Rules

1. **Right execution mode per agent**: Claude Code uses `--print --permission-mode bypassPermissions` (no PTY); Codex/Pi/OpenCode use `pty:true`
2. **Respect tool choice** — if the user asks for a specific agent, use it; don't silently substitute
3. **Orchestrator mode** — do not hand-code patches yourself when the task is delegated to an agent
4. **Be patient** — don't kill sessions just because they're slow; check with `process:log` first
5. **Parallel is fine** — run multiple agents at once for batch work
6. **Never start agents in the OpenClaw workspace** — they'll read soul docs and get confused about who's in charge
7. **Never checkout branches in the live OpenClaw project folder** — that's the running instance

---

## Progress Updates

Keep the user in the loop without flooding them.

- One short message when you start: what's running and where
- Update again only when something changes: milestone done, agent needs input, error, or finished
- If you kill a session, say so immediately and explain why

---

## Auto-Notify on Completion

For long-running background tasks, append a wake trigger to the prompt so Miki gets notified immediately when the agent finishes:

```
... your task here.

When completely finished, run:
openclaw system event --text "Done: [brief summary]" --mode now
```

**Example:**

```bash
bash pty:true workdir:~/project background:true command:"codex --yolo exec 'Build a REST API for todos.

When completely finished, run: openclaw system event --text \"Done: Built todos REST API\" --mode now'"
```

---

## Notes

- **PTY is essential for Codex/Pi/OpenCode** — without it, output breaks or the agent hangs
- **Git repo required for Codex** — use `mktemp -d && git init` for scratch work
- **`exec` is clean** — `codex exec "prompt"` runs and exits, perfect for one-shots
- **`submit` vs `write`** — `submit` sends input + Enter; `write` sends raw data without newline
