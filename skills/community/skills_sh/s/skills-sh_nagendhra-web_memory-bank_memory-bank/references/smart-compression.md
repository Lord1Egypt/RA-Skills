# Smart Compression

## The Problem

Every session adds content to MEMORY.md. Completed tasks accumulate.
Resolved blockers linger. Old session log entries pile up. Without
compression, memory becomes noise — Claude wastes tokens reading stale
history, and important current context gets buried.

Smart Compression keeps memory lean, relevant, and high-signal.

---

## Compression Thresholds

| Line Count | Action |
|-----------|--------|
| < 100 | No compression needed |
| 100-150 | Suggest: "Memory is at [N] lines. Want me to compress?" |
| 150-200 | Auto-compress at session end. Inform user of what changed. |
| > 200 | Compress immediately. Create MEMORY-ARCHIVE.md if it doesn't exist. |
| > 250 | Emergency compression (see below). |

---

## What Gets Compressed

### 1. Completed tasks (older than 3 sessions)

**Before:**
```markdown
## Completed
- [2025-03-20] Set up project scaffolding with Next.js 14 and TypeScript
- [2025-03-21] Created Prisma schema for User, Product, and Order models
- [2025-03-22] Built user registration endpoint with email verification
- [2025-03-25] Implemented product listing page with pagination
- [2025-03-28] Added shopping cart with local storage persistence
- [2025-04-01] Stripe checkout integration with session creation
- [2025-04-05] Webhook handler for payment confirmation
```

**After (sessions 1-4 compressed):**
```markdown
## Completed
- [Sessions 1-4] Project scaffolding, Prisma models, auth, product listing, cart
- [2025-04-01] Stripe checkout integration with session creation
- [2025-04-05] Webhook handler for payment confirmation
```

### 2. Resolved blockers

**Before:**
```markdown
## Blockers
- Need Stripe webhook secret from client (RESOLVED: got it 2025-04-03)
- PostgreSQL connection timeout in dev (RESOLVED: increased pool size)
- Waiting for design mockups for checkout page (RESOLVED: received 2025-03-28)
```

**After:**
```markdown
## Blockers
(none currently)
```

Resolved blockers are removed entirely. The resolution lives in git history.

### 3. Stale Active Work (no progress in 3+ sessions)

**Before:**
```markdown
## Active Work
- [ ] Implement email notification service (added session 3, no progress)
- [ ] Add admin dashboard (added session 2, no progress)
- [x] Stripe webhook handler (completed this session)
```

**After:**
```markdown
## Active Work
- [x] Stripe webhook handler (completed this session)

## Stale Items (no progress in 3+ sessions — keep or remove?)
- [ ] Implement email notification service
- [ ] Add admin dashboard
```

Flag stale items instead of silently removing. Let the user decide.

### 4. Old Session Log entries (older than 10 sessions)

Move to MEMORY-ARCHIVE.md with a summary paragraph.

### 5. Outdated Key Files

Files in the Key Files table that no longer exist → remove with note:
```
"Removed 2 stale entries from Key Files: src/old-auth.ts (deleted),
lib/legacy-utils.ts (deleted)."
```

---

## What NEVER Gets Compressed

These sections are permanent project knowledge:

| Section | Why it's protected |
|---------|-------------------|
| **Key Decisions** | Prevents re-litigating settled decisions |
| **Architecture Notes** | Design context that outlives any single task |
| **User Preferences** | Persistent across all sessions |
| **Project Overview** | Always needed for context |
| **Current "Where We Left Off"** | The most important section |
| **Active (unresolved) blockers** | Still relevant |
| **Last 3 Session Log entries** | Recent history for continuity |

---

## The Compression Algorithm

```
function compress(memory):
    lines = count_lines(memory)
    
    if lines < 100:
        return memory  // no compression needed
    
    target = 80  // aim for 80 lines post-compression
    
    // Phase 1: Safe compression (always do)
    remove resolved blockers
    remove completed tasks older than 3 sessions → collapse to session log
    remove Key Files entries for deleted files
    remove outdated Notes
    
    lines = count_lines(memory)
    if lines <= target:
        return memory
    
    // Phase 2: Moderate compression
    collapse session log entries older than 5 sessions into summary
    flag stale Active Work items (no progress in 3+ sessions)
    trim verbose descriptions to single lines
    
    lines = count_lines(memory)
    if lines <= target:
        return memory
    
    // Phase 3: Aggressive compression (only if still over target)
    collapse ALL completed tasks into one summary paragraph
    move session log to archive (keep only last 3)
    remove stale Active Work items (with user notification)
    
    return memory
```

---

## MEMORY-ARCHIVE.md

Created automatically when session history exceeds 10 entries or when
emergency compression runs.

### Template

```markdown
# Memory Archive — [Project Name]
Archive created: [DATE]
Covers: Sessions 1 through [N]

## Project Timeline

### Phase 1: Setup (Sessions 1-3)
[Paragraph summary: what was built, key decisions made, tools chosen]

### Phase 2: Core Features (Sessions 4-8)
[Paragraph summary: main features built, challenges overcome]

### Phase 3: [Phase Name] (Sessions 9-N)
[Paragraph summary]

## Archived Decisions
| Date | Decision | Reasoning | Status |
|------|----------|-----------|--------|
| [DATE] | [decision] | [why] | active / superseded |

## Historical Session Log
| Session | Date | Summary |
|---------|------|---------|
| 1 | [DATE] | [one-liner] |
| 2 | [DATE] | [one-liner] |
| ... | ... | ... |

## Archived Milestones
- [DATE] [milestone with key files]
- [DATE] [milestone with key files]
```

### Rules for the archive

- Write-once, read-rarely. Claude only reads the archive when explicitly
  asked about project history.
- Never modify archived entries (they're historical records).
- New archive entries are appended, never replacing old ones.
- Keep the archive under 200 lines. When it exceeds that, create
  phase-level summaries and remove individual session entries.

---

## Compression Report

Always tell the user what happened:

**Suggestion (100-150 lines):**
```
Memory is at 138 lines. I can compress it to ~85 by archiving 4 completed
milestones and removing 2 resolved blockers. Key decisions and architecture
are preserved. Want me to compress?
```

**Auto-compress (150-200 lines):**
```
Compressed MEMORY.md: 183 → 94 lines.
  - Archived: 6 completed tasks from sessions 1-5
  - Removed: 3 resolved blockers
  - Flagged: 2 stale active work items (no progress in 4 sessions)
  - Preserved: all 8 key decisions, architecture notes, current work
```

**Emergency compression (250+ lines):**
```
⚠ Memory was severely bloated (267 lines). Performed emergency compression:
  - Moved sessions 1-12 history to MEMORY-ARCHIVE.md
  - Kept only last 3 sessions of detail
  - Rebuilt Active Work from current git state
  - All key decisions preserved
  - Result: 78 lines. Please review and confirm accuracy.
```

---

## Emergency Compression

Triggered when memory exceeds 250 lines (something went wrong — likely
multiple sessions skipped compression).

```
Step 1: Create MEMORY-ARCHIVE.md (or append to existing)
Step 2: Move ALL session log entries except last 3 to archive
Step 3: Collapse ALL completed items into one summary paragraph
Step 4: Remove ALL resolved blockers
Step 5: Verify Active Work against actual git state
Step 6: Remove stale Active Work items
Step 7: Preserve: Key Decisions, Architecture Notes, User Preferences
Step 8: Recount lines. Target: under 100.
Step 9: Report to user with full details of what was compressed
```

---

## Compression Scheduling

| Event | Compression check? |
|-------|--------------------|
| Session end | Yes — always check line count |
| Mid-session "compress" | Yes — run immediately |
| Session start | No — never compress before user has context |
| Branch merge | Yes — good time to clean up |
| After recovery mode | Yes — reconstructed memory may be verbose |
