---
name: reflect
description: Use after merging a branch or completing a task to consolidate learnings into memory layers, close out issues, and verify the phase gate.
---

Phase gate: COMMIT checkpoint. Do not declare task complete until Step 8 passes.

Execute all steps in order. Escalate to the user only at explicit escalation points.

## Step 0 — Mark reflect timestamp

```bash
date +%s > "${CLAUDE_PROJECT_DIR}/ai-workspace/.last-reflect-ts"
```

## Step 1 — Review session work

```bash
git log --oneline -10
```

Review recent edits and corrections made during this session. If a completed plan exists in `ai-workspace/plans/` (Outcomes & Learnings filled in), use it as the primary source. Otherwise derive learnings directly from git history and session events. Build an explicit inventory of candidate learnings before moving on.

## Step 1b — Verify issue closure

Scan commit messages for closing keywords (case-insensitive): `closes`, `close`, `closed`, `fixes`, `fix`, `fixed`, `resolves`, `resolve`, `resolved` followed by `#N`.

For each issue number found:

```bash
gh issue view N --json state --jq '.state'
```

Warn if any referenced issue is still open. Do not block — warn and continue.

## Step 2 — Classify learnings

| Signal | Destination |
|---|---|
| References this repo's files, paths, configs, or project conventions | MEMORY.md only |
| General pattern, tool behavior, or preference applicable across projects | Basic Memory vault only |
| Both (project-specific instance of a cross-project pattern) | Both — cross-reference each entry to the other |

## Step 2b — Comment learnings on related issues

**Plan has `Issue: #N` in frontmatter**: post learnings directly as a comment on that issue. No confirmation needed — the link is explicit.

**No plan or no Issue field**: run `gh issue list --state open --json number,title,labels --limit 50`, fuzzy-match keywords against open issue titles. Confirm with user before posting to any fuzzy match. A bad auto-comment is worse than a missed one.

## Step 3 — Write to MEMORY.md (concurrent write protocol)

MEMORY.md lives on main and may receive concurrent writes. Never write from the current worktree.

```bash
REFLECT_DIR="${CLAUDE_SESSION_DIR:-$TMPDIR}/memory-reflect"
[ -d "$REFLECT_DIR" ] && rm -rf "$REFLECT_DIR"
git clone --depth 50 "$(git remote get-url origin)" "$REFLECT_DIR"
```

Retry loop (max 3 attempts):

1. Read `$REFLECT_DIR/ai-workspace/MEMORY.md` as it exists now.
2. Re-derive entries from the current file state — skip anything already present, avoid duplicates. Do not auto-merge. Do not replay old diffs.
3. Add new entries. Prune entries older than 30 days. Keep under 200 lines — if over, summarize the oldest section (never silently delete).
4. Commit and push:

```bash
git -C "$REFLECT_DIR" add ai-workspace/MEMORY.md
git -C "$REFLECT_DIR" commit -m "reflect: update MEMORY.md [$(date +%Y-%m-%d)]

Co-Authored-By: Claude <model>"
git -C "$REFLECT_DIR" push
```

5. On non-fast-forward rejection: `git -C "$REFLECT_DIR" pull --rebase`, return to step 1.
6. After 3 failures, stop and escalate — do not proceed:
   > MEMORY.md write failed after 3 retries. Manual merge required at `$REFLECT_DIR/ai-workspace/MEMORY.md`.

### Propagate to primary worktree

After successful push, bring the primary worktree's main up to date so other agents see the new MEMORY.md immediately:

```bash
PRIMARY="$(git worktree list --porcelain | grep -m1 '^worktree ' | sed 's/^worktree //')"
CURRENT=$(git -C "$PRIMARY" branch --show-current)
if [ "$CURRENT" = "main" ]; then
  # WIP commit if dirty
  if [ -n "$(git -C "$PRIMARY" status --porcelain)" ]; then
    git -C "$PRIMARY" add -u
    git -C "$PRIMARY" commit -m "wip: preserve local state before reflect sync"
    WIP=1
  fi
  git -C "$PRIMARY" fetch origin main
  git -C "$PRIMARY" merge --ff-only origin/main || echo "Primary diverged — manual pull needed"
  # Restore WIP
  [ "${WIP:-}" = "1" ] && git -C "$PRIMARY" reset --soft HEAD~1
fi
```

If primary is not on main, skip propagation — the next `git pull` will pick it up.

## Step 4 — Write to Basic Memory vault

Use `mcp__basic-memory__search_notes` first to avoid duplicates, then `mcp__basic-memory__write_note` or `mcp__basic-memory__edit_note`. Use `[[wiki-links]]` for connections. Tag every note with the current project name.

If Basic Memory MCP is not connected, log the skip in the output summary and continue. Do not block.

## Step 5 — ADR check

If a significant architectural decision, convention, or recurring pattern emerged, prompt:
> Should this become an ADR? Candidate: "<pattern summary>". (y/n)

If yes: create `ai-workspace/decisions/ADR-NNN-<slug>.md` using the template at `ai-workspace/decisions/TEMPLATE.md`. Increment the highest existing ADR number.

## Step 6 — Create issues from surfaced work

Check for duplicates first (open and recently closed):

```bash
gh issue list --state open --limit 100 --json number,title
gh issue list --state closed --limit 20 --json number,title
```

**Source (a) — Reflect TODOs**: gotchas, follow-ups, technical debt surfaced during Steps 1–5. Create a GitHub issue for each with no duplicate.

**Source (b) — Scratchpad** (`ai-workspace/scratchpad.md`): for each line matching `- [ ] ...` → create issue → rewrite as `- [x] → #N`. Leave plain bullets untouched — they are reference notes.

## Step 7 — Finalize plan

Rename the active plan to `.done.md`. Verify Outcomes & Learnings is filled in first.

```bash
mv ai-workspace/plans/<name>.md ai-workspace/plans/<name>.done.md
```

This commit can go on the primary worktree — `.done.md` plan files are in the allowlist (see task-branches.md). Skip if no active plan.

## Step 8 — Phase gate

Read `.branch-context.md`:

- **MEMORY.md not updated + .branch-context.md had content** → soft block: warn and do not declare task complete until resolved.
- **.branch-context.md missing or empty** → warn but do not block.

## Output summary

| Layer | Action |
|---|---|
| MEMORY.md | N entries added, N pruned (X lines total) |
| Basic Memory | N notes written/updated (or: skipped — MCP unavailable) |
| Issues closed | #N, #N (verified) / #N still open (warned) |
| Issues created | #N "<title>", #N "<title>" |
| Issues commented | #N |
| ADR | Created ADR-NNN / Skipped |
| Plan | Finalized <name>.done.md / None |
| Phase gate | MEMORY.md updated: yes/no — .branch-context.md: found/missing |
