# Branch-Aware Memory

## Why Branch-Aware?

Different branches are different workstreams. When you're on `feature/auth`,
you don't need payments context cluttering your memory. When you switch to
`bugfix/race-condition`, the context should switch with you.

Branch-aware memory gives each git branch its own overlay on top of the
base project memory.

---

## Directory Structure

```
project-root/
  MEMORY.md                            ← Base memory (shared across branches)
  .memory/
    branches/
      feature-auth.md                  ← Auth feature overlay
      feature-payments.md              ← Payments overlay
      bugfix-login-race.md             ← Bugfix context
    snapshots/
      v1-launch.md                     ← Milestone snapshot (read-only)
```

---

## How Overlays Work

### Load Order

1. Read base `MEMORY.md` (full project context)
2. Detect current branch: `git branch --show-current`
3. Convert branch name to slug (see conventions below)
4. Check for `.memory/branches/<slug>.md`
5. If overlay exists: merge on top of base

### Merge Rules

- Overlay sections **override** base sections with the same heading
- Base sections not in overlay **stay as-is**
- Overlay sections not in base **get added**
- The merged result is what Claude works with during the session

**Example:**

Base `MEMORY.md`:
```markdown
## Where We Left Off
Working on the homepage redesign.

## Key Decisions
| Date | Decision | Reasoning |
|------|----------|-----------|
| 2025-04-01 | Chose Prisma | Type safety |
```

Overlay `feature-auth.md`:
```markdown
## Where We Left Off
Implementing JWT refresh token rotation in src/auth/refresh.ts.

## Branch-Specific Decisions
| Date | Decision | Reasoning |
|------|----------|-----------|
| 2025-04-05 | bcrypt over argon2 | Better library support in Node |
```

**Merged result Claude sees:**
```markdown
## Where We Left Off
Implementing JWT refresh token rotation in src/auth/refresh.ts.
← (overlay replaced base)

## Key Decisions
| Date | Decision | Reasoning |
|------|----------|-----------|
| 2025-04-01 | Chose Prisma | Type safety |
← (base preserved, not in overlay)

## Branch-Specific Decisions
| Date | Decision | Reasoning |
|------|----------|-----------|
| 2025-04-05 | bcrypt over argon2 | Better library support in Node |
← (overlay added new section)
```

---

## Branch Slug Convention

Convert branch names to safe filenames:

| Branch Name | Slug | File |
|-------------|------|------|
| `feature/auth-system` | `feature-auth-system` | `feature-auth-system.md` |
| `bugfix/login-race` | `bugfix-login-race` | `bugfix-login-race.md` |
| `hotfix/2.1.3` | `hotfix-2-1-3` | `hotfix-2-1-3.md` |
| `john/experiment` | `john-experiment` | `john-experiment.md` |

Rules:
- Replace `/` with `-`
- Lowercase everything
- Replace `.` with `-`
- Strip other special characters

---

## Overlay Template

Keep overlays focused and small (20-50 lines):

```markdown
# Branch: feature/auth-system
Created: [DATE] | Last updated: [DATE] | Sessions on branch: [N]

## Branch Purpose
[One sentence: why this branch exists]

## Current Work
- **Task:** [specific task with file reference]
- **Status:** [in progress | blocked | ready for review]
- **Next step:** [immediate next action]

## Branch-Specific Decisions
| Date | Decision | Reasoning |
|------|----------|-----------|
| [DATE] | [decision] | [why] |

## Files Changed on This Branch
| File | Change | Status |
|------|--------|--------|
| [path] | [what changed] | [done | in progress] |

## Merge Checklist
- [ ] All tests pass
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] No merge conflicts with main
- [ ] Memory overlay folded back into base
```

---

## Creating Overlays

### Automatic creation

When Claude detects a branch switch at session start:

1. Check if overlay exists for new branch
2. If yes: load it
3. If no: ask the user

```
"You're on feature/auth but I don't have branch-specific memory for it.
Want me to create an overlay? This keeps auth context separate from main."
```

### Manual creation

User says: "create a branch memory for this" or "track this branch separately"

Claude creates `.memory/branches/<slug>.md` with the overlay template.

### When NOT to create overlays

- Short-lived branches (quick bugfix, one-session work) — not worth it
- Branches that are basically main (no divergent context)
- When the user declines

---

## Writing Back

At session end, Claude determines where each change belongs:

### Goes to base MEMORY.md

- Architecture decisions that apply project-wide
- New entries in Key Decisions table
- Changes to Project Overview
- Updates to User Preferences
- New Key Files entries

### Goes to branch overlay

- Current task progress (specific to this branch)
- Branch-specific decisions
- Files changed on this branch
- Merge checklist progress

### Decision heuristic

```
"Does this information matter when I switch to a different branch?"
  Yes → write to base MEMORY.md
  No  → write to branch overlay
```

---

## On Branch Merge

When a feature branch merges to main (detected via git):

```
Step 1: Identify what's in the overlay
Step 2: Fold permanent items into base MEMORY.md
  - Completed work → Completed section
  - Permanent decisions → Key Decisions table
  - New key files → Key Files table
Step 3: Update "Where We Left Off" in base
Step 4: Delete or archive the overlay file
Step 5: Confirm to user
```

**Prompt:**
```
"feature/auth just merged to main. I've folded the auth decisions into
base memory and archived the branch overlay. The new 'Where We Left Off'
is: 'Auth system complete. Next: implement rate limiting middleware.'"
```

---

## Branch Switch Detection

At every session start:

```python
current_branch = git branch --show-current
memory_branch = parse "Branch:" field from MEMORY.md header

if current_branch != memory_branch:
    # Branch has changed since last session
    overlay = find_overlay(current_branch)
    if overlay:
        load_overlay(overlay)
        greet_with_branch_context()
    else:
        ask_to_create_overlay()
```

---

## Cleanup

### After merge

Branch deleted + merged → prompt to delete overlay:
```
"The feature/auth branch was deleted (merged to main). Want me to
clean up the branch overlay file?"
```

### Stale overlays

Overlays with no updates in 30+ days → flag at session start:
```
"Found 3 branch overlays that haven't been updated in over a month:
feature-old-redesign.md, bugfix-legacy.md, experiment-caching.md.
Want me to archive or remove them?"
```

### Bulk cleanup

`"clean up branch memory"` → Claude lists all overlays with last-updated
dates and asks which to keep, archive, or delete.

---

## Edge Cases

**Detached HEAD state:**
- Use base memory only
- Warn: "You're in detached HEAD state. Using base memory only."

**Multiple branches sharing work:**
- Cross-reference in overlays: "Related: see .memory/branches/feature-api.md"
- Don't duplicate — reference instead

**Rebased branches:**
- Overlay content is still valid (it tracks context, not commits)
- File paths may have shifted — run file validation

**Branch renamed:**
- Old overlay won't auto-map to new name
- Claude should detect: "Branch was renamed from feature/auth to feature/authentication.
  Want me to rename the memory overlay too?"
