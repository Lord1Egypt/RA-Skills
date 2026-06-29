# Pre-flight checks (3 tips)

A few minutes of prep now saves a lot of pain later.

## Tip 1 — Version control your workspace

**Why**: As you build a skill, the AI will read and write many files. Without
version control, one bad edit can be hard to undo.

**How**: Make sure your workspace (or the directory where you're building) is
a Git repo. If not, run `git init` and make an initial commit before starting.
A simple `.gitignore` for typical noise (`.DS_Store`, `*.log`, `node_modules/`,
`__pycache__/`, `.skill-data/`) is enough to start.

**Verify**: `git status` works and reports a clean tree.

---

## Tip 2 — Long-running task tolerance

**Why**: Building a non-trivial skill (multiple files, multiple scripts) often
needs the agent to keep working for several minutes per turn. If your runtime
times out aggressively, you'll lose progress mid-build.

**How**: Make sure your agent/IDE can run long tasks. Typical knobs:
- A "subagent timeout" or "tool timeout" setting (raise to ≥ 5 minutes if you
  see truncated runs)
- A "max output tokens" cap (raise if responses get cut off)
- Background execution support (so a slow step doesn't block UX)

This is highly platform-specific; consult your agent's docs.

---

## Tip 3 — Cross-session continuity

**Why**: Skill development often spans multiple conversation turns. If the
session is dropped or you have to restart, you don't want to lose the design
context and progress notes.

**How**: Use whatever recovery story your agent provides:
- Save the design (Stage 2) to a persistent file (`DESIGN.md`, team wiki,
  Notion, etc.) so you can re-load it
- Make sure your agent supports conversation history export / resume
- Commit work-in-progress frequently to Git (covers both "lost session" and
  "bad edit")
