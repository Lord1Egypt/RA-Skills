# Session Diffing

## Purpose

Between sessions, the world moves. You push code, teammates push code,
dependencies update, files get renamed. Memory written 3 days ago may
not match reality.

Session diffing catches this drift at session start — before stale memory
causes confusion or bad decisions.

---

## The Diff Process

Run at session start, after loading MEMORY.md but before greeting the user.

### Step 1: Extract Baseline

Parse from MEMORY.md:
- `Last updated` date → baseline timestamp
- `Branch` field → expected branch
- `Session N` → session counter
- All file paths in `Key Files` table → expected files

### Step 2: Git History Since Last Update

```bash
# Total commits since last session
git log --oneline --since="YYYY-MM-DD"

# Commits by the current user
git log --oneline --since="YYYY-MM-DD" --author="$(git config user.name)"

# Files changed with stats
git diff --stat HEAD~N   # where N = commits since last update

# Check if branch changed
git branch --show-current
```

Summarize:
- Total commits since last update
- Commits by user vs by others
- Which files were touched

### Step 3: File Reference Validation

For every file in the Key Files table:

```
1. Does the file still exist at that path?
   → Yes: mark as valid
   → No: check if renamed (git log --follow --diff-filter=R -- old_path)
     → Renamed: note new path
     → Deleted: mark as stale
```

### Step 4: Dependency Check

```bash
# Check if package manifest changed since last session
git diff [baseline]..HEAD -- package.json package-lock.json \
  pyproject.toml poetry.lock requirements.txt \
  go.mod go.sum Cargo.toml Cargo.lock Gemfile Gemfile.lock
```

Report any new dependencies added or removed.

### Step 5: Conflict Detection

Compare memory claims against code reality:

| Conflict Type | How to Detect | Example |
|--------------|---------------|---------|
| **Missing file** | `Key Files` path doesn't exist on disk | Memory: `src/auth.ts` → file deleted |
| **Renamed file** | `git log --follow` shows rename | `auth.ts` → `authentication.ts` |
| **Stack drift** | Package manifest contradicts memory | Memory: "Express", reality: Fastify |
| **Stale task** | `Active Work` item completed in git | Memory: "in progress", git: merged PR |
| **Resolved blocker** | Blocker condition no longer true | Memory: "need API key", `.env` has it |
| **Decision contradiction** | Code pattern conflicts with `Key Decisions` | Decision: "use Prisma", imports: Drizzle |
| **Branch mismatch** | Current branch ≠ memory branch | Memory: `main`, current: `feature/auth` |

### Step 6: Generate Diff Report

Compile findings into a structured report for the greeting.

---

## Diff Report Format

### Clean (no drift detected)

```
Memory health: 9/10 | Updated yesterday | 2 commits since (both yours)
All file references valid. No conflicts detected.
```

Include in greeting naturally — don't make it feel like a report.

### Minor drift

```
Since last session (2 days, 5 commits — 3 yours, 2 by @teammate):
  - src/api/users.ts was refactored (referenced in memory)
  - 1 new dependency added: @tanstack/query
  - All other memory references are accurate
Auto-correcting: updated file modification note in Key Files.
```

### Significant drift

```
⚠ Memory drift detected (5 days, 14 commits):
  - src/auth/login.ts was renamed → src/auth/authentication.ts
  - package.json: Express removed, Fastify added
  - 2 Active Work items appear completed in git
  - Branch changed: memory says main, you're on feature/v2

Suggested actions:
  1. Update file references (auto-fixable)
  2. Confirm stack change: Express → Fastify in memory
  3. Mark completed items as done
  4. Load branch overlay for feature/v2
```

### Severe drift (triggers recovery mode suggestion)

```
⚠ Memory is severely out of date (21 days, 47 commits):
  - 5 of 8 Key Files paths are invalid
  - Active Work doesn't match current code state
  - Multiple architecture decisions may have changed
  
Recommend: rebuild memory from current code state.
Run recovery mode? (This will reconstruct memory from git + code)
```

---

## Conflict Resolution Strategies

### Auto-Resolve (Safe — no user confirmation needed)

These are non-controversial, factual corrections:

| Conflict | Resolution |
|----------|-----------|
| File renamed | Update path in Key Files. Note: "auto-corrected: X → Y" |
| File deleted | Remove from Key Files. Note: "removed stale entry: X (deleted)" |
| Completed task in git | Move from Active Work to Completed |
| Resolved blocker (env var now exists) | Remove from Blockers |
| Session counter increment | Update automatically |

Always inform the user what was auto-resolved:
```
"Auto-corrected 3 things: renamed auth.ts → authentication.ts in
Key Files, marked 'user registration' as completed, removed the
resolved API key blocker."
```

### User-Resolve (Needs confirmation)

These involve judgment or potential misunderstanding:

| Conflict | Prompt |
|----------|--------|
| Stack/tool change | "Memory says Express, code has Fastify. Did you switch?" |
| Architecture change | "The auth flow in memory doesn't match current code. Want me to update?" |
| Contradictory decision | "Key Decisions says Prisma, but I see Drizzle imports. Update?" |
| Teammate changes in your area | "3 commits by @alex touched files in your Active Work. Review?" |

### Full Rebuild (Nuclear option)

When > 50% of memory is stale:
- Suggest recovery mode
- Reconstruct from git + code
- Present for user verification
- Never auto-rebuild without asking

---

## Handling Team Changes

When commits by **other people** are detected since last session:

```
Step 1: List their commits separately
  "3 commits by @alex, 2 by @jordan since your last session"

Step 2: Check overlap with memory
  "2 of @alex's commits touched src/api/ — referenced in your Active Work"

Step 3: Summarize, don't alarm
  "@alex refactored the user endpoint and added input validation.
   Your Active Work on the orders endpoint is unaffected."

Step 4: Flag real conflicts (if any)
  "⚠ @jordan modified src/middleware/auth.ts, which you have listed
   as 'in progress' in Active Work. Want to review their changes?"
```

**Rules for teammate changes:**
- Never auto-resolve conflicts caused by teammate changes
- Always present teammate changes as informational, not adversarial
- If changes are in different areas: note and move on
- If changes overlap: flag for review

---

## Non-Git Projects

When there's no git repository:

```
Step 1: Compare file modification timestamps vs "Last updated"
Step 2: Check if Key Files still exist at their paths
Step 3: Skip commit history analysis entirely
Step 4: Skip dependency diffing (no reliable way without git)
Step 5: Still validate file references and flag stale entries
```

Limitations without git:
- Can't detect who made changes
- Can't detect renames (only missing files)
- Can't diff dependencies reliably
- Health scoring weights shift: Freshness and Actionability matter more

---

## Performance

Keep the diff fast — it runs at every session start:

- Use `--since` with dates (not scanning full history)
- Use `--oneline` for compact output
- Use `--stat` instead of full diffs (file names + change counts)
- Don't read file contents for validation — just check existence
- Cache the diff result in L0 session context (don't recompute)
- Total time budget: < 5 seconds for a typical repo
