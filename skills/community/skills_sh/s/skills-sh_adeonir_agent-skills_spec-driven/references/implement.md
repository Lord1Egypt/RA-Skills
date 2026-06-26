# Implement Tasks

Implement, verify, and complete tasks. Verification happens
continuously — after each task or range, never deferred to the end.
Load [status-workflow.md](status-workflow.md) for correct status
management.

## Contents

- [When to Use](#when-to-use)
- [Arguments](#arguments)
- [Workflow](#workflow) — Steps 1-8
- [Edge Case Verification](#edge-case-verification)
- [Final Verification](#final-verification)
- [Guidelines](#guidelines)
- [Error Handling](#error-handling)

## When to Use

When implementing tasks from a feature's tasks.md.

Start with a clean context window. Load artifacts from disk (spec.md, design.md,
tasks.md), not from a previous phase's conversation context. See SKILL.md Phase
Transitions.

## Arguments

**Selection** (what to implement):

- `[T-1]` - Single task
- `[T-1..T-5]` - Range
- `[US-1]` - All tasks under user story US-1
- `[--all]` - All pending
- Empty - Next pending task

**Commit behavior:**

- Default (no flag) - implement the selection, then stop and announce it is
  ready for review/commit. No commit is made; the human commits.
- `[--commit]` - auto-commit each boundary the selection fully completes.
- `[--all]` implies `[--commit]` - walking all pending work is always
  auto-committed.

Default commit granularity is one commit per user story. A prompt instruction
("atomic commits per task") overrides it for the run.

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

Track each step as it completes — mark it done before moving to the next.
In Claude Code, create a task list at phase start (TaskCreate) and update
each step as it completes (TaskUpdate).

### Step 1: Resolve Feature

1. If a feature name is given -> match `.artifacts/specs/{date}-{name}/` (glob `*-{name}` or `*-{name}-*` for a collision variant)
2. If no feature name -> match current git branch to `branch:` in spec.md frontmatter
3. If multiple or no match -> list available specs and ask user

If a user story ID argument was given (`[US-1]`):
- Read tasks.md, find the `### US-1 ...` section
- Collect all tasks under that section header
- Treat them as the task range for this run

### Step 2: Load Context

Read `spec.md` in full -- acceptance criteria, plus `## Decisions` and
`## Session Context` for choices, content, and constraints settled during specify
that the spec body alone does not carry. Follow any `sources:` pointer to
its durable source before coding. Read `design.md` (decisions with Source/Scope,
patterns, component design) and `tasks.md` (the steps to execute).
If `.artifacts/knowledge.md` exists, read it for project-level decisions and gotchas.

**Blocking-question gate:** If spec.md `## Open Questions` holds any `[blocking]`
question, halt: list the blocking items, route to [discuss](discuss.md) or the user to
resolve, then exit. `[deferrable]` questions do not gate; proceed. For an untagged
legacy spec, judge whether a question would change what you are about to build.

Implement always runs in **Full mode**: spec + design + tasks all exist (every
scope above Small produces them). Follow tasks.md. There is no inline
step-derivation or codebase scanning in implement -- discovery, research, and
grounding happened in design; implement executes and verifies.

**Grounding gate (paper check, no codebase reads):** confirm the design is
grounded on its face before executing — verification was design's job, not
implement's. Halt and route back to `design` if any holds:

- a Decision has a blank Source or Scope
- a Decision's Source points to external/web with no codebase or docs anchor
- the design assumes a subsystem with no Subsystem Presence verdict backing it
- a premise's recorded Scope does not cover this feature's context (per spec)

List the ungrounded items and stop; resolving them is design's job.

### Step 3: Prepare Branch and Status

Runs before subagent dispatch -- the branch must exist before any subagent writes code, and the status flip records that implementation is underway.

**Branch**: Read `branch:` from spec.md frontmatter. If it differs from the current git branch and is not `main`/`master`:

```bash
git switch -c {branch} 2>/dev/null || git switch {branch}
```

Skip the switch when frontmatter says `main`/`master`, when the field is empty, or when the current branch already matches. specify.md only records intent -- implement owns the actual `git switch`. Never create the branch later than this step (i.e., never after dispatch).

**Status**: If status is `ready` or `draft`:
- Set `status: in-progress`

### Step 4: Validate Dependencies

For each task to implement:
- Check [P] (parallel) - proceed
- Check [B:T-X] - verify T-X is done

**Subagent dispatch:** The user story is the dispatch grain. Dispatch one
subagent per user story in the selection, sequentially in spec order:

- `[T-1]`: one subagent for the single task.
- `[T-1..T-5]`: one subagent per user story the range spans, in spec order.
- `[US-1]`: one subagent for that user story.
- `[--all]`: one subagent per pending user story, in spec order.

Each subagent owns Steps 5-6 for the tasks of its user story. It implements
tasks in dependency order (`[B:T-X]` waits for `T-X`), resolves order
internally, runs verify per task (Step 5-After), marks `[x]` in tasks.md
(Step 6), and -- when auto-commit is on -- commits the boundary it completes.

Main agent dispatches one user story at a time and waits for it to return
before dispatching the next -- a single active writer, never concurrent
across stories, never fanning out across tasks. Between stories it reads
tasks.md and per-task status from disk. After the last user story in the
selection returns, it resumes at Step 7 (Check Completion).

Subagent brief includes:
- Paths to spec.md, design.md, tasks.md, coding-principles.md
- Task list within scope (T-X, ...) with `[P]`/`[B:T-X]` markers
- Acceptance criteria per task
- "Run Steps 5-6 for each task in dependency order. Implement, verify per
  task, mark `[x]` in tasks.md. Write code and updates to disk. Report
  files changed and per-task status."
- Auto-commit mode (on when `--commit` or `--all`, else off). When on: the
  commit granularity (default one commit per user story; per task if the prompt
  asked) and "after a commit boundary's last task passes verify and is marked
  `[x]`, build the message per [commit-conventions.md](commit-conventions.md)
  and `git commit` that boundary. Commit a boundary only when this scope fully
  completes it; one covered in part is left for a later run. Run hooks normally
  -- never `--no-verify` or `--amend`."
- "For every fact you reproduce (identifiers, tokens, copy, config values,
  identity strings), read it from the source of truth named in design.md or
  spec.md. If the fact is not in that source, STOP and report — never invent
  or default it."

Subagent writes code, runs verify, and updates tasks.md. Main agent reads
tasks.md and per-task status from disk, resumes at Step 7.

Dispatch shape:

```text
For each user story US-k in the selection (spec order):
  dispatch one subagent for US-k; wait for it to return;
  read tasks.md and per-task status from disk.
After the last user story: resume at Step 7.
```

Map this shape to the subagent dispatch primitive available in the harness.

### Step 5: Implement Tasks

**Ownership:** When Step 4 dispatched a subagent, the subagent runs Step 5
(and Step 6) for every task in its scope. Main agent resumes at Step 7. When
no dispatch ran (subagent support unavailable), main agent runs Step 5 inline.

For each task, follow the 3-phase cycle:

#### Before (Preparation)

- Load [coding-principles.md](coding-principles.md)
- Read the relevant reference files from design.md (patterns to follow)
- Check the conventions table (naming, imports, error handling)
- State the pre-implementation declaration before writing any code:

```text
Assumptions: {what am I assuming about existing code -- verify each}
Files: {exhaustive list of files to create/modify -- only these}
Success criteria: {which ACs and Done when this task satisfies}
```

Do not proceed without stating all three explicitly.

**Source of truth:** for every fact this task reproduces (identifiers, tokens,
copy, config values, identity strings), name the source it comes from
(design.md, a `file:line`, spec.md, a project doc). If the fact is not in that
source, STOP and ask — never invent or default it.

- Verify the declaration against the checklist:

**Pre-Implementation Checklist:**

Files and success criteria are already resolved by design.md and tasks.md —
check only assumptions and risk:

| Check | Question | Required? |
|-------|----------|-----------|
| Assumptions | Are all assumptions verified against actual code, not memory? | Required |
| Files | Do listed files match design.md component locations? | Skip — use design.md |
| Success criteria | Does it map directly to the task's Done when and AC-xxx? | Skip — use tasks.md |
| Risk | Could this change break existing functionality? | Required |

Any failed check: resolve before writing code.

#### During (Implementation)

- **Test-first (only when a test runner is detected):** if the project has a test
  command from the quality gates, author the task's tests first — write a test for
  each AC the task covers, run it and confirm it fails (the red), make it pass with
  the minimum code (the green), then refactor with the test green. **Capture** the
  red→green per AC to `test-evidence.md` (format below): the test command, the red
  run's exit code and failing assertion, and the green confirmation. The captured
  output -- not a prose claim -- is the binding evidence verify's AC→test map
  consumes (see [verify.md](verify.md) Step 6); a test that was never red may pass
  vacuously. This authoring loop is separate from the After quality gate, which
  *runs* the resulting suite; when no test runner exists, skip it (write no evidence
  file) and implement directly

  `test-evidence.md` format (sensible default -- adapt to the runner's output):

  ```markdown
  # Test Evidence: {feature}

  ## AC-1
  - Test: {test name or describe block}
  - Command: `{invocation}`
  - Red (behavior absent): exit {non-zero} -- {failing assertion or error excerpt}
  - Green (behavior present): exit 0
  ```
- Follow design.md architecture precisely
- Match patterns from reference files exactly
- Use project's error handling approach
- Follow naming conventions documented
- Apply research findings from design.md if applicable
- Follow Knowledge Verification Chain for any technical decisions
- **Scope guardrail:** if something outside the task definition is noticed (bug, improvement,
  tech debt), record it in `.artifacts/knowledge.md ## Gotchas` -- do not act on it inline.
  The heuristic: "Is this in my task definition?" If no, record and move on.

##### Design-gap recovery

When a defect surfaces during implementation that traces back to a missing or wrong assumption in `design.md` (rather than a coding mistake in the task), prefer a clean reset over additive corrective commits.

Heuristic for "design gap" vs "coding mistake":
- **Coding mistake**: the task's mechanism is correct in design, but implementation typed it wrong, missed an edge case, or violated a documented convention. Fix in place, normal commit.
- **Design gap**: the task's mechanism is wrong because design.md black-boxed a utility, a component contract, a numeric default, or a cross-task value flow. The corrective work invalidates the prior commit's premise.

When a design gap is identified mid-implement, pause and pick the cleaner recovery:

1. `git reset --soft` to the pre-defect commit (or the commit that introduced the wrong premise) -- preserves the staged corrective work without keeping the contradicting commit history
2. Re-commit in the corrected shape, with the new mechanism reflecting what design.md should have said
3. Record the gap in the right sink(s) -- a single gap can hit more than one:
   - **Feature-local audit trail (always):** append to the feature's `design.md` under a new section `## Design Gaps Discovered During Implementation` -- one bullet stating what the assumption was and how implementation invalidated it. This documents why the commit was reset; it is feature-scoped and is not read by later features, so it is not where a reusable learning survives.
   - **Cross-feature gotcha (when the gap encodes a durable project fact a future feature would otherwise rediscover):** record it in `.artifacts/knowledge.md ## Gotchas` -- the sink design.md Step 3 reads before designing the next feature. This is what keeps the learning from dying in the feature-local section.
   - **Skill-class issue (opt-in, when the gap reveals a class of issue the spec-driven skill itself should catch):** append to `.artifacts/spec-driven-feedback.md` as input for future skill iteration (this file is opt-in, not part of `.artifacts/knowledge.md`)

Never use `--no-verify` or `--amend` to mask a design gap. The corrective commit must run hooks normally. Destructive history rewriting (`reset --hard`, force push) requires explicit user confirmation.

Additive corrective commits ("oops, missed X", "fix the previous fix") are a smell that the underlying design assumption is wrong -- when two corrective commits stack, stop and apply the recovery above.

#### After (Quality Gates + Verify)

Quality gates and verification run after EVERY task or range -- never deferred.

**Quality gates:**

```bash
# Use --fix flags when available
{lint command} --fix
{typecheck command}
{test command}
```

Fix errors before proceeding to verify.

**Verify:**

Run [verify.md](verify.md) to check implementation against design, project
patterns, and visual references (if provided). Verify handles:
- Design adherence (code matches spec/design)
- Pattern adherence (code follows project conventions)
- Code correctness (semantic checks linters and type-checkers miss)
- Test coverage (AC→test map with red→green binding plus traceability when a test runner exists; announces read-only mode when none)
- Visual adherence (layout matches references, optional)

If verify finds issues, fix them before moving to the next task. See
verify.md for the full workflow including loop escape.

### Step 6: Update Progress

**Ownership:** When dispatched, the subagent runs Step 6 for each task it
completes (right after Step 5-After verify passes). Main agent runs Step 6
inline only when no dispatch ran.

If tasks.md exists:
1. Verify the "Done when" criteria for the task are met
2. Mark completed tasks by flipping `[ ]` to `[x]`. The checkbox alone
   signals completion -- do not append `VERIFIED`, a status word, or a
   parenthetical note to the "Done when" line; leave it as authored:
```markdown
- [x] T-1 [P] {description}
  - **Done when:** {verifiable outcome}
```
3. Update task counters in tasks.md header.
4. **Commit boundary (auto-commit on only):** when the task just marked closes
   a commit boundary this scope fully completes, build the message per
   [commit-conventions.md](commit-conventions.md), stage the boundary's changes,
   and `git commit` (hooks run normally). A boundary this scope completes only
   in part is left uncommitted. When a defect later invalidates a landed commit,
   see Design-gap recovery (Step 5 During).

### Step 7: Check Completion

If all tasks done:
- Run final verification (see [Final Verification](#final-verification))
- Set `status: to-review`
- Do NOT set `status: done` -- audit owns that transition

### Step 8: Record Discoveries

Load [knowledge.md](knowledge.md) for format.

Route the cross-feature knowledge implementation surfaced to
`.artifacts/knowledge.md`:

- **Runtime constraints, API quirks, workarounds, tech debt** -> `## Gotchas`
- **Cross-feature decisions** -> `## Decisions`
- **Normative conventions the codebase follows** -> `## Conventions`

If `.artifacts/knowledge.md` doesn't exist, create it with the three empty section headers (`## Decisions`, `## Gotchas`, `## Conventions`).

Descriptive area patterns belong in the `.artifacts/codebase/{area}.md` cache, written by exploration — not here. Record only what crosses features; feature-specific detail stays in this feature's artifacts, and inventory facts (packages, routes, modules) are re-derivable and not recorded.

### Step 9: Completion Gate

When all tasks in scope are done and Final Verification passes, behavior depends
on auto-commit mode.

**Auto-commit off (default):** stop and announce the work is ready -- no commit
is made; the human commits with their own flow.

```text
Implementation ready: `.artifacts/specs/{date}-{name}/`
Tasks: {X} done | ACs: {Y}/{Z} verified
Remaining: {count or "none"}

Ready for review/commit, or describe what to fix.
```

**Auto-commit on (`--commit` / `--all`):** boundaries already committed as they
completed -- report what landed, no blocking gate.

```text
Implementation committed: `.artifacts/specs/{date}-{name}/`
Tasks: {X} done | ACs: {Y}/{Z} verified | Commits: {N}
Remaining: {count or "none"}
```

- If issues remain: fix before presenting.
- If changes requested (off mode): address and re-present.
- Then flip status to `to-review` and stop. Implement does not run `audit` --
  audit gates the commit boundary (per-story or pre-PR) and is invoked
  separately. For user-facing features, also consider `validate`.

Never open a PR before `audit` passes for the work being merged.

## Edge Case Verification

When verifying code after each task, check for relevant edge cases:

| Category | What to Verify |
|----------|---------------|
| Error states | Error paths return meaningful messages, no silent failures |
| Boundaries | Empty arrays, zero values, max lengths, off-by-one |
| Concurrency | Race conditions in async operations, state mutations |
| Permissions | Authorization checks on protected operations |
| Network | Timeout handling, retry logic, offline behavior |
| Invalid input | Null/undefined, wrong types, malformed data |

Not every category applies to every task. Check only what's relevant to the code just written.

## Final Verification

When all tasks are complete, run a final pass before setting `status: to-review`:

- [ ] All acceptance criteria (AC-xxx) are covered by tasks
- [ ] All ACs marked `[x]` in spec.md match the per-task verify results
- [ ] Quality gates pass on the full feature (not just per-task)
- [ ] No TODO/FIXME comments left from this feature
- [ ] Edge cases from spec.md are handled
- [ ] Verify passed (design + pattern adherence)

Goals and Success Criteria are NOT checked here -- they are audit.md's job.
Do not mark their `[ ]` from this reference.

Audit is mandatory before `done`. UAT is on-demand, except required before `done`
for user-facing features (`user-facing: true`).

## Guidelines

**DO:**
- Complete one task at a time before starting the next
- Load coding-principles.md before writing any code
- Verify after each task or range -- never batch all verification to the end
- Follow Knowledge Verification Chain -- never fabricate patterns or APIs

**DON'T:**
- Refactor beyond what the task requires
- Batch all verification to the end
- Skip loading coding-principles.md before implementation

## Error Handling

- Tasks not found: tasks.md exists at every scope above Small; if missing, run `tasks` first
- Dependency blocked: List prerequisites
- Quality gate failed: Fix before marking done
- Scope misjudged: if a load-bearing decision surfaces, escalate Medium → Large via design (see [auto-sizing.md](auto-sizing.md) Safety Valve)
- Design-gap defect mid-implement: see Design-gap recovery in Step 5 During -- prefer `git reset --soft` over additive corrective commits, then record the gap in the feature's design.md (always), `.artifacts/knowledge.md ## Gotchas` (when it encodes a durable cross-feature fact), and `.artifacts/spec-driven-feedback.md` (opt-in skill-class issues)
