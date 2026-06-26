# Feature Design

Create feature design from specification.

Architectural decisions and contract enumeration deserve careful
reasoning — shallow analysis produces shallow design. Load
[status-workflow.md](status-workflow.md) for correct status management.

## Contents

- [When to Use](#when-to-use)
- [Depth Scaling](#depth-scaling)
- [Workflow](#workflow) — Steps 1-15
- [Guidelines](#guidelines)
- [Design Template](#design-template)
- [Error Handling](#error-handling)

## When to Use

- Scope is **Medium**, **Large**, or **Complex** (check `scope:` in spec.md frontmatter) — depth scales with scope (see Depth Scaling below)
- Spec is complete (no open questions blocking progress)
- Ready to define HOW to build

Start with a clean context window. Load artifacts from disk (spec.md, decisions.md),
not from a previous phase's conversation context. See SKILL.md Phase Transitions.

## Depth Scaling

Design runs at every scope above Small. What scales is depth:

- **Medium — light.** Capture Scope, Decisions (with Source
  and Scope), light Patterns & Reuse, Subsystem Presence claims, Component
  Design, and Requirements Traceability. Dispatch the Plan subagent (Step 10) at
  light depth. Skip the heavy data-model work: full member enumeration, Reused
  Component / Utility Contracts, Cross-Task Value Trace, and the Dependency
  Inversion check. The closing checklist runs only its grounding items
  (member-enumeration items are Large/Complex-only).
- **Large/Complex — full.** Everything below, including full member
  enumeration, contracts, cross-task value trace, and dependency inversion; the
  Plan subagent (Step 10) runs at full depth.

If the light Medium design surfaces a load-bearing decision novel to the
codebase, escalate Medium → Large: run the full design and tasks (see
[auto-sizing.md](auto-sizing.md) Safety Valve).

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

Track each step as it completes — mark it done before moving to the next.
In Claude Code, create a task list at phase start (TaskCreate) and update
each step as it completes (TaskUpdate).

### Step 1: Resolve Feature

1. If a name is given -> match `.artifacts/specs/{date}-{name}/` (glob `*-{name}` or `*-{name}-*` for a collision variant)
2. If no name -> match current git branch to `branch:` in spec.md frontmatter
3. If multiple or no match -> list available specs and ask user

### Step 2: Load Spec

Read `.artifacts/specs/{date}-{name}/spec.md`, including `## Decisions` and
`## Session Context`. Follow any `sources:` pointer to its durable source
before designing.

**Blocking-question gate:** If spec.md `## Open Questions` holds any `[blocking]`
question, halt: list the blocking items, route to [discuss](discuss.md) or the user to
resolve, then exit. `[deferrable]` questions do not gate; proceed. For an untagged
legacy spec, judge whether a question would change the architecture you are about to
define.

If decisions.md exists, load it for resolved gray areas.

### Step 3: Load Project Knowledge

If `.artifacts/knowledge.md` exists, read it before designing. It contains
cross-feature decisions, gotchas, and conventions accumulated from previous
features. Use it to:

- Avoid repeating past mistakes
- Follow established architectural patterns
- Respect decisions already made for the project

knowledge.md is cross-feature context, not this feature's content. Let it
shape your approach; do not carry other features' decisions, IDs, or
file references into this design unless this feature actually touches
them. design.md stays scoped to this feature.

If it doesn't exist, skip this step.

### Step 4: Load Architecture Context

Load each of the following if it exists. Skip silently if absent.

**Project root:**
- `CLAUDE.md` — project conventions, architecture, and agent constraints
- `AGENTS.md` — agent instructions

**Cached area context:**
- `.artifacts/codebase/{area}.md` — the area cache, if a prior feature
  already explored the area this feature touches

`.artifacts/knowledge.md` is already loaded in Step 3 — do not re-read.

Greenfield projects may have only `CLAUDE.md`. Never block on a missing
file — load what's there. If nothing exists, proceed with spec.md only.

### Step 5: Research Phase

Check for new technologies in spec:

- APIs mentioned
- Libraries not in codebase
- External services

For each new tech:
- Check `.artifacts/research/{topic}.md`
- If exists: use cached research
- If not: research and create cache (follow [research.md](research.md) trust boundary rules)

When there are unknowns, dispatch research -- one subagent per unknown topic, in
a single turn (emit multiple dispatch calls in one message, never sequentially).
A Medium scope typically has at most one unknown (one subagent); Large/Complex
often has several (fan-out). Each subagent follows research.md and writes to
`.artifacts/research/{topic}.md`. Output is the cache file; main agent reads
results from disk after dispatch completes.

Single-turn dispatch shape (three unknown techs):

```text
Turn N (one message):
  - dispatch subagent for {topic-1}, brief = {research.md + topic-1 + spec context}
  - dispatch subagent for {topic-2}, brief = {research.md + topic-2 + spec context}
  - dispatch subagent for {topic-3}, brief = {research.md + topic-3 + spec context}
Turn N+1: read .artifacts/research/{topic-N}.md for each, validate against spec.
```

Map this shape to the subagent dispatch primitive available in the harness.
No unknowns: no research runs. One unknown: one research subagent.

Follow the [Knowledge Verification Chain](../SKILL.md#knowledge-verification-chain) for all research.

When composing the research brief, state the question open — enumerate the
options to weigh against project conventions; never pre-load the recommended
conclusion (see [research.md](research.md) Brief Neutrality).

When incorporating research into the design, validate findings against the spec's requirements.
Research informs decisions but the spec remains the single source of truth for what to build.

### Step 6: Codebase Exploration

Load [codebase-exploration.md](codebase-exploration.md).

Focus areas:
- Similar existing features
- Reusable components
- Patterns to follow
- Integration points

**Subagent dispatch:** Codebase exploration is context-heavy
(multi-phase workflow with exhaustive member enumeration). Dispatch as
a single subagent that owns the entire exploration end to end and
writes findings to disk per the exploration template (see
[codebase-exploration.md](codebase-exploration.md)). Main agent reads
the artifact, never the raw file content. Depth scales: at **Large/Complex**
the subagent does exhaustive member enumeration; at **Medium** it runs light --
Subsystem Presence and the touched entities only.

Subagent brief:

- Paths to `spec.md`, [codebase-exploration.md](codebase-exploration.md)
- Path to `.artifacts/codebase/{area}.md` cache (if it exists)
- "Follow codebase-exploration.md end to end. Write findings per the
  template inlined there. Anchor every claim with file:line. Member
  enumeration must be exhaustive, not sampled."

**Discovery batch:** Step 5 research subagents and this exploration
subagent are independent. Dispatch all in a single turn -- emit multiple
dispatch calls in one message:

```text
Turn N (one message):
  - dispatch research subagent for {topic-1}
  - dispatch research subagent for {topic-2}
  - dispatch codebase-exploration subagent
Turn N+1: read .artifacts/research/*.md and exploration artifact from disk,
          advance to Data Model.
```

Map this shape to the subagent dispatch primitive available in the harness.

### Step 6a: Exploration Depth Gate

**Large/Complex only** — Medium skips exhaustive member enumeration (see Depth Scaling).

Before proceeding to the design generation phase (Steps 10-13), verify the exploration artifact's `Touched Types -- Member Enumeration` table is populated for every entity, projection, or contract the feature will read or modify.

**Citation resolution (deterministic).** Run the bundled script against the exploration
artifact:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/verify-citations.py .artifacts/codebase/{area}.md
```

It extracts every `file:line` citation and checks each resolves against the repo (file
exists, line in range), exiting non-zero with the unresolved list if any fail. An
unresolved citation is poisoned ground -- the checklists downstream would `[pass]`
against it -- so a non-zero exit fails this gate. Review the printed list: a genuine
miss returns to exploration; a rare false positive (e.g. a URL the regex caught) the
agent disregards. If the script is unavailable, open each cited `file:line` by hand.

**Content match (spot-check).** For the load-bearing citations -- the touched types the
feature reads or writes -- open the cited `file:line` and confirm it holds the claimed
member. Resolution proves the line exists, not that it says what the row claims.

**Exit criterion (all must hold):**

- Every touched type named in the spec or data flow has at least one row in the enumeration table
- `verify-citations.py` exits zero -- every cited `file:line` resolves against the repo
- Every load-bearing citation's content matches its claimed member (spot-check above)
- Every absence claim in the Absence Claims table has a `file:line` anchor
- No row has a blank Member cell or TBD `file:line`

If any criterion fails, return to [codebase-exploration.md](codebase-exploration.md) Phase 4 before continuing.

### Step 7: Check Concerns

Review the gotchas loaded in Step 3 (`.artifacts/knowledge.md ## Gotchas`)
for components flagged as fragile, carrying tech debt, or having test
coverage gaps.

Any such component requires extra care. Document in the Considerations
section how the design mitigates those concerns.

If no relevant gotchas exist, skip this step.

### Step 8: Record Discoveries

Load [knowledge.md](knowledge.md) for format.

Route the cross-feature knowledge this design surfaced to
`.artifacts/knowledge.md`:

1. **Cross-feature decisions** -> `## Decisions`, with rationale
2. **Gotchas** -> `## Gotchas`, with context
3. **Normative conventions** the codebase follows -> `## Conventions`, with where they apply

If `.artifacts/knowledge.md` doesn't exist, create it with the three empty section headers (`## Decisions`, `## Gotchas`, `## Conventions`).

Descriptive area patterns (reference files, integration points) are written to `.artifacts/codebase/{area}.md` by exploration (Step 6) — do not duplicate them here. Record only what crosses features; feature-specific detail stays in this feature's design.md, and inventory facts (packages, routes, modules) are re-derivable and not recorded.

### Step 9: Check Visual References

Check if the spec includes a `designs/` folder with visual references:

1. Look for `.artifacts/specs/{date}-{name}/designs/`
2. If images exist (screenshots, mockups, wireframes):
   - Review each image to understand visual requirements
   - Note UI/UX patterns, layout, components shown
   - Consider these in component design and implementation
3. If no designs folder: proceed without visual context

### Step 10: Dispatch Design Plan subagent

Steps 11-13 are owned by a Plan subagent. Main agent dispatches once,
receives structured slot fillers, composes design.md per the design
template (below), then runs the closing checklist against the
artifact before advancing to Step 14.

Why dispatched: Steps 11-13 are intelligence-sensitive (member
enumeration with file:line cites, dependency inversion, traceability
expansion). Isolating them in a Plan subagent keeps main context clean
for the user-visible checklist and approval gate. Plan is read-only by
harness contract (Edit/Write/NotebookEdit excluded), so it returns
structured slot fillers; main composes the artifact via the canonical
template (pattern A1: Plan returns slots, main fills template).

At **Medium**, dispatch the Plan subagent at light depth (Steps 11-13 with the
reduced slot set). Run Steps 11-13 inline only when subagent support is
unavailable; main agent executes them directly in that case.

Subagent brief:

- Inputs (paths only -- Plan reads from disk):
  - `.artifacts/specs/{date}-{name}/spec.md`
  - `.artifacts/specs/{date}-{name}/decisions.md` (if exists)
  - Exploration artifact path (from Step 6)
  - `.artifacts/research/*.md` (cached topics from Step 5)
  - `.artifacts/knowledge.md` (if exists)
  - `.artifacts/codebase/{area}.md` cache matching the feature's area
    (if exists)
  - `CLAUDE.md`, `AGENTS.md` (project root, if exist)
  - `.artifacts/specs/{date}-{name}/designs/` (if exists)
- Reference: the design template inlined at the bottom of this
  reference — return chunks matching the template section order and
  table shapes exactly
- Process: follow Step 11 (Data Model, including its closing checklist
  criteria internally), Step 12 (Dependency Inversion -- silent
  reasoning, never echoed into chunks), Step 13 prep (organize chunks
  per template section). When `spec.md` frontmatter has `origin:
  defect`, also produce the Root Cause block (hypothesis at file:line,
  evidence, confidence, fix-type) -- read the suspected sources to
  anchor the hypothesis, never speculate. Anchor every claim about an
  existing type with `file:line` from the exploration's Member
  Enumeration. Resolve any internal `[fail]` against Step 11's
  checklist criteria before returning.
- Return shape (structured slot fillers per template section, no
  surrounding prose):
  - Scope: in-scope, out-of-scope bullets
  - Root Cause (only when `spec.md` frontmatter has `origin: defect`):
    hypothesis (one sentence at file:line granularity), evidence rows
    (repro signal, log/stack/trace, file:line of first incorrect
    decision), confidence (high/medium/low), fix-type plan
    (root-fix or workaround with justification)
  - Research Summary: bullets per cached topic (or empty)
  - Patterns & Reuse: Conventions rows, Existing Code rows,
    Reused Component Contracts rows (when feature reuses a shared
    component in an execution context or input shape that differs
    from existing consumers), Reused Utility Contracts rows (one
    per shared utility the feature reuses), Integration Points rows
  - Data Model: Entities rows; per-entity Member Enumeration blocks
    (member, type, file:line); Relationships text or mermaid; API
    Contracts rows; Currently Exposed Fields rows (one per AC-named
    field when ACs enumerate output, display, response, or persisted
    fields)
  - Decisions: rows (decision, choice, source (file:line / ADR / doc,
    per the Knowledge Verification Chain order), scope (context the
    premise holds under), worst-case consumer file:line or `n/a` for
    non-numeric decisions, rationale -- when the choice fixes a numeric
    default, cap, or implicit upper bound, rationale must show derivation
    from the worst-case consumer)
  - Component Design: rows (component, file, action, responsibility)
  - Visual Design Considerations: bullets (only when designs/ exists)
  - Data Flow: numbered steps or mermaid; Cross-Task Value Trace rows
    (one per hop, when more than one task produces a value another
    task consumes)
  - Requirements Traceability: rows (requirement, component, file,
    status); expand to one row per field for multi-field ACs
  - Test Strategy: Infrastructure, Reference Tests, New Tests rows
  - Considerations: Error Handling rows, Security bullets, Risks, Rollout & Reversibility (only for risky cutovers)
  - Open Questions: checklist items
- Do NOT return: prose narration, process logs, dependency-inversion
  reasoning (silent per Step 12), Gotcha subsections (design-level
  gotchas with rationale go to Decisions; cross-feature gotchas go to
  `.artifacts/knowledge.md`)

Main agent composes `design.md` by writing Plan's chunks into the
design template (below) slots. Preserve template section order and
table shapes exactly. After writing, run Step 11's closing checklist
against
the composed artifact -- display each item as `[pass]` or `[fail]`. If
any item fails, re-dispatch Plan with the failure list as additional
brief context.

Main agent also updates spec.md status tags per Step 13 (change each
AC mapped in Requirements Traceability from `pending` to `in-design`).
Plan cannot perform this update because it is read-only; the write is
always main's responsibility regardless of dispatch.

_Steps 11-13 below describe the process Plan follows. Read them as
Plan's substeps when dispatched, or as main agent's process when
dispatch is skipped._

### Step 11: Data Model Definition

**Large/Complex only.** At Medium, capture only the entities the change touches
at a light grain — skip exhaustive member enumeration.

Define the data model before component design. Every statement about an existing type must cite `file:line` from the exploration's Member Enumeration.

- **Entities**: Every member the feature reads or writes, cited to `file:line`. Not "attributes" in the abstract -- the actual exposed members in source
- **Relationships**: How entities relate (one-to-many, many-to-many), with `file:line` for each referenced foreign key or join
- **Contracts**: Every member of every request, response, or projection the feature touches, cited to `file:line`. Not "shapes" -- enumerated members
- **Currently Exposed Fields**: If any acceptance criterion names specific output or display fields, fill the `Currently Exposed Fields` table in the design template (one row per AC-named field)
- **Reused Component Contracts**: If the feature reuses a shared component (UI component, service, module, class, hook, etc.) in an execution context or input shape that differs from existing consumers, fill the `Reused Component Contracts` table. One row per such component. Runtime preconditions, inputs this feature exercises, and defaults that activate for this input shape -- sourced by reading the component, not by trusting the name
- **Reused Utility Contracts**: For every shared utility the feature reuses, fill the `Reused Utility Contracts` table. One row per utility. Inputs, outputs, and internal rules (transforms, edge cases, output constraints) that shape the output -- sourced by reading the utility, not inferred from the name
- **Cross-Task Value Trace**: When the feature splits production and consumption of a value across multiple tasks, fill the `Cross-Task Value Trace` table inside `## Data Flow`. One row per hop. A reader must be able to reconstruct the value at every consumer without reading code

**Closing checklist — display each item as `[pass]` or `[fail]` before writing
design.md. Fix all `[fail]` items first. Do not run this check silently.**

Grounding (all scopes):

- [ ] Every Decision row has a non-empty Source grounded per the Knowledge Verification Chain order — a Source pointing to external/web with no codebase or docs anchor is a red flag
- [ ] Every Decision row has a Scope naming the context the premise holds under
- [ ] Every subsystem the design assumes present has a Subsystem Presence verdict anchored to wiring (`file:line`) — "documented" / "planned" does not satisfy it
- [ ] Every premise's Scope covers this feature's context — a premise true elsewhere but out of scope here is not applied
- [ ] Every integration-tool decision — a tech new to the codebase whose job is runtime wiring with existing config — cites an executed spike result against the real project config; external docs alone do not satisfy it
- [ ] No speculative component or abstraction (YAGNI screen): every entry in Component Design traces to an AC or a stated requirement; anything added for a hypothetical future need is removed

Member enumeration (Large/Complex):

- [ ] Every field named in any acceptance criterion has a row in `Currently Exposed Fields`
- [ ] Every Source cell cites a real `file:line`
- [ ] No Gap cell is blank (use "none" explicitly if no gap)
- [ ] Every "no change required" / "already returns" / "contract unchanged" claim in this section cites a `file:line` from the exploration's Member Enumeration
- [ ] Every type listed under Entities or Contracts matches a row in the exploration's Member Enumeration
- [ ] Every reused component listed in Component Design has a row in `Reused Component Contracts` when its execution context or input shape differs from existing consumers
- [ ] Every utility named in Component Design or Data Flow has a row in `Reused Utility Contracts`
- [ ] Every `Reused Component Contracts` and `Reused Utility Contracts` row has a real `file:line` in Source
- [ ] When more than one task produces a value another task consumes, `Cross-Task Value Trace` is populated with one row per hop
- [ ] Every Decisions row that fixes a numeric default, cap, or implicit upper bound has a non-empty `Worst-Case Consumer` cell with `file:line`
- [ ] If `spec.md` `origin: defect`: `## Root Cause` section is present with hypothesis cited to `file:line`, evidence (repro signal, stack/trace), confidence, and fix-type. If fix-type is `workaround`, the justification names the root defect, why root-fix is out of scope, and the follow-up reference
- [ ] If `spec.md` `origin: defect`: Decisions includes a row distinguishing the fix mechanism (root-fix vs workaround) with rationale -- never a defensive `try/catch`, fallback default, or silent recovery without explicit workaround labeling

### Step 12: Dependency Inversion Check (implicit)

**Large/Complex only.** Skip at Medium — a flat step list has no cross-story
ownership to invert.

Reason about this silently before writing design.md. Do not echo this check
into the artifact -- the design stays focused on the design, not on a process
log.

For each component, module, type, or primitive you are placing into a user story:

- Identify which user story *owns* it (the user story that introduces it)
- Identify every user story that *consumes* it
- The owning user story must be numbered ≤ the earliest consuming user story

If inverted -- owning user story has a higher number than a consuming user story --
resolve before writing, by picking one:

- **Relocate ownership**: move the component into the earliest consuming
  user story. Often the right answer for shared primitives that were mentally
  "grouped with their caller"
- **Reorder user stories**: if the primitive is conceptually a prerequisite, move
  its user story earlier in spec.md. Remember to keep user story IDs aligned with the
  new order
- **Inline then refactor**: leave the earlier user story shipping an inline
  implementation, and let the later user story's scope explicitly include the
  refactor to a shared primitive. Record this decision in Decisions so tasks
  can plan the refactor as an explicit task

Never let the design leave an inversion implicit. An inverted design produces
tasks whose commits do not stand alone, which breaks the per-story
commit-boundary contract that spec-driven relies on.

### Step 13: Generate design.md

Use the template (at the bottom of this reference) as the canonical
structure — it wins over any existing design. Do not read sibling specs
in `.artifacts/specs/` or anything in `.artifacts/archive/`; the only
cross-feature input is `.artifacts/knowledge.md`.

Generate the design following the template structure:
- Scope (what is in scope and out of scope)
- Root Cause (only when `spec.md` `origin: defect`; hypothesis at
  file:line + evidence + confidence + fix-type)
- Research Summary (if applicable)
- Patterns & Reuse (conventions to follow + existing code to reuse + Reused Component Contracts when applicable + Reused Utility Contracts + integration points with existing systems)
- Data Model (Entities, Relationships, API Contracts, Currently Exposed Fields when ACs enumerate fields)
- Decisions (architecture approach + secondary decisions; every decision records its Source — where it is grounded (codebase file:line, ADR, or project doc), per the Knowledge Verification Chain order — and its Scope, the context the premise holds under; any decision that fixes a numeric default, cap, or implicit upper bound must cite the worst-case consumer in the codebase that the value must satisfy, and the rationale must show derivation from that consumer -- never from a typical or lifted value)
- Component Design (component, file, action, responsibility)
- Data Flow (use mermaid for complex flows; Cross-Task Value Trace when more than one task produces a value another task consumes)
- Requirements Traceability (AC -> Component -> File; ACs enumerating N fields expand to N rows: field -> source file:line)
- Test Strategy
- Considerations (Error Handling, Security, Risks, Rollout & Reversibility for risky cutovers -- no Gotcha subsections)
- Open Questions

After generating design.md, update spec.md: for each AC mapped in Requirements Traceability,
change its status tag from `` `pending` `` to `` `in-design` ``.

### Step 14: Update Status

Set spec.md frontmatter: `status: ready`

### Step 15: Approval Gate

Present a summary:

```text
Design ready: `.artifacts/specs/{date}-{name}/design.md`
Decisions: {count} | Open questions: {count or "none"}

Approve to proceed, or describe changes.
```

Whether to stop here depends on the user's original request (see Specify Step 18 for the same rule):

- User asked only for design (rare): stop and wait.
- User asked for the full planning bundle ("plan and break into tasks", "turn this into a spec for us to implement", "figure this out and spec it", etc.): present this as a waypoint, then continue into `tasks`. Collect approval once at the end of planning.

If changes are requested: update design.md, then continue.

Do not start code-producing phases (`implement`) without explicit user approval regardless of the original phrasing.

## Guidelines

**DO:**
- Resolve open questions in the spec before designing
- Keep architecture decisions scoped to the feature
- Research unfamiliar technologies before committing to them
- Reference existing codebase patterns when available
- Follow Knowledge Verification Chain for all technical decisions
- Enumerate every member of every type the feature reads or writes, cited to file:line
- Cite file:line from the exploration's Member Enumeration for every claim about an existing type
- Expand multi-field acceptance criteria into one traceability row per field
- Read the source of every reused component and utility before filling its contract row -- preconditions, defaults, internal rules come from the code, not the name
- Trace cross-task values explicitly when one task produces and another consumes -- one row per hop in `Cross-Task Value Trace`
- Cite the worst-case consumer (file:line) for every numeric default, cap, or implicit upper bound -- derive the value from that consumer
- For `origin: defect` specs: produce `## Root Cause` with hypothesis at file:line, evidence, confidence, and fix-type before drafting Decisions
- For `origin: defect` specs: surface the fix mechanism (root-fix vs workaround) as a Decisions row -- the choice is design-level, not implementation-level

**DON'T:**
- Start designing with unresolved open questions in the spec
- Fabricate APIs or patterns -- verify first
- Over-architect beyond the feature scope -- screen speculative components and abstractions out (YAGNI)
- Sample touched types -- enumerate them
- Claim "already returns X" / "no additional join" / "contract unchanged" without a file:line anchor
- Collapse multi-field ACs into a single traceability row
- Add `### Gotcha` subsections to Considerations -- design-level gotchas with rationale go to Decisions; cross-feature gotchas go to `.artifacts/knowledge.md ## Gotchas`
- Substitute the Entities table for prose or bullets -- the table is the index; member enumeration goes in sub-blocks below
- Treat a reused component or utility as a black box (contrasts: read its source for preconditions, defaults, and internal rules)
- Lift a numeric default from an existing consumer's intrinsic value (contrasts: derive from the worst-case consumer with file:line)
- Reason at "checkbox" level about cross-task values ("isXUrl matches, so the path runs") (contrasts: simulate the actual transformation through every hop in `Cross-Task Value Trace`)
- Propose a defensive `try/catch`, fallback default, or silent recovery as the fix without diagnosing the cause first (contrasts: produce `## Root Cause` with file:line evidence, then either root-fix or labeled workaround with a follow-up)

## Design Template

ALWAYS use this exact template structure:

````markdown
---
name: {{name}}
status: draft
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
sources: []
---

# Technical Design: {{Feature}}

## Scope

{{What is in scope and out of scope for this feature}}

{{#if defect}}
## Root Cause

Required when `spec.md` has `origin: defect`. Investigation belongs to
design, not to the spec or the ticket. Hypothesis must be at file:line
granularity, anchored by reading the suspected sources -- not by
restating the symptom.

- **Hypothesis:** {{one sentence naming the wrong behavior at file:line — e.g., "expiry check uses `<` instead of `<=` at auth.ts:42, so boundary timestamps are rejected"}}
- **Evidence:**
  - Repro signal: {{log excerpt, failing test name, stack trace, observable behavior}}
  - First incorrect decision: {{file:line where the path diverges from the correct one}}
  - Supporting cites: {{additional file:line references that confirm the chain}}
- **Confidence:** {{high | medium | low}}
- **Fix type:** {{root-fix | workaround}}
- **Workaround justification (only if fix type is workaround):** {{why root-fix is out of scope, name of the root defect, follow-up reference (ticket id / spec id / knowledge.md entry)}}

The fix mechanism must appear as a row in `## Decisions` so the choice is
traceable. Never use a defensive `try/catch`, fallback default, or
silent recovery without an explicit workaround label.
{{/if}}

## Research Summary

{{#if research}}
> From .artifacts/research/{{topic}}.md

- {{key finding 1}}
- {{key finding 2}}
{{/if}}

## Patterns & Reuse

### Conventions to Follow

| Pattern | Project Uses | Avoid | Reference |
|---------|-------------|-------|-----------|
| Naming | {{convention}} | {{anti-pattern}} | {{file:line}} |
| Error handling | {{approach}} | {{anti-pattern}} | {{file:line}} |
| API calls | {{pattern}} | {{anti-pattern}} | {{file:line}} |

### Existing Code to Reuse

| Component | Location | How to Use |
|-----------|----------|------------|
| {{existing component}} | {{file:line}} | {{extend/import/wrap}} |

### Reused Component Contracts

Required when the feature reuses a shared component (UI component,
service, module, class, hook, etc.) in an execution context or input
shape that differs from existing consumers. One row per reused
component. Fields sourced by reading the component, not by trusting the
name.

| Component | Runtime Preconditions | Inputs Exercised | Defaults Activated for This Input Shape | Source (file:line) |
|-----------|----------------------|------------------|-----------------------------------------|--------------------|
| {{name}} | {{must run inside X / requires Y to be initialized / must be invoked from environment Z}} | {{inputs this feature passes — props, args, config, params}} | {{defaults that activate when called this way}} | {{file:line}} |

### Reused Utility Contracts

Required for every shared utility the feature reuses. One row per
utility. Internal rules sourced by reading the utility, never inferred
from the name.

| Utility | Inputs | Outputs | Internal Rules (transforms, edge cases, output constraints) | Source (file:line) |
|---------|--------|---------|-------------------------------------------------------------|--------------------|
| {{name}} | {{shape}} | {{shape}} | {{rules that shape the output — caps, multipliers, exclusions, branching, etc.}} | {{file:line}} |

### Integration Points

| System | Integration Method |
|--------|--------------------|
| {{existing API / service / DB / auth}} | {{how the feature connects}} |

## Data Model

### Entities

| Entity | Purpose |
|--------|---------|
| {{name}} | {{role in feature}} |

For each entity, enumerate the members the feature reads or writes:

#### {{Entity}}

- `{{memberName}}` ({{type}}) — {{path:line}}

### Relationships

{{Describe entity relationships. Use a mermaid erDiagram when relationships are non-trivial.}}

### API Contracts

| Endpoint | Method | Request | Response |
|----------|--------|---------|----------|
| {{path}} | {{verb}} | {{shape}} | {{shape}} |

### Currently Exposed Fields

Required when any acceptance criterion enumerates output, display,
response, or persisted fields. One row per AC-named field.

| AC ID | Field | Source (file:line) | Currently Exposed? | Gap? |
|-------|-------|--------------------|--------------------|------|
| {{AC-N}} | {{fieldName}} | {{path:line or "none"}} | {{yes / no}} | {{none / must add / must map}} |

## Decisions

{Non-obvious decisions only. If the choice is self-evident from the
spec, omit it. Every decision records its Source — where it is grounded
(codebase file:line, ADR, or project doc), following the Knowledge
Verification Chain order — and its Scope, the context the premise holds under.}

| Decision | Choice | Source (file:line / ADR / doc) | Scope | Worst-Case Consumer (file:line) | Rationale |
|----------|--------|--------------------------------|-------|---------------------------------|-----------|
| {{what was decided}} | {{what was chosen}} | {{where the decision is grounded — codebase file:line, ADR id, or project doc, per the Knowledge Verification Chain order}} | {{the context the choice holds under — e.g. client bundle, server runtime, this feature only}} | {{file:line of largest realistic consumer the value must satisfy, or `n/a` for non-numeric decisions}} | {{why this over alternatives — when the choice fixes a numeric default, cap, or implicit upper bound, the rationale must show the value derives from the worst-case consumer}} |

## Component Design

| Component | File | Action | Responsibility |
|-----------|------|--------|----------------|
| {{name}} | {{path}} | {{new/modify}} | {{what}} |

{{#if designs}}
## Visual Design Considerations

{{#each designs}}
- **{{filename}}**: {{design_decisions_based_on_image}}
{{/each}}

Key UI/UX patterns to implement:
- {{layout_patterns}}
- {{component_styles}}
- {{interaction_behaviors}}
{{/if}}

## Data Flow

{{Use a mermaid sequenceDiagram or flowchart when the flow involves 3+ steps or multiple actors.}}

1. {{Entry point}}
2. {{Transform}}
3. {{Output}}

### Cross-Task Value Trace

Required when more than one task produces a value another task
consumes. One row per hop. A reader must be able to reconstruct the
value at every consumer without reading code.

| Hop | Producer Task | Value Shape Out | Consumer Task | Transformation Applied at Consumer | Final Value Shape |
|-----|---------------|-----------------|---------------|------------------------------------|-------------------|
| 1 | {{T-X}} | {{shape produced}} | {{T-Y}} | {{what the consumer applies on top}} | {{shape after consumer}} |

## Requirements Traceability

> **Granularity rule:** If an acceptance criterion enumerates N fields,
> expand it into N rows — one per field, each with its own Source
> `file:line`. Coarse AC-level rows hide individual field gaps.

| Requirement | Component | File | Status |
|-------------|-----------|------|--------|
| AC-1 | {{comp}} | {{path}} | Planned |
| AC-2 | {{comp}} | {{path}} | Planned |

## Test Strategy

### Infrastructure

| Aspect | Detail |
|--------|--------|
| Framework | {{test runner}} |
| Command | {{test command}} |
| Location | {{test directory pattern}} |

### Reference Tests

| File | What It Tests |
|------|---------------|
| {{existing test}} | {{pattern to follow}} |

### New Tests

| Component | Test File | Scenarios |
|-----------|-----------|-----------|
| {{comp}} | {{path}} | {{what to test}} |

## Considerations

### Error Handling

- {{error scenario}}: {{how handled}}. User sees: {{user-visible impact or "none"}}.

### Security

- {{concerns if applicable}}

### Risks

- {{risk}}: {{impact if it happens}} — Mitigation: {{how addressed, or "accepted"}}

### Rollout & Reversibility

Only when this change is a user-visible cutover, migration, or behavior swap.
Omit otherwise.

- Cutover: {{what user-visible behavior changes}}
- Guard: {{feature flag, phased rollout, or none}} — {{why}}
- Rollback: {{how to revert if it goes wrong}}

## Open Questions

- [ ] {{question}}
````

## Error Handling

- Spec not found: Suggest `specify`
- Open questions blocking architecture: Suggest `discuss`
- Codebase unclear: Ask for guidance
