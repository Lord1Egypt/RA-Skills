---
name: workflow-execution
description: >
  Plan-first workflow for non-trivial work: plan with done criteria,
  create a tracking issue, package context as documents on the issue,
  decide where code lives, hand off to an executing agent, verify completion.
  Use when tasks involve 3+ steps, architecture/strategy decisions,
  risky edits, or iterative bug-fixing.
---

# Workflow Execution

Run this workflow for any meaningful work. The core loop: **plan → track → package context → route → hand off → execute → verify.**

## Core Principles

- Plan before acting. The plan lives on the tracking issue, not in chat.
- Package context as documents, not spawn strings. The executing agent should never depend on chat history.
- Decide where code lives before writing any code.
- Prefer the simplest approach that can pass verification.
- Be explicit about proof, not optimism.

---

## Phase 1: Plan

Enter planning before acting when **any** trigger is true:

- Work requires **3 or more concrete steps**
- Work changes architecture, interfaces, data flow, or shared contracts
- Work includes risky edits (security, auth, migrations, destructive operations, production config, or unknown blast radius)
- Work will be handed off to another agent or subagent

### Plan contents

1. **Goal** — one sentence describing what done looks like.
2. **Done criteria** — explicit, checkable conditions. Not "it works" but "tests pass, PR merged, deployed."
3. **Constraints** — what must not break, budget limits, timeline, dependencies.
4. **Failure modes** — what could go wrong and how you'll detect it.
5. **Ordered steps** — small, each with a verification method (test, build, smoke check, log proof, diff).

---

## Phase 2: Track

Before implementation starts, create or reference a **tracking issue** in your project management system.

### What to do

1. **Create an issue** with a clear title and the goal from Phase 1.
2. **Attach the plan as a document** on the issue (key: `plan`). This is the source of truth — not a chat message, not a comment, a structured document.
3. **Link to parent issues** if this work is part of a larger effort.

### Why documents, not descriptions

- Documents are **revisioned** — you can see how the plan evolved.
- Documents are **keyed** — `plan`, `design`, `context` each have a clear role.
- Documents are **agent-readable** — any agent that picks up the issue gets the full context.
- Documents survive **context resets** — when a session compacts or a new agent spawns, the context lives on the issue, not in memory.

### Tracker reference implementations

This skill is tracker-agnostic. See `references/` for how to do this with specific systems:
- `references/tracker-paperclip.md` — Paperclip Issues + Documents API
- `references/tracker-github.md` — GitHub Issues + issue body/comments
- `references/tracker-none.md` — skip tracking, plan in a local file

---

## Phase 3: Package Context

Before handing off to an executing agent, attach structured documents to the tracking issue:

### Required: `plan` document
The plan from Phase 1. Always attached.

### When applicable: `design` document
Attach when work involves:
- New interfaces or API contracts
- Architecture decisions with tradeoffs
- User-facing UI/UX (include design brief: user flow, empty/loading/error states, copy, responsive behavior, accessibility)

### When applicable: `context` document
Attach when the executing agent needs background that isn't obvious from the code:
- Prior decisions and their rationale
- Relevant code references (files, functions, patterns to follow)
- Domain knowledge the agent won't have
- Links to related issues or discussions

### Packaging principle
Ask: *"If a brand new agent picked up this issue with zero chat history, could they do the work?"* If not, add more context documents.

---

## Phase 4: Route

Before execution, decide **where the code lives**.

### Decision criteria

| Signal | Destination |
|--------|-------------|
| Work extends an existing project/repo | **Existing repo** — branch off main |
| Work is reusable, publishable, or useful to others | **New repo** — create it, then work there |
| Work is pure local glue, config, or one-off automation | **Local workspace** — but document why it's local |

### Routing rules

- **Default: existing repo.** Most work extends something that already exists.
- **New repo trigger:** If you find yourself thinking "other people could use this" or "this should be a skill/package," it's a new repo.
- **Local-only justification required.** If code stays in the local workspace, document why — it should be because it's genuinely specific to this setup, not because it was easier.
- **Branch naming:** Include the tracking issue identifier in the branch name (e.g., `SUP-490/skill-rewrite`).

---

## Phase 5: Hand Off

Spawn the executing agent with an **issue reference**, not inline context.

### Dispatch rule

**Code handoffs MUST use `sessions_spawn`, not `sessions_send`.**

`sessions_spawn` triggers the full enforcement pipeline (Lobster gate, spawn-code-lint, post-spawn PR creation). `sessions_send` bypasses all of it. Use `sessions_send` only for non-code work: status checks, coordination, questions.

The test: if the message asks the target agent to **write, edit, or move code** → `sessions_spawn`. Everything else → `sessions_send` is fine.

### Handoff protocol

1. The spawn message includes: the tracking issue identifier, the repo/branch to work in, and any model/thinking preferences.
2. The executing agent's first step is: read the issue, read attached documents (`plan`, `design`, `context`), then proceed.
3. The executing agent updates the issue as it works — comments for progress, status changes for state transitions.

### Subagent strategy

- **Spawn by default** when work spans multiple files/systems, requires research, or includes long-running operations.
- **One clear objective per subagent** with concrete deliverables.
- **Clean ownership boundaries** — avoid overlapping edit zones.
- **Prefer fewer, well-scoped subagents** over many tiny ones.

---

## Phase 6: Execute

### Minimal-impact changes
- Implement the smallest change set that satisfies the goal.
- Reuse existing patterns before inventing new abstractions.
- Keep naming, structure, and style consistent with local code.
- Avoid incidental cleanup unless it directly reduces risk.

### Failure recovery hierarchy
When something goes wrong during execution, follow this priority order:

1. **Transient provider failure** (429, timeout, model overload): OpenClaw's native
   model fallback chain handles this automatically. Do not change tracker issue
   status. Continue in the same session once the request succeeds.

2. **Context reset or compaction**: Re-read the `plan`, `context`, and `design`
   documents from the tracking issue. Never reconstruct plan state from in-session
   memory after compaction — the issue documents are the source of truth.

3. **Durable blocker** (missing dependency, unclear requirements, architectural gap):
   Update the tracking issue status to `blocked`. Add a comment naming the specific
   blocker and what needs to resolve it.

4. **The tracker is an audit trail and coordination hub — not the place to manage transient retries.**
   Do not flip status on transient errors, partial progress, or model fallbacks.

### Autonomous bug-fix behavior (guardrailed)
When bugs appear during execution:
1. Reproduce and isolate the failing path.
2. Form the smallest plausible fix hypothesis.
3. Apply minimal-touch patch.
4. Re-run impacted checks and one nearby regression check.
5. Repeat until pass or a guardrail is hit.

**Stop and escalate when:**
- Root cause remains unclear after multiple attempts.
- Fix requires major architectural change.
- Risk of data loss or security impact is non-trivial.

### Demand elegance (balanced)
- Reject hacks that create hidden fragility or repeat incidents.
- Prefer clear structure over clever shortcuts.
- Scale sophistication to task size — don't over-engineer obvious fixes.

---

## Phase 7: Verify

Do not mark complete without proof.

### Evidence types
- **Tests:** targeted unit/integration/e2e checks.
- **Static checks:** lint, typecheck, build.
- **Runtime checks:** smoke test key affected flows.
- **Logs/output:** command results or excerpts showing success.
- **Diff sanity:** verify only intended files changed.

### Governance
- Significant code changes: branch + PR + review before merge.
- CI must pass before merge.
- Fix review comments before closing.

### Close the loop
1. Update the tracking issue status to done.
2. Add a closing comment with verification evidence.
3. If the work produced a reusable lesson, capture it durably.

---

## Self-Correction Loop

If the correction cycle was triggered by a context reset or compaction, re-read the issue's `plan`, `context`, and `design` documents before resuming — do not reconstruct plan state from in-session memory.

After any correction cycle (failed check, rework, rollback):

1. Record what failed and why (brief, concrete).
2. Extract one reusable lesson/pattern.
3. Apply that lesson immediately to remaining work.
4. Capture a durable note when the lesson is broadly reusable.

---

## Quick Checklist (Repeat Each Run)

- [ ] Plan: goal, done criteria, constraints, failure modes, ordered steps
- [ ] Track: issue created/referenced, plan document attached
- [ ] Package: context documents attached (design, context as needed)
- [ ] Route: code destination decided, branch created with issue ID
- [ ] Hand off: agent spawned with issue reference, not inline context
- [ ] Execute: minimal-impact implementation
- [ ] Verify: evidence collected, checks pass, governance followed
- [ ] Close: issue updated, evidence in closing comment, lessons captured
