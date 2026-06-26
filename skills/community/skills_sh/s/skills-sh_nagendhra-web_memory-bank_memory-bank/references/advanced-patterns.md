# Advanced Patterns

Power-user patterns for getting the most out of memory-bank.

---

## Pattern 1: Team Memory Protocol

**Trigger:** Working on a shared codebase with teammates who also use Claude Code.

**Setup:**
1. Commit `MEMORY.md` to the repo
2. Add `.memory/` to `.gitignore` (branch overlays are personal)
3. Add attribution rule to `CLAUDE.md`:

```markdown
MEMORY.md is team-shared. When updating:
- Add your initials and date to entries: "[JS 2025-04-08] Finished auth"
- Preserve entries by other team members
- Never delete someone else's Active Work items
```

**How it works:**
- Each teammate's Claude session reads the shared memory
- Updates include initials so authorship is clear
- Merge conflicts in MEMORY.md: accept both sides, Claude reconciles at next session

**Team standup shortcut:**
Say "generate my standup update" → Claude reads MEMORY.md and produces:

```
Yesterday: Completed Stripe webhook handler, resolved Redis caching blocker
Today: Writing integration tests for payment flow
Blockers: None currently
```

**Memory review in PRs:**
Include MEMORY.md changes in PR diffs. Reviewers see the context and
reasoning alongside the code changes.

---

## Pattern 2: Velocity Tracking

**Trigger:** "how's our velocity?", "are we on track?", "project status"

**Requires:** 5+ sessions of history in Session Log.

**What Claude analyzes:**
- **Tasks per session:** Average completed tasks per session. Trending up (accelerating) or down (hitting walls)?
- **Recurring blockers:** Same blocker appearing 3+ times → systemic issue
- **Scope creep:** Active Work growing faster than Completed → flag it
- **Session duration patterns:** Are sessions getting shorter (less work) or longer (deeper work)?
- **Estimated remaining:** Based on current velocity, rough session count for remaining Active Work

**Output format:**
```
Project Velocity — Sessions 1-12

Tasks completed:     28 total | ~2.3 per session
Current trajectory:  Stable (slight acceleration in last 3 sessions)
Active work items:   5 remaining
Est. sessions left:  2-3 at current pace

Recurring blockers:
  - "Waiting for client assets" appeared 3 times (sessions 4, 7, 9)
    → Consider: placeholder assets or async workflow

Scope creep check:
  - 3 items added to Active Work in last 3 sessions
  - 4 items completed in same period
  - ✓ Net progress is positive

Recommendation: On track. The recurring client asset blocker is the
main risk to timeline.
```

---

## Pattern 3: Decision Tree

**Trigger:** "why didn't we use X?", "should we reconsider Y?", "decision history"

Enhanced Key Decisions table that tracks the full decision context:

```markdown
## Decision Tree
| # | Date | Decision | Alternatives Considered | Reasoning | Confidence | Revisit | Status |
|---|------|----------|------------------------|-----------|------------|---------|--------|
| 1 | 2025-03-15 | Prisma for ORM | Drizzle, TypeORM, raw SQL | Type safety, migration tooling, team knows it | High | Never | Active |
| 2 | 2025-03-18 | pnpm over npm | npm, yarn, bun | Disk efficiency, strict deps | High | Never | Active |
| 3 | 2025-03-22 | Skip Redis caching | Redis, in-memory cache | Premature optimization at current scale | Medium | At 10k users | Active |
| 4 | 2025-04-01 | Express over Fastify | Fastify, Hono, Koa | Middleware ecosystem, team familiarity | Low | Next major version | Active |
```

**Status values:**
- `Active` — current decision, in effect
- `Superseded` — replaced by a newer decision (note which one)
- `Reverted` — tried it, rolled back (note why)
- `Under review` — being reconsidered

**When someone asks "why not X?":**
Claude checks the Decision Tree first. If X was already considered and
rejected, Claude explains the reasoning without re-debating.

---

## Pattern 4: Context Snapshots

**Trigger:** "snapshot this", "save a milestone", "snapshot: [name]"

Save a frozen snapshot of project state at key milestones:

```
.memory/
  snapshots/
    v1-launch.md
    pre-migration.md
    auth-complete.md
```

**Snapshot template:**
```markdown
# Snapshot: v1-launch
Created: 2025-04-08 | Session: 12 | Branch: main

## State at This Moment
[Full project state — what works, what doesn't, what's planned]

## Architecture at Snapshot
[System design, key components, data flow]

## Active Decisions
[Copy of Key Decisions table at this moment]

## Metrics
- Files: [count]
- Dependencies: [count]  
- Test coverage: [%]
- Open issues: [count]
```

**Rules:**
- Snapshots are **read-only** — never modified after creation
- Claude only reads them on explicit request: "what was the state at v1 launch?"
- Useful for: post-mortems, comparing before/after migrations, project retrospectives

---

## Pattern 5: Focus Mode

**Trigger:** "focus on [domain]", "I'm only working on [area] today"

Claude loads only memory sections relevant to the specified domain:

```
User: "focus on the payment system"

Claude loads:
  ✓ Project Overview (always)
  ✓ Key Decisions mentioning payments/Stripe
  ✓ Active Work items with payment-related files
  ✓ Key Files in src/payments/ or src/api/checkout/
  ✓ Blockers related to payments
  
  ✗ Skips: auth-related work, frontend styling, infra tasks
```

**Benefits:**
- Reduces context noise for deep work sessions
- Claude doesn't accidentally suggest switching to unrelated tasks
- Session-end writes only update the focused sections

**Exit focus mode:** "broaden context" or "full memory" or just start
a new session.

---

## Pattern 6: Memory Hooks

Add automated checks and actions to your memory workflow:

```markdown
## Hooks

### Pre-flight (session start)
- [ ] Run `pnpm install` (deps may have changed)
- [ ] Run `pnpm db:migrate` (new migrations may exist)
- [ ] Verify `.env.local` has all required variables
- [ ] Run `pnpm dev` and confirm app starts

### Auto-checkpoint
Save memory every 60 minutes during long sessions.

### Post-flight (session end)
- [ ] Run `pnpm lint`
- [ ] Run `pnpm test`
- [ ] Commit MEMORY.md if team-shared
```

Add to CLAUDE.md to automate:
```markdown
At session start, run the Pre-flight Checklist in MEMORY.md.
Every 60 minutes, save a memory checkpoint.
At session end, run the Post-flight Checklist before saving memory.
```

---

## Pattern 7: Cross-Project Insights

**Trigger:** "what patterns do I always use?", "common decisions across projects"

After working on 3+ projects with memory-bank, the Global Memory (L2)
accumulates patterns. Ask Claude to analyze:

```
User: "what are my patterns across projects?"

Claude analyzes GLOBAL-MEMORY.md:
  - Most used tools: Prisma (4/5 projects), Zod (3/5), Tailwind (5/5)
  - Common pattern: always adds error boundaries in React
  - Recurring decision: composition over inheritance
  - Common mistake: forgets to add loading states (flagged 3 times)
  - Preferred testing approach: integration > unit for API routes
```

---

## Pattern 8: Onboarding Acceleration

**Trigger:** "onboard someone", "new team member joining", "explain this project to a newcomer"

Claude reads MEMORY.md + git history + README and generates:

```markdown
# Onboarding Guide — [Project Name]
Generated: [DATE]

## 30-Second Overview
[What this project does, for who, why it matters]

## Get Running in 5 Minutes
1. `git clone [repo]`
2. `cp .env.example .env.local` and fill in [these vars]
3. `pnpm install`
4. `pnpm db:migrate`
5. `pnpm dev` → http://localhost:3000

## Architecture (TL;DR)
[ASCII diagram of system components and data flow]

## The 5 Most Important Files
[Files that, if you understand these, you understand the project]

## Key Decisions (And Why)
[Top 5 decisions a newcomer would question, with the reasoning]

## Gotchas That Will Bite You
[Things not obvious from the code that every new dev hits]

## Current State
[What's done, what's in progress, what's blocked]

## Your Suggested First Task
[A starter task that teaches the codebase without too much risk]
```

---

## Pattern 9: Memory-Driven Code Review

**Trigger:** Before reviewing a PR or when someone asks for a review.

Claude loads MEMORY.md alongside the diff and checks:

- Does the PR align with documented architecture decisions?
- Does it contradict any Key Decisions? (e.g., PR uses raw SQL, but
  decision says "use Prisma for all queries")
- Does it touch areas with known issues or blockers?
- Does it affect files in Active Work (potential conflicts)?

**Output:**
```
Memory-informed review notes:
  - This PR adds a raw SQL query in src/api/reports.ts. Note: Decision #1
    says "use Prisma for all DB queries." Is this an intentional exception?
  - The file src/middleware/auth.ts has a known issue (session 8):
    "Race condition on concurrent refresh token requests." This PR modifies
    the same file — verify the race condition isn't affected.
  - PR overlaps with @alex's Active Work on the user endpoint. Coordinate.
```

---

## Pattern 10: Disaster Recovery Ladder

When memory is corrupted, stale, or lost — try each step, stop when usable:

```
Level 1: Validate
  └─ Check current MEMORY.md against code. Fix minor drift.
  └─ Success? → Done. Memory is usable.

Level 2: Archive Recovery
  └─ Check MEMORY-ARCHIVE.md for recent clean state
  └─ Restore last known good state + update from git
  └─ Success? → Done.

Level 3: Snapshot Recovery
  └─ Check .memory/snapshots/ for milestone snapshots
  └─ Load most recent snapshot + update from git
  └─ Success? → Done.

Level 4: Git Reconstruction
  └─ Rebuild from git log + code analysis + README
  └─ Present reconstructed memory for user verification
  └─ Success? → Done.

Level 5: Fresh Start
  └─ Interview the user: "What are we building? What's the stack?
     What are you working on right now?"
  └─ Write a new MEMORY.md from scratch
  └─ Always succeeds (but loses historical context)
```

Each level is more aggressive. Start gentle, escalate only if needed.
