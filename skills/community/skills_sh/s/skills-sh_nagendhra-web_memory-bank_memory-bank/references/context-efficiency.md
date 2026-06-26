# Context Efficiency Guide

The #1 reason Claude Code sessions die early: context window exhaustion.
You burn tokens re-explaining your project, loading irrelevant history,
and storing verbose prose. Memory Bank fixes this systematically.

This reference covers every technique for minimizing token waste while
maximizing what Claude knows about your project.

---

## The Math (Verified with tiktoken)

Claude Code's context window is finite. Every token matters:

```
Typical session budget:      ~200,000 tokens (200k window)
System prompt:               ~14,328 tokens (fixed, always present)
System tools:                ~17,600 tokens (fixed)
Autocompact buffer:          ~33,000 tokens (reserved, unusable)
Available for work:          ~135,000 tokens

WITHOUT memory-bank (measured):
  Conversation overhead:     ~566 tokens (4 exchanges to re-explain)
  File reads to orient:      ~634 tokens (Claude reads 3+ source files)
  Total waste per session:   ~1,200 tokens
  Over 10 sessions:          ~12,000 tokens gone

WITH memory-bank (measured):
  Compact MEMORY.md:         ~334-667 tokens (depends on project size)
  Greeting + confirm:        ~60 tokens
  File reads:                0 tokens (memory has context)
  Total per session:         ~394-727 tokens

Net savings per session:     ~473-806 tokens (39-67% reduction)
Net savings over 10 sessions: ~4,730-8,060 tokens
```

These numbers were measured using tiktoken (cl100k_base) on our example
MEMORY.md files with realistic session-start conversations. Claude's
tokenizer differs slightly, but the ratios hold.

---

## Progressive Loading

### The Three Tiers

Not all memory is equally urgent. Load in priority order:

**Tier 1: ALWAYS (auto-loaded at session start)**

```markdown
## Project Overview
Bakery e-commerce. Next.js 14, Prisma, Stripe. Launching April.

## Where We Left Off
- Current task: Stripe webhook handler in src/api/webhooks/stripe/route.ts
- Status: in progress — handlePaymentSuccess() done, handleRefund() stubbed
- Next: Implement handleRefund(), then write integration tests

## Blockers
- Need Stripe webhook secret from client for staging
```

Cost: ~150-250 tokens. Gives Claude 80% of what it needs.

**Tier 2: ON DEMAND (loaded when the topic comes up)**

```markdown
## Key Decisions
[loaded when Claude encounters a decision point]

## Key Files
[loaded when Claude needs to find or reference files]

## Architecture Notes
[loaded when touching system design or data flow]
```

Cost: ~200-400 tokens when needed. Many sessions never need all of Tier 2.

**Tier 3: RARE (loaded only when explicitly asked)**

```markdown
## Session Log
[loaded for velocity tracking or "what did we do last week?"]

## User Preferences
[loaded on first session or when behavior seems off]

## External Context
[loaded when working with APIs or external services]
```

Cost: ~150-300 tokens. Most sessions skip Tier 3 entirely.

### How Progressive Loading Works

At session start:
1. Read MEMORY.md fully (Claude needs to parse it)
2. Surface Tier 1 in the greeting (actively use these tokens)
3. Hold Tier 2 and 3 in passive memory (read but not actively referenced)
4. When a Tier 2/3 topic comes up naturally, reference it

The key insight: Claude reads the whole file once, but only **actively uses**
Tier 1 tokens in its initial response. Tier 2/3 activate on demand without
re-reading the file.

### When to Override Progressive Loading

Force full load for:
- First session on a project (need full orientation)
- After long breaks (7+ days, need full refresh)
- Recovery mode (rebuilding, need everything)
- Team onboarding (generating handoff, need everything)

---

## Compact Encoding Reference

### Tables vs Prose

Tables are the single biggest token saver. Same information, ~50% fewer tokens.

**Decisions:**
```
PROSE (42 tokens):
We decided to use Prisma as our ORM. We considered Drizzle and raw SQL
as alternatives, but chose Prisma because of its superior TypeScript
type inference and because the team already has experience with it.

TABLE (16 tokens):
| Prisma over Drizzle | Type inference, team familiarity | All DB access |
```

**File references:**
```
PROSE (35 tokens):
The main API route for creating checkout sessions is located in the
file src/app/api/checkout/route.ts. The Stripe client configuration
can be found in src/lib/stripe.ts.

TABLE (12 tokens):
| src/app/api/checkout/route.ts | Stripe session creation |
| src/lib/stripe.ts | Stripe client singleton |
```

### Checklists vs Descriptions

```
PROSE (28 tokens):
The webhook handler is partially complete. The payment success handler
is finished but the refund handler still needs to be implemented.
Integration tests have not been started yet.

CHECKLIST (15 tokens):
- [x] handlePaymentSuccess()
- [ ] handleRefund() — needs implementation
- [ ] Integration tests
```

### Reference Pointers vs Content Duplication

Never store code in memory. Point to it:

```
BAD (90+ tokens):
The authentication middleware checks for a Bearer token in the
Authorization header, validates it using jsonwebtoken, and attaches
the decoded user to req.user. The implementation is:
  const token = req.headers.authorization?.split(' ')[1];
  const decoded = jwt.verify(token, process.env.JWT_SECRET);
  req.user = decoded;

GOOD (8 tokens):
Auth middleware: src/middleware/auth.ts:12 (JWT verify → req.user)
```

### Abbreviation Conventions

Use consistent shorthand in memory files:

| Long Form | Short Form |
|-----------|-----------|
| in progress | WIP |
| not started | TODO |
| completed | DONE |
| blocked by | BLOCKED: |
| see file | → file:line |
| because | — reason |
| alternative considered | vs. X |

### One-Line Summaries

Every completed task should compress to one line:

```
BAD: "During session 5, we worked on implementing the shopping cart
functionality. We used Zustand for state management with a localStorage
middleware for persistence. The cart page UI includes quantity controls
and real-time price calculations."

GOOD: "[S5] Cart: Zustand + localStorage, quantity controls, price calc
```

---

## Session Continuation Protocol

### When to Trigger

| Signal | Action |
|--------|--------|
| User says "save state" / "continue later" | Full save + CONTINUATION.md |
| Context at 60% | Auto-checkpoint MEMORY.md |
| Context at 80% | Alert + auto-save + suggest new session |
| Context at 90% | Emergency save immediately |
| Session crash / disconnect | MEMORY.md should already be checkpointed |

### CONTINUATION.md Format

The fastest possible warm-up file. Under 50 lines, under 500 tokens:

```markdown
# Continue: [specific task name]
Session: [N+1] | Branch: [branch] | Saved: [timestamp]

## Resume Point
File: `[exact file path]`
Function: `[function name]` at line [N]
State: [what's done in this function, what's left]

## Context Snapshot
- [fact 1 Claude needs to continue — one line]
- [fact 2]
- [fact 3]
- [any decision made during the interrupted session]

## Partial Work
- [what's half-done and needs finishing]
- [any temporary state: variables, test data, debug flags]

## Immediate Next Action
[ONE sentence: the exact next thing to do. No ambiguity.]
```

### CONTINUATION.md vs MEMORY.md

| | CONTINUATION.md | MEMORY.md |
|---|---|---|
| Purpose | Fast warm-up for NEXT session | Full project state |
| Size | Under 50 lines / 500 tokens | Under 150 lines / 1,500 tokens |
| Lifespan | Single use, deleted after load | Permanent |
| Content | Cursor position + immediate context | Everything |
| When written | Session end / context limit | Every session end |

At next session start:
1. Check for CONTINUATION.md first (fast path)
2. Load it — this is all Claude needs to start coding
3. Load MEMORY.md as background context
4. Delete CONTINUATION.md
5. Start working immediately

### Emergency Save Procedure

When context is critically high (80%+):

```
Step 1: STOP current work mid-task if needed
Step 2: Write MEMORY.md with current full state
Step 3: Write CONTINUATION.md with exact resume point:
  - File and line number where work stopped
  - What's done, what's half-done in current function
  - Any decisions or findings from this session
  - The exact next line of code to write
Step 4: Notify user:
  "Context is at 82%. I've saved everything — MEMORY.md has full state,
   CONTINUATION.md has the exact resume point. Start a new session and
   say 'continue' — I'll pick up at src/auth/refresh.ts:47 with zero
   warm-up."
Step 5: If user continues: keep working but avoid verbose responses
Step 6: If user starts new session: greeting loads CONTINUATION.md first
```

---

## Context Budget Awareness

### Monitoring

Claude should track approximate context usage throughout the session:

```
Milestones:
  25%  → No action. Working efficiently.
  40%  → Internal note: consider being more concise in responses.
  50%  → Suggest: "We're at ~50% context. Good time to /compact."
  60%  → Auto-checkpoint MEMORY.md. Mention it briefly.
  75%  → Save state. Alert: "Context at 75%. ~25% remaining.
          Consider wrapping up or starting fresh for max efficiency."
  85%  → Emergency save. Strong recommendation to start new session.
  95%  → Final save. Stop accepting new tasks.
```

### Staying Lean Mid-Session

Claude should optimize its OWN token usage during the session:

```
INSTEAD OF (verbose — wastes tokens):
"I've finished implementing the handleRefund function in the webhook
handler file. The function extracts the payment_intent from the refund
event, looks up the corresponding order in the database using Prisma,
and updates the order status to 'refunded'. I also added error handling
for cases where the order isn't found. Let me know if you'd like me to
proceed with the integration tests next."

DO THIS (concise — same information, ~40% fewer tokens):
"Done — handleRefund() in route.ts:89. Extracts payment_intent → finds
order via Prisma → updates status to 'refunded'. Added not-found error
handling. Ready for integration tests?"
```

Rules for Claude during memory-bank sessions:
- Lead with the result, not the process
- Use file:line references instead of describing locations
- Skip "I've done X" preamble — show the result directly
- Use bullet points over paragraphs for status updates
- Never repeat what the user just said back to them

---

## Token Cost of Memory Features

Know what each feature costs so you can budget:

| Feature | Token Cost | When Incurred |
|---------|-----------|---------------|
| Tier 1 memory load | 150-250 | Every session start |
| Tier 2 memory (on demand) | 200-400 | When topic arises |
| Tier 3 memory (rare) | 150-300 | Only when asked |
| Session diff report | 100-200 | Session start (with git) |
| Health score display | 50-100 | Session start |
| Branch overlay load | 100-200 | When on non-main branch |
| CONTINUATION.md load | 200-400 | After interrupted session |
| Compression report | 50-100 | Session end (when triggered) |
| Handoff generation | 500-1,000 | One-time on request |
| **Typical session total** | **500-1,200** | |

Compare to without memory-bank: 1,700-5,000 tokens of re-explanation.

---

## Compact MEMORY.md Benchmark

A well-written MEMORY.md should hit these targets:

| Metric | Target | Red Flag |
|--------|--------|----------|
| Total lines | 50-120 | > 150 without compression |
| Token count | 500-1,200 | > 2,000 |
| Project Overview | 1-2 lines | > 5 lines |
| Where We Left Off | 4-6 lines | > 10 lines |
| Key Decisions (per entry) | 1 table row | Multi-line prose |
| Key Files (per entry) | 1 table row | Descriptions > 10 words |
| Completed (per entry) | 1 line | Multi-line descriptions |
| Active Work items | Checkboxes | Prose paragraphs |

### Self-Test

Run this check against your MEMORY.md:

```
1. Can Claude start working from "Where We Left Off" alone?
   → If yes: Tier 1 is good
   → If no: "Next immediate step" isn't specific enough

2. Is any information in MEMORY.md also in README or CLAUDE.md?
   → If yes: delete it from memory (don't duplicate)

3. Are there prose paragraphs that could be tables?
   → If yes: convert them

4. Are there completed items older than 3 sessions?
   → If yes: compress to one-liners

5. Is the file under 1,200 tokens?
   → If no: compress aggressively
```

---

## Anti-Patterns (Token Killers)

### 1. The Novelist

```
BAD: "Over the course of our previous session, we engaged in a thorough
discussion about the merits of various authentication strategies..."

Memory is not a journal. It's a state file.
```

### 2. The Duplicator

```
BAD: Storing stack info in MEMORY.md when it's already in CLAUDE.md
BAD: Storing project description when it's in README.md
BAD: Storing git history when `git log` has it

Memory stores what NO OTHER FILE stores.
```

### 3. The Hoarder

```
BAD: Keeping every completed task with full descriptions
BAD: Never removing resolved blockers
BAD: Storing "just in case" context

If it's resolved, it's in git. Delete it from memory.
```

### 4. The Code Stasher

```
BAD: Pasting code snippets into memory for "reference"

Code belongs in code files. Memory stores pointers: file:line
```

### 5. The Architect Astronaut

```
BAD: Storing detailed system diagrams in memory
BAD: Long architecture descriptions

Use 2-3 lines for architecture. Detail lives in code and docs.
```
