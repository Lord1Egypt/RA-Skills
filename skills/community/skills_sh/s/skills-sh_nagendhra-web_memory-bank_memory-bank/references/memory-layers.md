# Memory Layers Architecture

## Overview

Memory Bank uses a 3-tier architecture. Each layer has a different scope,
lifetime, and purpose. Together they give Claude complete context without
bloating any single file.

```
┌─────────────────────────────────────────┐
│  L2: Global    ~/.claude/GLOBAL-MEMORY  │  Permanent, cross-project
├─────────────────────────────────────────┤
│  L1: Project   ./MEMORY.md             │  Project lifetime
├─────────────────────────────────────────┤
│  L0: Session   (in conversation)       │  Dies at session end
└─────────────────────────────────────────┘
```

---

## Layer 0: Session Context

**Scope:** Current conversation only.
**Lifetime:** Created at session start, destroyed at session end.
**Storage:** In-memory (conversation context). Not written to disk.

### What belongs in L0

- Current task focus and scratch notes
- Intermediate results and experiments
- Temporary decisions not yet confirmed
- Debug findings in progress
- Things the user said "try this" about (not yet committed to)

### What does NOT belong in L0

- Anything that should survive a session restart
- Confirmed decisions (promote to L1)
- Cross-project preferences (promote to L2)

### Auto-flush at session end

When a session ends, Claude reviews L0 and promotes relevant items:

```
L0 contents at session end:
  "Tried Redis for caching, works well"  →  promote to L1 (Key Decisions)
  "User prefers explicit error handling"  →  promote to L2 (User Preferences)
  "Debugging that weird timeout issue"    →  promote to L1 (Known Issues) if unresolved
  "Scratch calc: 4096 / 64 = 64 chunks"  →  discard (ephemeral)
```

---

## Layer 1: Project Memory

**Scope:** Single project.
**Lifetime:** Created on first session, lives as long as the project.
**Storage:** `MEMORY.md` in project root, plus optional branch overlays.

### What belongs in L1

- Project overview and stack
- Architecture and design decisions (with reasoning)
- Active work items with specific file/function references
- Blockers and open questions
- Key files table
- Session log (compressed history)
- Known issues and gotchas
- Branch-specific overlays in `.memory/branches/`

### Size budget

| Stage | Target Lines |
|-------|-------------|
| New project | 30-50 |
| Active development | 50-100 |
| Mature / complex | 100-150 |
| Hard cap (triggers compression) | 200 |

### Branch awareness

L1 supports overlays per git branch:

```
MEMORY.md                          ← base (always loaded)
.memory/branches/
  feature-auth.md                  ← loaded when on feature/auth
  feature-payments.md              ← loaded when on feature/payments
```

Overlay sections override base sections with the same heading.
See `branch-aware-memory.md` for full details.

### Compression lifecycle

```
Session 1-3:   Everything is fresh, no compression needed
Session 4-8:   Completed tasks start accumulating, suggest compression
Session 8-15:  Auto-compress, create MEMORY-ARCHIVE.md for old sessions
Session 15+:   Regular compression cycles, lean active memory
```

See `smart-compression.md` for the full algorithm.

---

## Layer 2: Global Memory

**Scope:** All projects, all sessions.
**Lifetime:** Permanent (until user modifies or removes entries).
**Storage:** `~/.claude/GLOBAL-MEMORY.md`

### What belongs in L2

- Coding style preferences ("always use explicit returns")
- Tool choices ("prefers pnpm over npm")
- Language/framework preferences ("uses TypeScript strict mode always")
- Common patterns ("always adds error boundaries in React")
- Reusable architectural decisions ("prefers composition over inheritance")
- Work style ("likes detailed commit messages", "prefers small PRs")

### What does NOT belong in L2

- Project-specific decisions (those are L1)
- Temporary preferences ("use verbose logging for this sprint")
- Anything that contradicts a project's L1 memory (L1 wins)

### When to update L2

Only promote to L2 when a pattern is confirmed across **2+ projects**:

```
Project A: "Chose Zod for validation — great type inference"
Project B: "Using Zod again for API validation"
  → Promote to L2: "Prefers Zod for runtime validation (TypeScript projects)"
```

Single-project decisions stay in L1 even if they feel universal.

### GLOBAL-MEMORY.md Template

```markdown
# Global Memory
Last updated: [DATE]

## User Profile
- Role: [e.g., Senior fullstack developer]
- Primary languages: [e.g., TypeScript, Go, Python]
- Experience level: [context for how Claude should communicate]

## Code Style Preferences
- [preference with reasoning]
- [preference with reasoning]

## Tool Choices
| Category | Preference | Why |
|----------|-----------|-----|
| Package manager | pnpm | Speed, disk efficiency |
| Validation | Zod | Runtime + type inference |
| ORM | Prisma | Type safety, migrations |
| Testing | Vitest | Fast, ESM native |

## Patterns I Always Use
- [pattern: description]
- [pattern: description]

## Things I Never Want
- [anti-pattern: why to avoid]
- [anti-pattern: why to avoid]

## Work Style
- [how you like to work with Claude]
- [communication preferences]

## Reusable Decisions
| Decision | Reasoning | First Used |
|----------|-----------|------------|
| [decision] | [why] | [project/date] |
```

---

## Promotion Rules

### L0 → L1 (Session → Project)

**When:** At session end, or when user says "remember this."

**What promotes:**
- Confirmed technical decisions → Key Decisions table
- Completed work → Completed section + Session Log
- New blockers → Blockers section
- Important context → Architecture Notes or Notes
- Unresolved issues → Known Issues

**What stays in L0:**
- Scratch calculations
- Abandoned experiments
- Speculative ideas not confirmed
- Temporary debug state

### L1 → L2 (Project → Global)

**When:** A decision or preference is confirmed across 2+ projects.

**What promotes:**
- Tool/library choices that repeat
- Coding style preferences that hold
- Architectural patterns used everywhere
- Work style observations

**Process:**
1. At session end, Claude checks if any L1 decisions match an existing L2 entry
2. If a new decision echoes an L1 decision from a different project → suggest promotion
3. User confirms → write to GLOBAL-MEMORY.md
4. Never auto-promote without user confirmation

### Demotion

**L1 → Archive:**
- Completed tasks older than 5 sessions → MEMORY-ARCHIVE.md
- Resolved blockers → removed entirely

**L2 → Removed:**
- User explicitly contradicts a L2 preference → ask if L2 should update
- Example: L2 says "prefers Prisma" but user chooses Drizzle in new project
  → "Your global memory says you prefer Prisma, but you chose Drizzle here.
     Want me to update your global preference, or is this project-specific?"

---

## Cross-Layer Interactions

### Load Order at Session Start

```
1. Load L2 (global context — who is the user, how do they work)
2. Load L1 base (project state — MEMORY.md)
3. Load L1 overlay (branch context — .memory/branches/<branch>.md)
4. Resume L0 (start new session context)
5. Run session diff (compare L1 against actual code state)
6. Generate greeting (synthesize all layers into summary)
```

### Priority (Conflict Resolution)

When layers disagree, more specific wins:

```
L1 (project) overrides L2 (global)
  L2 says "use pnpm" but project uses yarn → yarn wins
  L2 says "TypeScript strict" but project has strict: false → respect project

L0 (session) overrides L1 (project)
  L1 says "next step: write tests" but user says "let's refactor first" → refactor

Branch overlay overrides base L1
  Base says "working on auth" but branch overlay says "working on payments" → payments
```

### Information Flow Diagram

```
Session Start:
  L2 ──→ ┐
  L1 ──→ ├──→ Merged Context ──→ Greeting + Next Step
  Git ──→ ┘

Mid-Session:
  User action ──→ L0 (scratch) ──→ L1 (if "remember this")

Session End:
  L0 ──→ L1 (flush)
  L1 ──→ L2 (promote if cross-project pattern)
  L1 ──→ Archive (compress old entries)
```
