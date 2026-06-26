---
name: bail
description: Reflects, updates GitHub Issue, closes PR if open, cleans up worktree/branch.
---

Bail-out protocol: always reflect FIRST, then clean up. All commands use absolute paths and `git -C`.

## Inputs

- `WORKTREE`: absolute path to current worktree (or primary if no worktree)
- Optional reason string (if not provided, ask for one)

## Steps

1. **Detect current step** by examining what exists:

   | What exists | Estimated step |
   |------------|---------------|
   | Just an issue, no branch | Step 0 (Capture) |
   | .branch-context.md, no worktree | Step 1 (Orient) |
   | Worktree exists, no code changes | Step 2 (Isolate) |
   | Plan file on branch | Step 3-4 (Design/Review) |
   | Code changes committed | Step 5-7 (Build/Verify/Archive) |
   | PR open on GitHub | Step 8 (Ship) |

2. **Prompt for reason** if not provided.

3. **Write learnings to .branch-context.md** in the worktree:

   ```bash
   # Write bail context — use absolute path
   cat >> "$WORKTREE/.branch-context.md" <<EOF

   ## Bail
   - Reason: <reason>
   - What was attempted: <summary>
   - What was learned: <learnings>
   EOF
   git -C "$WORKTREE" add .branch-context.md
   git -C "$WORKTREE" commit -m "docs: capture bail context"
   ```

4. **Consolidate learnings to MEMORY.md** via disposable clone (never checkout main in a worktree):

   ```bash
   BAIL_DIR="${CLAUDE_SESSION_DIR:-$TMPDIR}/bail-reflect"
   [ -d "$BAIL_DIR" ] && rm -rf "$BAIL_DIR"
   git clone --depth 50 "$(git -C "$WORKTREE" remote get-url origin)" "$BAIL_DIR"
   ```

   Read `$BAIL_DIR/ai-workspace/MEMORY.md`, append relevant learnings from `.branch-context.md`, then:

   ```bash
   git -C "$BAIL_DIR" add ai-workspace/MEMORY.md
   git -C "$BAIL_DIR" commit -m "docs: consolidate learnings from abandoned <branch>

   Co-Authored-By: Claude <model>"
   git -C "$BAIL_DIR" push
   ```

   On non-fast-forward: `git -C "$BAIL_DIR" pull --rebase` then push. Max 3 retries.
   Clean up: `rm -rf "$BAIL_DIR"`

5. **Update GitHub Issue** (if accessible):

   ```bash
   GH_REPO=<owner/repo> gh issue comment <number> --body "Bailing: <reason>. Learnings captured in MEMORY.md."
   GH_REPO=<owner/repo> gh issue edit <number> --add-label "deferred" --remove-label "triage"
   ```

6. **Close PR if open**:

   ```bash
   PR_NUM=$(GH_REPO=<owner/repo> gh pr list --head "<branch>" --json number -q '.[0].number')
   if [ -n "$PR_NUM" ]; then
     GH_REPO=<owner/repo> gh pr close "$PR_NUM"
   fi
   ```

7. **Ask about branch preservation**:

   Default: preserve the branch (user can resume later).

   If user explicitly says delete — confirm by showing what will be destroyed:
   ```
   This will delete:
   - Branch: <name>
   - Worktree: <path>
   - Remote branch (if pushed)

   Type 'delete' to confirm.
   ```

   Only after typed confirmation:
   ```bash
   PRIMARY="$(git -C "$WORKTREE" worktree list --porcelain | grep -m1 '^worktree ' | sed 's/^worktree //')"
   # Verify branch is merged before deleting (-d fails if unmerged, -D would force)
   git -C "$PRIMARY" worktree remove "$WORKTREE"
   git -C "$PRIMARY" branch -d <branch>
   ```

   If `branch -d` fails (unmerged work), warn the user and stop. Do NOT use `branch -D`.

8. **Done.** Do not checkout main — stay in whatever CWD the session has.

## Edge Cases

- No worktree exists (bailing at Step 0-1) → skip worktree cleanup, just update issue
- No GitHub access → skip issue update, still do local cleanup + memory consolidation
- PR already merged → don't close, just note it in the output
- No .branch-context.md → create one with just the bail reason before consolidating
- `CLAUDE_SESSION_DIR` unset → fall back to `$TMPDIR` for clone

Output: Summary of what was cleaned up and where learnings were saved.
