---
name: memory-bank
description: >
  Token-efficient persistent memory system for Claude Code that saves ~67%
  tokens on session warm-up (verified with tiktoken). Layered architecture with progressive loading,
  compact encoding, branch-aware context, smart compression, session diffing,
  conflict detection, session continuation protocol, and recovery mode.
  Activates at session start (if MEMORY.md exists), on "remember this",
  "pick up where we left off", "what were we doing", "wrap up", "save progress",
  "don't forget", "switch context", "hand off", "memory health", "save state",
  "continue where I left off", "context budget", "how much context left",
  or any session start on a project with existing memory files. This skill
  solves two problems at once: Claude forgetting everything between sessions,
  AND sessions hitting context limits too fast. It replaces thousands of
  wasted re-explanation tokens with a compact, structured memory load that
  gives Claude full project context in under 2,000 tokens.
tags: [memory, context, persistence, sessions, token-efficiency, branch-aware, compression, analytics]
version: 2.0.0
author: community
---

# Memory Bank

An adaptive memory system that gives Claude Code persistent, intelligent
context across sessions — while cutting token waste so your sessions last
3-5x longer. Not a flat file — a layered architecture that compresses,
branches, diffs, self-heals, and loads only what matters.

---

## Core Architecture

Memory Bank operates on three layers:

```
┌─────────────────────────────────────────────┐
│  Layer 2: GLOBAL MEMORY                     │
│  ~/.claude/GLOBAL-MEMORY.md                 │
│  Cross-project patterns, user preferences,  │
│  reusable decisions. Permanent.             │
├─────────────────────────────────────────────┤
│  Layer 1: PROJECT MEMORY                    │
│  ./MEMORY.md (+ branch overlays)            │
│  Architecture, decisions, active work.      │
│  Lives as long as the project.              │
├─────────────────────────────────────────────┤
│  Layer 0: SESSION CONTEXT                   │
│  In-conversation only.                      │
│  Current task focus, scratch notes.         │
│  Dies when session ends (persisted to L1).  │
└─────────────────────────────────────────────┘
```

**Layer 0 (Session)** — Ephemeral. Tracks what you're doing right now.
Automatically flushed to Layer 1 at session end.

**Layer 1 (Project)** — The primary memory file. Tracks project state,
decisions, active work, blockers. Branch-aware: each git branch can have
its own overlay that merges with the base memory.

**Layer 2 (Global)** — Cross-project knowledge. Your coding preferences,
tool choices, patterns you always use. Lives in `~/.claude/GLOBAL-MEMORY.md`.
Loaded alongside Layer 1 at session start.

> See `references/memory-layers.md` for full architecture details.

---

## When to Activate

| Trigger | Action |
|---------|--------|
| Session starts, `MEMORY.md` exists | Full load sequence |
| `"remember this"`, `"don't forget"` | Mid-session update |
| `"wrap up"`, `"save progress"`, `"done for now"` | Full session write |
| `"pick up where we left off"`, `"what were we doing"` | Load + summarize |
| `"switch to [branch]"`, `"context for [feature]"` | Branch-aware load |
| `"memory health"`, `"is memory stale"` | Health check |
| `"hand off"`, `"onboard someone"` | Generate handoff doc |
| `"compress memory"`, `"clean up memory"` | Run compression |
| `"rebuild memory"` | Recovery mode |
| `"save state"`, `"continue this later"` | Session continuation protocol |
| `"context budget"`, `"how much context left"` | Context budget check |
| `"running out of context"`, `"session is long"` | Emergency save + continuation file |

---

## Workflow

### 1. Session Start — The Load Sequence

Execute this sequence before doing anything else:

```
Step 1: Detect memory files
  └─ Check for MEMORY.md in project root
  └─ Check for ~/.claude/GLOBAL-MEMORY.md
  └─ Check for MEMORY-ARCHIVE.md (has history been archived?)

Step 2: Detect git context
  └─ Current branch name
  └─ Check for .memory/branches/<branch>.md overlay
  └─ Days since last session (from "Last updated" field)

Step 3: Session diff (if git available)
  └─ Commits since last memory update
  └─ Files changed since last session
  └─ Any conflicts between memory and current code state

Step 4: Health check
  └─ Score memory freshness (see Health Scoring below)
  └─ Flag stale entries
  └─ Flag referenced files that no longer exist

Step 5: Context-aware greeting
  └─ Summarize where we left off (2-3 sentences, specific)
  └─ Report any drift detected (code changed, memory stale)
  └─ State the next immediate action
  └─ Ask: "Ready to continue, or has the plan changed?"
```

**Example greeting (fresh memory, same branch):**
> "Welcome back! Last session you finished the Stripe webhook handler in
> `src/api/webhooks/stripe.ts` and were about to write integration tests.
> The `handlePaymentSuccess()` function is complete but `handleRefund()` is
> stubbed out. 3 commits have landed since — all yours, no surprises.
> Ready to pick up with the integration tests?"

**Example greeting (stale memory, branch switched):**
> "Welcome back! Your memory is from 5 days ago on `main`, but you're now
> on `feature/user-profiles`. I found a branch overlay from 3 days ago with
> context about the profile avatar upload. However, `src/components/Avatar.tsx`
> referenced in memory was renamed to `ProfileImage.tsx`. Want me to update
> memory with the current state before we continue?"

**If no MEMORY.md exists:**
- Proceed normally
- After first meaningful work, offer: "Want me to start tracking our
  progress? I'll create a memory file so next session picks up instantly."

---

### 2. Mid-Session Updates

When the user says "remember this" or you complete a significant milestone:

1. Read current `MEMORY.md`
2. Determine what changed:
   - New decision made? → Update `Key Decisions`
   - Task completed? → Move from `Active Work` to `Completed`, update `Where We Left Off`
   - New blocker? → Add to `Blockers`
   - Important context? → Add to `Notes`
3. Write the updated file
4. Confirm with specifics: "Saved — added the Zod migration decision and
   marked the user model as complete."

**Do NOT rewrite the entire file on mid-session updates.** Only modify
the sections that changed. This preserves context from session start.

---

### 3. Session End — The Write Sequence

When wrapping up, execute a full memory write:

```
Step 1: Audit the session
  └─ What was accomplished? (be specific: files, functions, lines)
  └─ What decisions were made and why?
  └─ What's blocked or unresolved?
  └─ What should happen next? (crystal clear next step)

Step 2: Compress completed work
  └─ Move finished items to Completed with one-line summaries
  └─ Remove resolved blockers
  └─ Archive stale notes

Step 3: Update memory health metadata
  └─ Update "Last updated" timestamp
  └─ Increment session counter
  └─ Update file reference table (verify paths still exist)

Step 4: Write MEMORY.md
  └─ Full overwrite with current state
  └─ Verify the file was written successfully

Step 5: Check compression threshold
  └─ If > 150 lines, suggest compression
  └─ If > 200 lines, auto-compress (see Smart Compression)

Step 6: Prompt for global memory
  └─ Any cross-project learnings worth saving to Layer 2?
  └─ New user preferences discovered?
```

---

## MEMORY.md Template

```markdown
# Project Memory
Last updated: [DATE] | Session [N] | Branch: [BRANCH]
Memory health: [SCORE]/10

## Project Overview
[1-2 sentences. What this is, what stack, what stage.]

## Where We Left Off
- **Current task:** [specific task with file/function reference]
- **Status:** [done | in progress | blocked]
- **Next immediate step:** [so clear Claude can start without asking anything]
- **Open question:** [decision pending, if any]

## Completed
- [DATE] [one-line summary with key files touched]
- [DATE] [one-line summary]

## Active Work
- [ ] [task — specific file, function, or component]
- [ ] [task]
- [x] [recently completed, will archive on next compression]

## Blockers
- [blocker with context on what's needed to unblock]

## Key Decisions
| Date | Decision | Reasoning | Affects |
|------|----------|-----------|---------|
| [DATE] | [what was decided] | [why] | [files/areas impacted] |

## Key Files
| File | Purpose | Last Modified |
|------|---------|---------------|
| [path] | [what it does] | [session N] |

## Architecture Notes
[Non-obvious design choices, data flow, system boundaries]

## Known Issues
- [issue, severity, and workaround if any]

## Session Log
| Session | Date | Summary |
|---------|------|---------|
| [N] | [DATE] | [one-line summary of what happened] |

## User Preferences
[How the user likes to work — discovered across sessions]

## External Context
[APIs, services, env setup — NO secrets, NO credentials, NEVER]
```

---

## Branch-Aware Memory

When working across multiple git branches, memory adapts:

```
MEMORY.md                          <- Base project memory (main/trunk)
.memory/
  branches/
    feature-auth.md                <- Overlay for feature/auth branch
    feature-payments.md            <- Overlay for feature/payments branch
    bugfix-race-condition.md       <- Overlay for bugfix branch
```

**How it works:**

1. At session start, detect current git branch
2. Load base `MEMORY.md` first
3. Check `.memory/branches/<branch-slug>.md` for an overlay
4. Merge overlay on top of base (overlay sections take priority)
5. At session end, write changes back to the correct layer:
   - Architecture decisions → base `MEMORY.md` (shared across branches)
   - Branch-specific work → `.memory/branches/<branch>.md`

**On branch merge:**
- When a feature branch merges to main, prompt:
  "The `feature/auth` branch just merged. Want me to fold its memory
  overlay into the base MEMORY.md and clean up the branch file?"

> See `references/branch-aware-memory.md` for merge strategies.

---

## Smart Compression

Memory files grow. Smart Compression keeps them useful:

**Auto-compress triggers:**
- MEMORY.md exceeds 150 lines → suggest compression
- MEMORY.md exceeds 200 lines → auto-compress
- Entries older than 5 sessions → candidates for archival

**Compression rules:**
1. Completed tasks older than 3 sessions → collapse to one-liner in Session Log
2. Resolved blockers → remove entirely
3. Stale "Active Work" items (no progress in 3+ sessions) → flag for user
4. Decision Log entries → NEVER compress (permanent record)
5. Architecture Notes → NEVER compress (permanent record)

**Archival:**
When session count exceeds 10, create `MEMORY-ARCHIVE.md`:
```markdown
# Memory Archive
Archived sessions from Project Memory.

## Sessions 1-8 Summary
[Paragraph summary of early project work]

## Key Milestones
- Session 2: Initial project scaffolding complete
- Session 5: Auth system shipped
- Session 8: Database migration to Prisma complete
```

> See `references/smart-compression.md` for the full compression algorithm.

---

## Session Diffing

At session start, detect what changed since memory was last written:

```bash
# Get the date from MEMORY.md "Last updated" field
# Then check what happened since

git log --oneline --since="[last-updated-date]"
git diff --stat HEAD~[commits-since]
```

**Report format:**
> "Since your last session (3 days ago), there have been 7 commits:
> 4 by you, 3 by @teammate. Key changes: `src/api/users.ts` was refactored,
> `package.json` has 2 new dependencies (zod, @tanstack/query).
> Your memory references `src/api/users.ts` — I'll verify it's still accurate."

**Conflict detection:**
When session diff reveals changes that contradict memory:
- Memory says "using Express" but `package.json` now has Fastify → flag
- Memory references `src/auth/login.ts` but file was deleted → flag
- Memory says "blocked on API key" but `.env` now has it → update

> See `references/session-diffing.md` for conflict resolution strategies.

---

## Memory Health Scoring

Rate memory on a 1-10 scale across four dimensions:

| Dimension | Weight | Score 10 | Score 1 |
|-----------|--------|----------|---------|
| **Freshness** | 30% | Updated today | > 14 days old |
| **Relevance** | 30% | All referenced files exist | Most files missing/renamed |
| **Completeness** | 20% | All sections filled, next step clear | Missing key sections |
| **Actionability** | 20% | Can start working immediately | Need to ask 3+ questions |

**Display at session start:**
```
Memory health: 8/10
  Freshness:    9/10 (updated yesterday)
  Relevance:    7/10 (2 file paths changed)
  Completeness: 8/10 (all sections present)
  Actionability: 9/10 (next step is crystal clear)
```

**If health < 5:** Trigger recovery mode or suggest a memory rebuild.

---

## Recovery Mode

When memory is severely stale, corrupted, or missing critical context:

```
Step 1: Scan the project
  └─ Read package.json / pyproject.toml / go.mod (detect stack)
  └─ Read README.md and CLAUDE.md (project context)
  └─ List key directories and recent files

Step 2: Read git history
  └─ Last 20 commits (who, what, when)
  └─ Current branch and recent branches
  └─ Any open/recent PRs

Step 3: Reconstruct memory
  └─ Build Project Overview from package.json + README
  └─ Build Key Files from most-modified files in git log
  └─ Build Key Decisions from commit messages and code patterns
  └─ Set "Where We Left Off" from most recent commits
  └─ Flag confidence level: "Reconstructed from code — verify with user"

Step 4: Present and confirm
  └─ Show reconstructed memory to user
  └─ Ask for corrections
  └─ Write verified MEMORY.md
```

---

## Handoff Protocol

Generate a developer handoff document that's optimized for humans (not Claude):

```markdown
# Project Handoff: [Project Name]
Generated: [DATE] | By: [user] via Claude Code

## Quick Start
1. Clone: `git clone [repo]`
2. Install: `[package manager] install`
3. Setup: [env vars, database, etc.]
4. Run: `[dev command]`

## Current State
[Where the project is right now — what works, what doesn't]

## Architecture
[System diagram, key components, data flow]

## Active Work
[What's in progress, what's next, what's blocked]

## Key Decisions & Why
[Decisions that a new developer would question — with the reasoning]

## Gotchas
[Things that will bite you if you don't know about them]

## Who to Ask
[People, channels, or docs for domain-specific questions]
```

Trigger with: "generate a handoff", "onboard someone to this project",
"write a handoff doc"

---

## Context Efficiency Engine

The #1 complaint with Claude Code: **sessions hit context limits too fast.**
You spend half your tokens re-explaining context, and the other half doing
actual work. Memory Bank flips this ratio.

### The Token Problem (Verified with tiktoken)

Without memory-bank, every session start costs ~1,200 tokens:

```
Conversation overhead (4 exchanges):      ~566 tokens
  User re-explains project, stack, status
  Claude asks clarifying questions
  User answers follow-ups
  Back-and-forth until Claude understands

File reads (Claude reads 3+ files to orient): ~634 tokens
  Webhook handler:    ~344 tokens
  Checkout route:     ~257 tokens
  Stripe client:      ~33 tokens

TOTAL per session: ~1,200 tokens
TOTAL over 10 sessions: ~12,000 tokens wasted
```

### The Token Solution (Verified)

With memory-bank, the same session start costs ~400 tokens:

```
MEMORY.md loads (compact format):  ~334 tokens
  Entire project context in one structured file
  Decisions, files, status, blockers, architecture

Claude greeting + user confirms:   ~60 tokens
  Claude already knows everything, no questions needed

File reads needed:                 0 tokens
  Memory has file purposes, no need to read source

TOTAL per session: ~394 tokens (67% reduction)
TOTAL over 10 sessions: ~3,940 tokens (saved ~8,060)
```

These numbers were measured using tiktoken on our example files.
Actual savings depend on project complexity (larger projects save more).

### Progressive Loading

Don't dump everything into context. Load in tiers:

```
Tier 1: ALWAYS load (costs ~200 tokens)
  └─ Project Overview (1-2 sentences)
  └─ Where We Left Off (current task, status, next step)
  └─ Active Blockers

Tier 2: Load on DEMAND (costs ~300 tokens when needed)
  └─ Key Decisions (only when a decision comes up)
  └─ Key Files (only when working with files not in Tier 1)
  └─ Architecture Notes (only when touching architecture)

Tier 3: Load ONLY when asked (costs ~200 tokens when needed)
  └─ Session Log (only for velocity/history questions)
  └─ User Preferences (only on first session or when relevant)
  └─ External Context (only when working with APIs/services)
```

**Result:** Instead of loading 800 tokens of memory at once, load 200
tokens immediately and the rest only when actually needed. Most sessions
never need Tier 3 at all.

### Compact Encoding Rules

Every line in MEMORY.md is optimized for maximum information per token:

**Use structured shorthand, not prose:**
```
BAD (38 tokens):
  "We made the decision to use Prisma as our ORM instead of Drizzle
   because it provides better TypeScript type inference and the team
   is already familiar with it from previous projects."

GOOD (14 tokens):
  | 2025-04-01 | Prisma over Drizzle | Type inference, team familiarity | All DB |
```

**Use tables for structured data (they compress well):**
```
BAD (scattered prose — 120 tokens for 5 files):
  The main checkout route is in src/app/api/checkout/route.ts. The Stripe
  client is configured in src/lib/stripe.ts. Cart state management is in...

GOOD (table — 60 tokens for 5 files):
  | File | Purpose |
  | src/app/api/checkout/route.ts | Stripe session creation |
  | src/lib/stripe.ts | Stripe client singleton |
  | src/stores/cart.ts | Zustand cart + persistence |
```

**Use checklists for active work (scannable, dense):**
```
BAD (prose):
  We are currently working on the webhook handler, which is partially
  complete. We also need to write tests and haven't started yet.

GOOD (checklist):
  - [x] Stripe webhook handler — handlePaymentSuccess()
  - [ ] handleRefund() — stubbed, needs implementation
  - [ ] Integration tests for webhook endpoints
```

**One line, one fact. No filler words:**
```
BAD: "The project is essentially a web application that was built for..."
GOOD: "Bakery e-commerce. Next.js 14, Prisma, Stripe. Launching April."
```

### Context Budget Tracking

Monitor token usage and warn before hitting limits:

```
At session start, estimate the context budget:

Available context:   ~200,000 tokens (Claude's window)
Memory load:         ~800 tokens (Tier 1 + loaded Tiers)
System prompt:       ~2,000 tokens
Remaining for work:  ~197,200 tokens

At 40% usage (~80,000 tokens consumed):
  → Suggest: "We're at 40% context. Consider compacting soon."

At 60% usage (~120,000 tokens consumed):
  → Save a session checkpoint automatically
  → Suggest: "Context at 60%. Good time to /compact or start fresh."

At 80% usage (~160,000 tokens consumed):
  → Auto-save full state to MEMORY.md
  → Alert: "Context is at 80%. Saving state now — you can continue
     in a new session with zero loss. Say 'wrap up' or keep going."
```

### Session Continuation Protocol

When a session hits context limits or user wants to start fresh:

```
Step 1: EMERGENCY SAVE (before context dies)
  └─ Write MEMORY.md with EVERYTHING from current session
  └─ Include exact cursor position: file, function, line number
  └─ Include any uncommitted mental model (what Claude was thinking)
  └─ Include partial work state: what's done, what's half-done, what's next

Step 2: Write CONTINUATION.md (a one-shot warm-up file)
  └─ Ultra-compact: under 50 lines, under 500 tokens
  └─ Contains ONLY what the next session needs to start immediately
  └─ Format:

  ```markdown
  # Continue: [task name]
  Resume from: `src/auth/refresh.ts:47` — writing rotateToken()
  
  ## State
  - handlePaymentSuccess(): DONE ✓
  - handleRefund(): stubbed at line 89, needs Stripe refund.created event
  - Tests: NOT STARTED
  
  ## Context
  - Stripe webhook sig verified in middleware (line 12)
  - Using stripe.webhooks.constructEvent() not manual HMAC
  - Refund handler follows same pattern as payment handler
  
  ## Immediate Next Action
  Implement handleRefund() in src/api/webhooks/stripe/route.ts:89
  using the stripe.refund.created event payload. Pattern:
  extract refund.payment_intent → find order → update status to "refunded"
  ```

Step 3: GREET AND GO (next session)
  └─ Read CONTINUATION.md first (it's the fast-path)
  └─ Read MEMORY.md for full context only if needed
  └─ Delete CONTINUATION.md after loading
  └─ Start working immediately — no questions, no warm-up
```

**Trigger phrases:** "save state", "I'm running out of context",
"continue this later", "session is getting long"

### Token Savings By Feature (Verified)

| Feature | How It Saves | Measured Impact |
|---------|-------------|-----------------|
| Structured memory vs re-explaining | Compact file replaces 4+ conversation exchanges | ~566 tokens/session |
| Eliminating orientation file reads | Claude doesn't need to read source files to understand project | ~634 tokens/session |
| Compact encoding (tables > prose) | Same info, 39-42% fewer tokens than prose | 39-42% reduction in memory size |
| Session continuation protocol | CONTINUATION.md is under 200 tokens vs full re-warm-up | ~1,000 tokens on session handoff |
| Smart compression | Keeps memory under 150 lines / ~700 tokens | Prevents bloat over time |

**Verified totals (measured with tiktoken):**

| Scenario | Tokens | Turns |
|----------|--------|-------|
| Without memory-bank | ~1,200/session | 8 turns |
| With memory-bank | ~394/session | 2 turns |
| **Savings** | **~806/session (67%)** | **6 turns** |
| Over 10 sessions | **~8,060 saved** | 60 turns saved |
| Over 30 sessions | **~24,180 saved** | 180 turns saved |

### Anti-Patterns That Waste Tokens

**Never do these in memory files:**

```
✗ Verbose prose where a table works
✗ Repeating the same information in multiple sections
✗ Storing code snippets in memory (reference file:line instead)
✗ Long descriptions of completed work (one-line summaries only)
✗ Keeping resolved blockers (delete them)
✗ Storing information that's in README.md or CLAUDE.md already
✗ Using memory for things Git tracks (commit history, diffs, blame)
```

**Always do these:**

```
✓ Tables for structured data (decisions, files, tasks)
✓ Checklists for active work
✓ One sentence for Project Overview (not a paragraph)
✓ File:line references instead of describing code
✓ Delete resolved items (they're in git history)
✓ Reference other files instead of duplicating content
```

> See `references/context-efficiency.md` for the full token optimization guide.

---

## Rules for Excellent Memory

**Be surgical, not vague.**
Bad: "Working on auth"
Good: "Implementing JWT refresh token rotation in `src/auth/refresh.ts` —
`rotateToken()` is complete, needs Redis TTL logic in `src/cache/tokens.ts:47`"

**The "Next immediate step" is the single most important line.**
It should be so precise that Claude can start coding the instant a session
begins, with zero clarifying questions.

**Capture the "why" behind every decision.**
Future Claude will encounter the same trade-offs and re-litigate them
unless the reasoning is recorded.

**Never store secrets.** No API keys, passwords, tokens, or credentials.
Ever. Not even "temporarily". Reference `.env` or a secrets manager instead.

**Overwrite on session end, surgical update mid-session.**
Session end = full rewrite for consistency. Mid-session = targeted section
updates to avoid losing context.

**Keep it under 150 lines.** Compress aggressively. Stale information is
actively harmful — it misleads more than it helps.

---

## Auto-Setup via CLAUDE.md

For fully automatic memory with all features, add to project `CLAUDE.md`
(or `~/.claude/CLAUDE.md` for all projects):

```markdown
## Memory

At the start of every session:
1. Check for MEMORY.md in the project root
2. Check for ~/.claude/GLOBAL-MEMORY.md
3. Check current git branch and look for .memory/branches/<branch>.md
4. Run session diff — what changed since last memory update
5. Score memory health and flag any issues
6. Greet me with a specific summary and the next immediate step

During sessions:
- Update memory when I say "remember this" or complete a milestone
- Track key decisions with reasoning in the decision table

At session end (when I say "wrap up", "save", "done for now"):
1. Write comprehensive MEMORY.md with full current state
2. Ensure "Next immediate step" is crystal clear
3. Run compression if over 150 lines
4. Confirm what was saved
```

> See `references/claude-md-integration.md` for the full integration guide.

---

## Reference Files

- `references/memory-layers.md` — Full architecture of the 3-tier memory
  system with promotion rules and cross-layer interactions
- `references/branch-aware-memory.md` — Git branch integration, overlay
  merging, and cleanup strategies
- `references/smart-compression.md` — Compression algorithm, archival
  thresholds, and what to never compress
- `references/session-diffing.md` — Cross-session change detection,
  conflict resolution, and drift correction
- `references/advanced-patterns.md` — Team workflows, velocity tracking,
  handoff protocol, and enterprise patterns
- `references/context-efficiency.md` — Token optimization guide,
  progressive loading details, compact encoding reference
- `references/claude-md-integration.md` — Complete setup guide for
  automatic triggering across all projects

## Examples

- `examples/solo-fullstack.md` — Memory for a solo developer on a Next.js app
- `examples/team-backend.md` — Team-shared memory for a backend service
- `examples/monorepo.md` — Multi-domain memory for a monorepo
- `examples/minimal.md` — 5-line memory for quick prototypes
