---
name: archive
description: Fills Outcomes & Learnings in a plan file and renames it to .done.md.
---

## Inputs

- `WORKTREE`: absolute path to current worktree (resolve from session CWD or `git rev-parse --show-toplevel`)
- Plan file path (default: most recent non-`.done.md` in `$WORKTREE/ai-workspace/plans/`)

## Steps

1. **Find the plan file**:
   ```bash
   ls -t "$WORKTREE/ai-workspace/plans/"*.md | grep -v '.done.md' | head -1
   ```
   If plan is already `.done.md` → error: "Already archived."

2. **Read the plan file** to understand what was planned.

3. **Gather outcomes**: Ask the user (or infer from git log + branch context):
   - What worked well?
   - What didn't go as planned?
   - What would you do differently?

   If user skips → write "Outcomes: not recorded" (don't block).

4. **Write Outcomes & Learnings section** to the plan file:
   ```markdown
   ## Outcomes & Learnings

   **Completed**: [date]

   ### What Worked
   - [bullet points]

   ### What Didn't
   - [bullet points]

   ### Learnings
   - [bullet points]
   ```

5. **Rename to .done.md**:
   ```bash
   git -C "$WORKTREE" mv ai-workspace/plans/<name>.md ai-workspace/plans/<name>.done.md
   ```

6. **Commit the archive**:
   ```bash
   git -C "$WORKTREE" add ai-workspace/plans/<name>.done.md
   git -C "$WORKTREE" commit -m "docs: archive plan <name>

   Co-Authored-By: Claude <model>"
   ```

Output: Confirmation that the plan is archived with path to `.done.md` file.
