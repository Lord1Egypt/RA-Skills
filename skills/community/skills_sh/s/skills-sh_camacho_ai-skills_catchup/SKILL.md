---
name: catchup
description: "Use after /clear, /compact, session resume, or context loss. Use when branch context is stale or unknown. Use when starting work in an existing worktree."
---

# Catchup — Context Reconstruction

**This skill is strictly read-only. Do NOT edit files, create branches, or run write commands.**

## 1. Gather data (run all independent steps in parallel)

- `git log --format="%h %s (%ar)" -20`, `git status`, and `git worktree list`
- Read `.branch-context.md` (if exists — check CWD and worktree root). Parse YAML frontmatter: `workflow_step`, `validate_round`/`validate_max`, `review_round`/`review_max`, `plan_review_chunk`/`plan_review_total`/`plan_chunks_approved`
- Read `ai-workspace/MEMORY.md` — note anything in-progress or blocking
- Read `HANDOFF.md` (if exists)
- List `ai-workspace/plans/` (sort by mtime, most recent first) and read the first file that does NOT end in `.done.md` or `.executed.md`
- Search Basic Memory via MCP for recent entries matching the current branch name. If MCP unavailable, skip silently.
- **GitHub** — check availability first:
  ```bash
  command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1
  ```
  If authenticated, run in parallel:
  ```bash
  gh pr list --state open
  gh issue list --state open --limit 15
  ```
  If `gh` is unavailable or unauthenticated, note "GitHub CLI unavailable" and skip. Do NOT attempt to install or authenticate.

## 2. Synthesize

Present findings in this format. **Omit sections where the data source was not found** (e.g., no HANDOFF.md, gh unavailable). Always show Loop state and Blockers even when empty — absence is informative:

```
Branch:         <name> — <what we're building (from plan or branch-context)>
Worktree:       <path> (or "primary")
Last commit:    <hash> <message>
Uncommitted:    <staged/unstaged summary, or "clean">
Workflow step:  <N> — <step name> (from frontmatter, or inferred)
Loop state:     validate <round>/<max>, review <round>/<max>
Active plan:    <file> — <current phase> — <next action>
Blockers:       <list>
Open PRs:       <count — titles>
Open issues:    <count — top 5 titles>
Handoff:        <detail>
```

After the summary, **surface blockers and TODO items prominently** — remaining work, failing CI, stale branches, items from memory flagged as blocking. These go above the fold, not as footnotes.

## 3. Suggest next actions

Based on gathered state, suggest 2-3 concrete next actions. Examples:
- "Resume building — plan X is at step 5 (Build)"
- "Run /validate — implementation looks complete"
- "Address blocker: [description]"
- "Review open PR #N — awaiting action"
- "Pick up issue #N — in-progress"

End with: "What would you like to do?"

## Failure modes

- **No `.branch-context.md`**: infer workflow step from git state and plan file status. Note: "No branch context — step inferred."
- **No active plan**: note "No active plan." Do not search `.done.md` files.
- **On `main` branch**: skip branch-context and plan lookup. Show git state, PRs, issues, and memory only.
- **Basic Memory MCP unavailable**: skip silently.
- **`gh` unavailable**: show "GitHub CLI unavailable — PR/issue status unknown."
