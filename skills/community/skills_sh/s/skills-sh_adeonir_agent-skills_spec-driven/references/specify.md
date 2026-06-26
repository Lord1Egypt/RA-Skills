# Specify Feature

Create a new feature specification with adaptive depth. Load
[status-workflow.md](status-workflow.md) for correct status management.

## Contents

- [When to Use](#when-to-use)
- [Content Separation (CRITICAL)](#content-separation-critical)
- [Arguments](#arguments)
- [Workflow](#workflow) — Steps 1-18
- [Codebase Mapping Note](#codebase-mapping-note)
- [Guidelines](#guidelines)
- [Spec Template](#spec-template)
- [Error Handling](#error-handling)

## When to Use

When creating a new feature spec or modifying an existing one.

## Content Separation (CRITICAL)

Each artifact has a distinct purpose. Never mix these concerns.

| File | Purpose |
|------|---------|
| spec.md | WHAT to build (requirements, acceptance criteria) |
| decisions.md | WHY certain decisions were made (discuss output, gray areas) |
| design.md | HOW to build (architecture, files, implementation) |
| tasks.md | WHEN to build (ordered tasks with dependencies) |

### spec.md MUST contain ONLY:

- Goals (measurable outcomes)
- Non-goals (explicit exclusions)
- Glossary (domain terms used in ACs, defined behaviorally; "None" when empty)
- User stories with acceptance criteria inline (AC-N IDs, EARS-lite shape 1:1 (no compound), status starts as `` `pending` ``)
- Edge cases (boundary conditions, error scenarios)
- Success criteria (measurable outcomes)
- For brownfield: current behavior description (high-level, no code)

### spec.md MUST NOT contain:

- Code snippets, identifiers, or field/enum names from the codebase (e.g., `mode: 'create'`, `reason: 'validation_error'`, `discountType === 'fixed'`)
- Component, hook, function, or class names (e.g., `PlanFormDrawer`, `usePlans`, `DangerZone`)
- File paths or directory structures (e.g., `src/components/ui/`)
- Technology or library choices (e.g., React, TanStack Form, shadcn, Radix)
- Implementation approaches (e.g., `useTransition`, `router.refresh()`, server actions)
- Database schemas or API designs
- Architecture decisions
- Milestones, epics, sprints, release names, or roadmap references (e.g., "part of Q2 epic", "blocked by milestone 3", "planned for v2")

These apply to ALL sections -- Overview, Goals, Non-Goals, Glossary, User Stories, ACs, Edge Cases, Success Criteria, Operational Follow-ups, Notes, Baseline. Behavior always trumps symbols.

These belong in design.md, created during the `design` phase.

## Arguments

- `[description]` - Feature description
- `[@file.md]` - Path to PRD/Design Doc file
- Greenfield: "create new feature for..."
- Brownfield: "modify feature...", "improve..."

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

Track each step as it completes — mark it done before moving to the next.
In Claude Code, create a task list at phase start (TaskCreate) and update
each step as it completes (TaskUpdate).

### Step 1: Assess Scope

Before anything else, determine complexity to auto-size the pipeline:

| Signal | Scope | Pipeline |
|--------|-------|----------|
| Mechanical change, zero decisions, outcome obvious from the description | **Small** | Redirect to [quick-mode.md](quick-mode.md) |
| Canonical pattern already in the codebase, no new abstraction needed | **Medium** | Specify -> Design (light) -> Tasks (light) -> Implement |
| ≥1 load-bearing decision new to the codebase (reviewer cannot predict approach from description) | **Large** | Specify -> Design -> Tasks -> Implement |
| Ambiguity in the problem itself, solution space open | **Complex** | Specify (+ Discuss) -> Design -> Tasks -> Implement (+ UAT) |

If **Small**: redirect to [quick-mode.md](quick-mode.md) and stop here.

Record the assessed scope in spec.md frontmatter as `scope: medium|large|complex`.
Small never reaches this file -- it redirects to quick-mode above, so `small`
is not a valid spec.md scope value.

This is the first-pass size on the raw input, and it is **provisional**: Step 9
recalibrates it after discovery, when the load-bearing decisions are visible. Do
not treat the Step 1 size as final, and do not let it anchor the recalibration.

### Step 2: Check Project Context

Load whatever project context exists:

| Context Found | Action |
|---------------|--------|
| `CLAUDE.md` exists | Use `## Project` and `## Architecture` as context for discovery |
| `.artifacts/codebase/{area}.md` cache exists | Use for brownfield pattern matching in that area |
| Neither exists (greenfield) | Proceed without — project context is optional for new projects |
| Neither exists (brownfield) | Scan a few representative files when discovery needs codebase context |

### Step 3: Ensure Spec Structure

Check if `.artifacts/specs/` parent exists. If not:

```bash
mkdir -p .artifacts/specs
```

### Step 4: Derive Spec Directory Name

The directory is `{YYYY-MM-DD}-{name}`: the creation date (the same value
written to `created` in the spec frontmatter) plus the feature slug. No
counter, no scan. If `.artifacts/specs/{YYYY-MM-DD}-{name}/` already
exists (same name, same day), suffix the slug (`{name}-2`).

### Step 5: Determine Type (Greenfield vs Brownfield)

**Greenfield triggers:**
- "create new feature"
- "new feature"
- "implement from scratch"

**Brownfield triggers:**
- "modify feature"
- "improve"
- "refactor"
- "extend"

If ambiguous, ask user.

### Step 6: Process Input

**If input is a file (@file.md):**

Extraction is **transformation**, not copying. Source documents define
product-level or system-level requirements; the spec defines feature-level,
implementation-ready requirements. Every item must be narrowed to feature
scope and refined with implementation detail.

| Source (PRD/Design Doc) | spec.md |
|-------------------------|---------|
| Product-wide user stories | Feature-scoped user stories prioritized by implementation order (P1/P2/P3) |
| Directional requirements (must/should/could) | Implementable FRs with measurable criteria |
| High-level acceptance criteria | Testable ACs in EARS-lite shape (1:1, no compound) |
| Product KPIs and success metrics | Feature-specific success criteria (demo-able) |
| No edge cases | Edge cases (boundaries, errors, invalid inputs) |

1. If path is a directory, list all files: `find {path} -type f -name "*.md"`
2. Read each file completely -- extract rules ("must", "cannot", "always"),
   constraints ("only if", "when", "unless"), and examples
3. Filter each item: relevant → transform; not relevant → note WHY in Notes;
   partially relevant → extract only the applicable part
4. Transform (never copy verbatim): narrow broad user stories to feature scope, make
   ACs testable (EARS-lite shape, 1:1), add missing edge cases and success criteria
   derived from requirements
5. Output extraction summary in Notes section before generating spec -- the
   "Transformed To" column must show the refined version, not a copy

**If input is text:**
- Use as feature description

**If input is empty:**
- Ask user for feature description

**Record sources:**

`sources:` is the spec's list of durable external references it points to
instead of duplicating their content -- input file paths (`@file.md`, a PRD
or Design Doc path), tracker ticket IDs or URLs, design-artifact paths. One
entry per source. A clean session follows these to recover context the spec
deliberately did not copy, so they are the pointer half of the handoff
(`## Session Context` holds what has no durable source). Record every input
that defined this spec here as you process it; leave `[]` only when nothing
durable defines the work -- the content lived only in conversation and must
go to `## Session Context` instead.

**Snapshot the raw input:**

Beyond the `sources:` pointer, the raw input that defined this spec is frozen
verbatim into `inputs/` (written at Step 12). Three homes, three jobs, no overlap:

- `sources:` -- a *pointer* to where the live source lives; it may drift or move.
- `## Session Context` -- *distilled* prompt-only material with no durable source.
- `inputs/` -- the *raw, verbatim* copy of what was ingested, kept frozen so a
  later audit can check the delivered feature against the original source, not only
  the spec. Distinct from `designs/` (visual references) and `design.md` (the
  technical design doc).

**Detect defect origin:**

The spec captures WHAT to build, including for fixes. When the input
originates from a defect, the spec must be framed around the correct
behavior (the root), not the absence of a symptom.

Defect signals (apply when any match):
- Input file is a bug or issue ticket artifact
- Input file frontmatter has `type: bug` or `type: issue`
- Description contains defect keywords: `fix`, `bug`, `error`,
  `broken`, `regression`, `crash`, `falha`, `quebrou`,
  `não funciona`, "stopped working", "throws", "fails"

When defect signals match:
- Set frontmatter `origin: defect` (default `origin: feature`)
- Frame Goals around the correct behavior, not the absence of a
  symptom. Prefer "Token expiry check accepts boundary timestamp" over
  "Users no longer see login errors at boundary times". The first
  defines the root; the second defines the symptom.
- Each AC asserts the correct behavior, including for the case that
  used to fail. Symptom-only ACs ("no 500 in logs", "no toast appears")
  are insufficient on their own -- pair with a behavior AC.

Investigation of the cause is NOT performed in specify -- that work
belongs to design (Large/Complex) or to Step 6 Diagnose in quick-mode
(Small). Specify captures the problem and the success behavior; the
how comes later.

### Step 7: Feature Discovery

Load [discovery.md](discovery.md) and conduct feature discovery. If input came
from a file (@file.md), pass the extracted content as starting context so
discovery can skip questions already answered by the document.

### Step 8: Baseline Discovery (Brownfield)

If type is `brownfield`:

1. **Analyze current behavior from user perspective** (not implementation details):
   - What users can currently do
   - Current workflows and limitations
   - What needs to change

2. **Behavior only -- no file paths, no component/hook names:**

   | Include | Exclude |
   |---------|---------|
   | What users can do | File paths |
   | Current limitations | Function names |
   | Behavior gaps | Code snippets |
   | User-facing issues | Technical implementation |

3. **Add Baseline section to spec.md:**

   ```markdown
   ## Baseline

   ### Current Behavior
   - Users can currently do X
   - System behaves like Y
   - Limitation: Z

   ### Gaps / Limitations
   - Missing: A
   - Problem: B
   - Improvement needed: C
   ```

If no `.artifacts/codebase/{area}.md` cache exists for the area:
- Scan a few representative files for brownfield context
- Proceed with limited codebase understanding if that is enough

### Step 9: Recalibrate Scope

Discovery has now surfaced the load-bearing decisions the raw input hid. Re-size
before the spec binds. Load [auto-sizing.md](auto-sizing.md) and run its
**Recalibration Gate**: enumerate the load-bearing decisions, classify each as
canonical or novel to the codebase with evidence, default novel when novelty
cannot be ruled out, and derive the size from that enumeration — independently of
the Step 1 size.

Run the gate inline (see auto-sizing.md "Running it"): re-derive the load-bearing
decision list from scratch and only then compare against the Step 1 size, so the
first pass does not lead the enumeration. This is a re-classification, not a review
of a written artifact, so it does not warrant an isolated subagent.

Reconcile against Step 1:

- Gate size higher → **escalate** and carry the new size forward (Step 14 Propose
  Approaches now runs if the size reached Large/Complex).
- Agreement → **confirm**.
- Lower → **de-escalate only** with positive evidence that every decision is
  canonical (`file:line` or area-cache anchor); otherwise hold the higher size.

Set frontmatter `scope` to the reconciled size. Record the verdict (confirmed,
escalated, or de-escalated) and the load-bearing decisions that drove it as a row
in `## Decisions`.

If the gate escalates to **Complex**, note any gray areas as Open Questions and
suggest [discuss.md](discuss.md), consistent with discovery's Gray Area Detection.

### Step 10: Generate Feature Name

Convert description to kebab-case:
- "Add user authentication" -> `add-user-auth`

### Step 11: Ask About Branch

Default suggestion is a new branch. Record the user's choice in `branch:` frontmatter only — the branch is created at implement start, not here.

```text
Branch for this feature?
1. New branch: feature/{name} (recommended)
2. Current branch ({current-branch})
3. Other (specify name)
```

- Whichever option the user picks, store the resolved branch name in spec.md frontmatter.
- Do not run `git checkout` or `git switch` in this step. Branch creation belongs to implement.md.

### Step 12: Create Spec Directory

```bash
mkdir -p .artifacts/specs/{date}-{name}
```

Snapshot the raw input into `inputs/` -- the frozen copy the audit oracle reads
(distinct from the `sources:` pointer; see Step 6). Non-destructive copy only:

```bash
mkdir -p .artifacts/specs/{date}-{name}/inputs
cp -R {input-path} .artifacts/specs/{date}-{name}/inputs/   # @file.md or a directory of docs
```

When the input was conversational (no file), write the prompt or ticket text
verbatim to `inputs/prompt.md` instead. Skip the snapshot entirely when nothing
durable defined the spec (the `sources: []` case).

### Step 13: Include Visual References

Check if the prompt includes images (screenshots, mockups, wireframes, diagrams):

**If images are present:**
1. Create `designs/` subdirectory:
   ```bash
   mkdir -p .artifacts/specs/{date}-{name}/designs
   ```
2. Save each image to the designs folder with descriptive filenames:
   - `{brief-description}.{ext}` (e.g., `login-screen.png`, `user-flow.jpg`)
3. Images will be referenced in spec.md section "Visual References"

**If no images:**
- Skip this step (designs/ folder is optional)

### Step 14: Propose Approaches (Large/Complex only)

Skip for Small and Medium scope.

For **Large** and **Complex** features, before drafting the spec present 2-3 architectural
approaches with trade-offs. Lead with your recommendation and the reason. Keep each
option to 3-4 sentences. Wait for user to choose before proceeding.

Example structure:

```text
**Option A (recommended):** {approach} — {why it fits, trade-off}
**Option B:** {approach} — {why it fits, trade-off}
**Option C:** {approach} — {why it fits, trade-off}
```

Do not draft spec.md until user confirms an approach. Record the chosen approach in
spec.md Notes section.

### Step 15: Generate spec.md

Use the template (below) as the canonical structure — it wins over any
existing spec. Do not read sibling specs in `.artifacts/specs/` for shape
or decisions, and never read `.artifacts/archive/`: archived specs are
superseded and out-vote both the template and the current spec. The only
cross-feature input a new spec draws on is `.artifacts/knowledge.md`.

Generate the spec following the template structure:
- Frontmatter with feature name, type, scope, status, review, branch, created date
- Greenfield: Overview, Goals, Non-Goals, Glossary, User Stories (with ACs inline), Edge Cases, Success Criteria, Operational Follow-ups, Open Questions, Notes
- Brownfield: Same structure plus Baseline section (Current Behavior, Gaps/Limitations)
- **If images were saved to designs/**: Include Visual References section with markdown image references (e.g., `![Description](designs/filename.png)`)

Each user story includes "Why Px" to justify its priority level. P1 user stories must be vertical slices -- complete, demo-able features (not just backend or frontend). Each P1 user story includes an Independent Test. Acceptance criteria are inline per user story with AC-xxx IDs for traceability.

#### Pre-write checklist

Before writing spec.md, display the result of every item below — show `[pass]` or
`[fail]` for each line. Fix all `[fail]` items before writing. Do not run this
check silently.

- [ ] No code identifiers in ACs or Edge Cases (no `mode: 'create'`, no `===`, no field or enum names)
- [ ] No technology or library names anywhere (no React, TanStack, shadcn, Radix)
- [ ] No component, hook, function, or class names from the codebase
- [ ] No file paths or directory names
- [ ] Non-Goals entries describe behavior, not code symbols
- [ ] Notes contains only behavioral context -- no HOW, no libraries, no component names
- [ ] No milestones, epics, sprints, release names, or roadmap references anywhere
- [ ] Every non-functional claim is quantified (e.g. `p95 ≤ 200ms`) or demoted to an Open Question — no vague "fast", "scalable", "responsive"
- [ ] Each user story is a commit boundary: no AC depends on work belonging to a later user story (move it if so)
- [ ] No speculative Goal or User Story (YAGNI): each solves a present need within the Success Criteria; speculative items moved to Non-Goals, not Open Questions
- [ ] Baseline (if brownfield) describes user-observable behavior, not code structure
- [ ] If origin=defect: Goals name the correct root behavior, not the absence of a symptom; every defect AC asserts correct behavior (symptom-only ACs are paired with a behavior AC)
- [ ] the scope verdict (confirmed/escalated/de-escalated) and the load-bearing decisions that set the scope appear in `## Decisions`
- [ ] Every agent gap-fill is in `## Assumptions` as `agent-assumed` — none left as a stated fact in Goals, User Stories, or ACs
- [ ] `discovery:` provenance is resolved to `human` or `autonomous-assumed` (not the placeholder)

If any box fails: rewrite the offending lines behaviorally, or move HOW content to design.md. Never ship a spec that leaks design.

### Section Rules

**Goals:** 2-4 per feature (more signals scope creep). Each goal must map to at least
one Success Criterion. Future-tense observation windows ("for N days after deploy",
"in the period following launch") are not verifiable at audit time -- keep the
architectural/instrumentation claim in Goals and move the observation window to
`## Operational Follow-ups`.

**User Stories:** All user stories WILL be implemented. Priorities define implementation
order, not whether something ships. Each user story is a commit boundary -- an AC that
requires work from a later user story must be moved to that user story. Watch for narrative vs
build order inversions: if a user story defines a reusable primitive that an earlier-numbered
user story consumes, the inversion breaks the commit-boundary contract. Fix by moving the
primitive's user story earlier, merging it into the first consumer, or making the earlier
user story ship an inline implementation that the later user story refactors into the shared
primitive. Never leave the inversion implicit.

**YAGNI screen:** Before finalizing Goals and User Stories, screen each against present
need. A Goal or User Story that adds complexity for a hypothetical future need, solves a
problem that does not exist yet, or reaches beyond the Success Criteria is speculative --
move it to Non-Goals with the reason. Do not route it to Open Questions: an Open Question
may return, and spec-driven ships every User Story it keeps, so the screen happens here,
before the spec binds, not at implementation.

**User-facing flag:** Set `user-facing: true` when the feature delivers something that
needs **visual approval** — a screen, layout, component, button, copy/text, visual
state, or flow the user sees: what an automated test confirms *functions* but not that
it *looks or reads right*. Set `false` for backend, API, data, infrastructure, library,
or logic work with no such surface — correctness there is fully verifiable by automated
tests (which the audit re-run already enforces), so there is nothing for a human to
approve by sight. Test: would a human need to look at this and approve that it is
visually and textually correct and the UX makes sense? Notification, email, or CLI text
a human reads counts (it is copy to approve); pure machine-to-machine output does not.
The flag gates whether UAT is required before `done` — when in doubt, `true`.

**Acceptance Criteria:** Use EARS-lite — one of five clause shapes, 1:1 per AC, no
compound clauses. The shape names how the requirement is triggered; the sentence
states one observable obligation:

```text
Ubiquitous:  The system shall {action}.
Event:       When {trigger}, the system shall {action}.
State:       While {state}, the system shall {action}.
Optional:    Where {feature}, the system shall {action}.
Unwanted:    If {unwanted condition}, then the system shall {mitigation}.
```

One trigger, one outcome per AC. Each AC maps to a test downstream — that
mapping lives in the tests, not the spec.
Happy paths go in ACs; boundary conditions go in Edge Cases. AC IDs are monotonic
and never reused: removing an AC retires its ID with a tombstone entry — status
`removed` plus a one-line reason — instead of renumbering, so existing task and
test references stay stable. A retired AC keeps its line, e.g.:

```text
- AC-3 `removed`: folded into AC-1
```

When an AC references a third-party audit tool, append
an `Audit-tool measurement` sub-bullet:

```markdown
- [ ] AC-1: When {trigger}, the system shall {observable outcome}
  - **Audit-tool measurement:** {tool name} -- {exact metric the tool reports} -- pass threshold: {numeric or boolean}
```
Required only when the AC references a third-party audit tool. Omit the sub-line otherwise.

**Non-functional criteria:** Any performance, latency, throughput, capacity, or
availability claim must carry a number and the condition it holds under (`p95 ≤ 200ms
under 50 RPS`), or it is not an acceptance criterion — demote it to an Open Question.
Vague adjectives ("fast", "scalable", "responsive") are not testable and never ship as ACs.

**Glossary:** Define every domain term that appears in an AC, behaviorally — no code
identifiers, libraries, or component names. Write "None" when the feature introduces no
domain vocabulary. This is where Spec Review confirms each term is defined.

**Operational Follow-ups:** Plain bullets (no `[ ]` -- the absence of a checkbox makes
the non-gating intent explicit). Use "None" if every criterion is pre-merge verifiable.
Never duplicate items that also appear in Goals or Success Criteria.

**Notes:** Same behavior vs symbol filter as the rest of the spec -- no libraries, no
paths, no component or hook names. Omit the section entirely if there is nothing
behavioral to capture beyond what other sections already cover. Boundary vs Session
Context: Notes holds surrounding evidence (stakeholders, deadlines, prior art);
Session Context holds prompt-only material that *defines* the work (content/copy,
constraints, clarifications). Unverified premises go to `## Assumptions`. If losing it
would change what gets built, it is Session Context, not Notes.

**Decisions and Session Context:** Both sections are always present -- the durable home for
context settled during specify that would otherwise live only in chat. `## Decisions`
captures choices made among alternatives at the specify grain (scope, requirements,
product behavior); `## Session Context` captures content, constraints, and clarifications
(unverified premises go to `## Assumptions`).
Boundary: design.md runs at every scope above Small, so technical and architecture
decisions go in its `## Decisions` instead -- spec.md stays at the specify grain,
design.md owns the implementation grain, no duplication. When discuss.md runs (Complex
gray areas), its resolutions stay there; record only their downstream effect on scope or
requirements here. Fill from this conversation, or write "None" when a `sources:` pointer
covers it. Never delete either section -- an explicit "None" asserts nothing was lost; a
missing section is an omission.

**Assumptions:** The durable ledger of unverified premises the build rests on, always
present (`None` when empty). Each row carries an **origin**: `user-hypothesis` (the user
asserted it as fact without evidence -- the old "mark as hypothesis") or `agent-assumed`
(the agent filled a gap the human did not answer). Anti-fabrication rule: an
`agent-assumed` premise is recorded here, never written as a stated fact in Goals, User
Stories, or ACs. A load-bearing assumption that cannot be confirmed without the user is
also raised as a `[blocking]` Open Question, so it gates the build instead of riding
silently. The "How it gets confirmed" column gives audit and UAT a target.

**Open Questions:** Each unresolved item is tagged `[blocking]` (the build cannot
proceed -- a design or implement decision depends on the answer) or `[deferrable]`
(captured, resolved later, build proceeds). Discovery sets the tag with the context it
has. A `[blocking]` question does not stop spec *creation*, but it surfaces at the
approval gate and halts the phase it bears on -- design and implement read the tag.
Write "None" when all resolved.

### Step 16: Spec Review

The spec's own review gate — there is no separate review file. It runs two passes
over the drafted spec.md and records one verdict in frontmatter `review:`:

- **16a Coverage Review** — what is missing from the requirement set
- **16b Shape Review** — whether what is present is well-formed

Run 16a before 16b: coverage may add requirements, and those additions must pass
the shape checks. Set the verdict from both passes:

- Both clear (no unresolved gap, every shape check `[pass]`) → `review: pass`
- Any unresolved gap or `[fail]` → `review: changes`; report the failing lines,
  resolve or fix them, re-run both passes until `pass`

The review verdict gates specify's own approval gate (Step 18), not the downstream
phases — a spec edited after review resets `review` to `pending` and must be
re-reviewed before that gate.

### Step 16a: Coverage Review

The first pass checks what is *missing* — the requirement-set gaps every
downstream gate is blind to, because verify and audit trace against the spec and a
requirement absent from it has nothing to trace. This is coverage, not
completeness: it cannot prove the set is complete; it hunts known classes of
incompleteness along lenses answerable from the spec's own contents, so it
survives a PRD handed off with no human to answer discovery.

**Dispatch.** Independence is the point — whoever drafted the spec is blind to what
they did not think of. Dispatch an isolated subagent that reads the drafted spec
fresh, framed adversarially ("assume gaps exist; find them"). Run inline only when
subagent support is unavailable.

Subagent brief (task-specific input, no conversation history):

- `.artifacts/specs/{date}-{name}/spec.md` (the draft)
- The discovery synthesis and the input `sources:` (PRD / ticket)
- `.artifacts/codebase/{area}.md` cache if it exists — to judge precedent
  ("a delete exists elsewhere, so its absence here is a real gap")
- The lenses below

**Lenses.** Depth scales with scope, like the design and tasks Plan dispatch: at
**Medium** the subagent runs light — only the three a canonical reapplication still
tends to drop (happy↔failure symmetry, CRUD/lifecycle symmetry, actor coverage); at
**Large/Complex** it runs all six. Select only those that apply (a data migration
skips actor and state); each is answerable from the spec's contents.

| Lens | Asks |
|------|------|
| Happy↔failure symmetry | Every AC that touches network, input, or a dependency has a stated behavior for the failure path |
| Lifecycle / CRUD symmetry | A create has a delete, an enable a disable — where the domain implies the pair |
| State-transition closure | Every state an entity can enter has a stated way out; no orphan state |
| Actor coverage | Every named actor has its path specified, and its boundary — what it must not do |
| Goal sufficiency | Every Goal is actually served by its requirements, not just nominally linked to one tangential AC |
| Implicit precondition | No AC assumes a precondition that nothing in the spec establishes |

Return shape (structured, no prose): per applied lens, `covered` or a list of
candidate gaps, each with the spec evidence that triggers it (the AC, Goal,
entity, or actor).

**Forcing function.** Every candidate gap lands in exactly one destination — never
dropped silently:

- **add** → a new user story or AC (authored in EARS-lite shape, checked by 16b)
- **exclude** → a Non-Goal row, with the reason
- **defer** → an Open Question, with the reason

An unresolved gap holds the verdict at `review: changes` (see Step 16). When this
pass adds requirements, 16b shape-checks them on the same loop.

This pass hunts known gap-classes; it does not catch a requirement nobody
conceived. Conceptual gaps still surface only through discovery or UAT.

### Step 16b: Shape Review

Review the written artifact against the criteria below — the shape of what is
present, including anything 16a added. Show `[pass]` or `[fail]` per line.

- [ ] Every AC matches one EARS-lite shape (ubiquitous, event, state, optional, unwanted)
- [ ] Every AC is atomic — one trigger, one outcome, no compound "and"
- [ ] Every AC is testable — a concrete test is describable without guessing intent
- [ ] Every Goal maps to at least one Success Criterion
- [ ] Every domain term used in an AC is defined (no undefined jargon)
- [ ] Open Questions are each resolved or explicitly deferred with a reason

Failing lines feed the `review:` verdict in Step 16.

### Step 17: Handoff Completeness Gate

Before presenting the spec as ready, confirm self-sufficiency:

> Could a clean session implement this from `spec.md` plus its `sources:`
> alone? If anything that bears on implementation was settled only in this
> conversation -- a decision, content/copy, a constraint, a clarification --
> capture it in `## Decisions` or `## Session Context` now. If it lives in a durable
> source the project already tracks, record a `sources:` pointer instead of
> duplicating.

The artifact is the only thing the next session sees. If it is only in
chat, it does not exist.

### Step 18: Approval Gate

Present a summary:

```text
Spec ready: `.artifacts/specs/{date}-{name}/spec.md`
Type: {greenfield|brownfield} | Scope: {medium|large|complex} ({confirmed|escalated|de-escalated})
Review: {pass|changes} | Open questions: {count} ({N blocking}) | Gray areas: {yes/no}
Discovery: {human|autonomous-assumed} | Assumptions: {count} ({N agent-assumed})

Approve to proceed, or describe changes.
```

List every `[blocking]` Open Question and every `agent-assumed` assumption explicitly
under the summary -- these are the unresolved premises the user approves over, not just
a count.

Whether to stop here depends on what the user actually asked for. Read the original request:

- **User asked for the spec only** (e.g. "write a spec", "capture the requirements", "draft what this feature should do") -- stop at this gate and wait for approval.
- **User asked for the full planning bundle** (e.g. "plan this out", "plan and break into tasks", "turn this into a spec for us to implement", "design this", "break into tasks", "figure this out and spec it", provides a PRD and asks to "turn this into something we can execute") -- do not stop. Present this summary as a waypoint, then continue the pipeline through the final planning phase the scope requires. Approval is collected once at the end of planning, not at every phase boundary.

Apply the pipeline by scope once you have decided to continue:

- Small: Quick mode handles the whole job -- Specify was not invoked. If you are reading this, the scope assessment was wrong; back out and route through `quick-mode`.
- Medium: Specify → `design` (light) → `tasks` (light), then wait for user go before `implement`
- Large: Specify → `design` → `tasks`, then wait for user go before `implement`
- Complex: Specify → (`discuss` if gray areas) → `research` (if new tech) → `design` → `tasks`, then wait for user go before `implement`

Approval gates catch user disagreement; they do not re-checkpoint every phase when the user already asked for the whole planning bundle. When the request clearly means "the full plan, starting from the spec," continue through the pipeline and collect approval once at the end.

If changes are requested at any gate: update the relevant artifact, re-run its pre-write checks, then continue.

Do not start `implement` (code-producing phases) without explicit user approval regardless of the original phrasing.

## Codebase Mapping Note

The `.artifacts/codebase/{area}.md` cache holds reusable area-level
exploration (patterns, integration points) from prior features.
**Baseline in specify** captures specific current behavior relevant to
this feature.

They complement each other:

- Area cache: macro view (the area, reused across features)
- Baseline discovery (Step 8): micro view (this feature only)

## Guidelines

**DO:**
- Validate feature scope before creating the spec
- Mark unclear requirements as TBD rather than inventing constraints
- Keep one feature per spec -- split if scope is too broad
- Auto-size correctly based on actual complexity

**DON'T:**
- Include technical solutions in spec (that belongs in design)
- Force Large pipeline on Medium features
- Invent constraints when requirements are unclear

## Spec Template

ALWAYS use this exact template structure:

````markdown
---
name: {{name}}
scope: {{medium|large|complex}}
type: {{greenfield|brownfield}}
origin: {{feature|defect}}
user-facing: {{true|false}}
discovery: {{human|autonomous-assumed}}
status: draft
review: pending
uat: pending
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
branch: {{branch-name or main}}
sources: []
---

# Feature: {{Title}}

## Overview

{{Problem description: what pain point are we solving, who is affected, why now}}

## Goals

- [ ] {{Primary goal with measurable outcome}}
- [ ] {{Secondary goal with measurable outcome}}

## Non-Goals

| Feature | Reason |
|---------|--------|
| {{feature}} | {{why excluded}} |

## Glossary

{{Domain terms used in the acceptance criteria, defined behaviorally. Write "None"
when the feature introduces no domain vocabulary.}}

- **{{Term}}** — {{definition, no code identifiers, libraries, or component names}}

## User Stories

### US-1 [P1] {{User Story Title}}

- As a {{user}}, I want {{goal}} so that {{benefit}}
- **Why P1:** {{why this is critical for MVP}}
- **Independent Test:** {{how to verify this user story works alone}}

**Acceptance Criteria:**

- [ ] AC-1 `pending`: When {{trigger}}, the system shall {{observable outcome}}
  - **Audit-tool measurement:** {{tool name}} — {{exact metric}} — pass threshold: {{numeric or boolean}}
- [ ] AC-2 `pending`: While {{state}}, the system shall {{observable outcome}}

### US-2 [P2] {{User Story Title}}

- As a {{user}}, I want {{goal}} so that {{benefit}}
- **Why P2:** {{why this matters but is not MVP}}

**Acceptance Criteria:**

- [ ] AC-3 `pending`: The system shall {{observable outcome}}

### US-3 [P3] {{User Story Title}}

- As a {{user}}, I want {{goal}} so that {{benefit}}
- **Why P3:** {{why this is nice-to-have}}

**Acceptance Criteria:**

- [ ] AC-4 `pending`: If {{unwanted condition}}, then the system shall {{mitigation}}

{{#if designs}}
## Visual References

{{#each designs}}
![{{description}}](designs/{{filename}})
{{description of what this image shows}}

{{/each}}
{{/if}}

## Edge Cases

- If {{boundary condition}}, then the system shall {{observable handling}}
- If {{error scenario}}, then the system shall {{graceful handling}}
- If {{unexpected input}}, then the system shall {{validation response}}

## Success Criteria

- [ ] {{Measurable outcome — e.g., "User can complete X in under 2 minutes"}}
- [ ] {{Measurable outcome — e.g., "Zero errors in Y scenario"}}

## Operational Follow-ups

Post-deploy observations, monitoring windows, or runbook tasks that
cannot be verified at audit time. Recorded here so the spec captures
intent, but **not audit targets** — audit only checks Goals and Success
Criteria.

- {{Operational item, e.g., "Post-deploy monitoring: zero rejections in payment flow over 7 days"}}
- {{or write "None" if every criterion is pre-merge verifiable}}

## Open Questions

{{Each tagged `[blocking]` (build cannot proceed without it) or `[deferrable]`
(resolve later). Write "None" if all resolved.}}

- [deferrable] {{unresolved question}}

## Decisions

{{Choices settled during this conversation that a clean session could not
reconstruct from the spec or its `sources:`. Omit self-evident rows;
write "None" when every choice is obvious or covered by a `sources:`
pointer. At Large/Complex this is usually "None" -- technical and
architecture choices belong in design.md.}}

| Decision | Choice | Rationale |
|----------|--------|-----------|
| {{what was decided}} | {{what was chosen}} | {{why this over alternatives}} |

## Session Context

{{Material that defines the work but lives only in this conversation, not
in a `sources:` pointer — content/copy to implement, user-stated constraints,
clarifications that resolved ambiguity. Write "None" when a `sources:` entry
covers it. Unverified premises go to `## Assumptions`, not here.}}

- {{captured item, or "None"}}

## Assumptions

{{Unverified premises the build rests on, tagged by origin. Always present;
write "None" when empty.}}

| Assumption | Origin | How it gets confirmed |
|------------|--------|-----------------------|
| {{premise}} | {{user-hypothesis / agent-assumed}} | {{test / UAT scenario / ask user / metric}} |

## Notes

{{additional behavioral context — evidence, stakeholders, deadlines; never technology choices, component names, or file paths}}

{{#if brownfield}}
## Baseline

### Current Behavior

- {{What users observe today — no component names, no code identifiers}}

### Gaps / Limitations

- {{What's missing or problematic, described as user impact}}
{{/if}}
````

## Error Handling

- No project structure: Initialize project first
- ID conflict: Regenerate ID
- Branch exists: Offer to checkout existing
- Scope misjudged: Safety valve in implement catches this
