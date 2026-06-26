# Audit Feature

Validate Goals and Success Criteria against evidence, mark the
corresponding checkboxes in spec.md, and transition status from
`to-review` to `done`.

Auditing requires evidence-based reasoning across spec, design, and
implementation — shallow checks risk rubber-stamping. Load
[status-workflow.md](status-workflow.md) for correct status management.

## When to Use

- After a user story completes (commit boundary) -- partial pass validates the Goals/Success Criteria the user story unblocks
- After the entire spec is implemented -- gates the PR
- User explicitly requests `audit` or `validate goals`
- Before closing a feature -- `done` requires audit

Audit may run per-story (incremental) or once at the end. Status only flips to `done` when every Goal and Success Criterion is Met. Always run audit before opening a PR for the work being merged.

## When to Skip

- Feature is still `in-progress` -- finish the current user story first
- Feature is already `done` -- re-audit only if requested

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

Track each step as it completes — mark it done before moving to the next.
In Claude Code, create a task list at phase start (TaskCreate) and update
each step as it completes (TaskUpdate).

### Step 1: Resolve Feature

1. If a name is given -> match `.artifacts/specs/{date}-{name}/` (glob
   `*-{name}` or `*-{name}-*` for a collision variant); a re-audit target
   may already live in `.artifacts/archive/`, so check there too
2. If no name -> match current git branch to `branch:` in spec.md frontmatter, checking `.artifacts/specs/` then `.artifacts/archive/`
3. If multiple or no match -> list available specs and ask user

### Step 2: Pre-Audit Check

Read spec.md frontmatter. If `status` is not `to-review`:

| Current Status | Action |
|----------------|--------|
| `draft`, `ready` | Stop. Inform user implement has not started. |
| `in-progress` | Stop. Inform user to finish implement (which sets `to-review`). |
| `done` | Ask user if they want to re-audit. If yes, proceed. |

### Step 2a: Dispatch Audit subagent

Steps 3-5 are owned by a read-only audit subagent. Main agent resolves the
feature and clears the pre-audit gate (Steps 1-2, including any user
interaction), re-runs the test suite (see Test Re-run below), then dispatches
once, receives a structured verdict, and applies it in Steps 6-9.

Why dispatched: evidence gathering reads spec, design, source, tests, and UAT
notes -- context-heavy and read-only. Isolating it keeps the main context clean
for the user-visible checkbox and status writes. The subagent is read-only by
harness contract (Edit/Write/NotebookEdit excluded), so it returns the verdict;
main applies it (pattern: subagent returns slots, main fills the result).

**Test Re-run (main agent, before dispatch).** When the project has a test
runner, the main agent runs the full suite once and captures the result --
green, or red with the failing tests. This is the audit's own execution, not a
trust of verify's per-task claims: a suite green during implement can be red at
audit (a later task regressed it, or it was never actually green). The result
becomes the automated-test evidence the subagent uses (Step 4) and a hard gate
on the outcome (Step 7). When no test runner exists, skip the re-run and report
that audit cannot re-validate tests -- Goals tied to behavior rest on code
inspection only.

A green re-run confirms the suite passes now; it does not confirm each test binds
to its AC (a test can pass vacuously). Binding rests on the red->green evidence
recorded at implement time (see [verify.md](verify.md) Step 6), not on this re-run.

Subagent brief:

- Inputs (paths only -- subagent reads from disk): `spec.md` (Goals + Success
  Criteria), `design.md`, the feature's source and test files,
  `.artifacts/specs/{date}-{name}/validate.md` if it exists, and
  `.artifacts/specs/{date}-{name}/inputs/` (the raw input snapshot) if it exists
- The test-suite re-run result from the main agent (green, or red with the
  failing tests) -- use it as the automated-test evidence; never infer test
  status from reading the test files
- "Run Steps 3-5: load every `- [ ]` under `## Goals` and `## Success Criteria`
  (never `## Operational Follow-ups`, never ACs), gather evidence per the
  evidence-source order, and classify each target Met / Unmet / Unmeasurable
  with an evidence cite. If `inputs/` exists, also compare the delivered feature
  and spec against the original input and report divergences -- each marked
  accounted-for (a Non-Goal or Decision explains it) or unaccounted. Return the
  verdict; do not edit any file."

Return shape:

```text
{ targets: [{ name, classification, evidence }],
  all_met: bool, unmet: int, unmeasurable: int,
  input_divergences: [{ what, accounted_for: bool, note }] }
```

When subagent support is unavailable, main runs Steps 3-5 inline.

### Step 3: Load Audit Targets

_Steps 3-5 run inside the audit subagent dispatched in Step 2a._

Read spec.md and extract every `- [ ]` item under:

- `## Goals`
- `## Success Criteria`

Record each target with its exact line text. These are the only items this
reference may mark -- never touch ACs (verify.md owns those).

**Never read `## Operational Follow-ups`** -- that section captures
post-deploy observation tasks and is non-audit by design. Items there never
block status transition.

### Step 4: Gather Evidence

For each target, collect evidence that it is met. Evidence sources, in order
of preference:

| Evidence Type | Source | When to Use |
|---------------|--------|-------------|
| Automated test | The main agent's test re-run result (Step 2a), matched to the behavior | Goals tied to behavior |
| Metric measurement | Benchmark, profiler, instrumentation output | Success Criteria with numbers ("under 2 minutes", "zero errors") |
| Code inspection | Relevant files from design.md | Goals tied to presence of a capability |
| Manual observation | UAT session notes or user-supplied evidence | Subjective user-facing behavior |

If `.artifacts/specs/{date}-{name}/validate.md` or UAT notes exist, consult
them -- validate may have already confirmed some targets.

### Step 5: Classify Each Target

For each target, mark one of:

- **Met** -- evidence clearly supports the claim
- **Unmet** -- evidence missing or contradicts the claim
- **Unmeasurable** -- target is phrased in a way that cannot be verified (e.g., vague wording)

Report a table:

| Target | Classification | Evidence |
|--------|----------------|----------|
| G1: Users complete onboarding in under 2 minutes | Met | Benchmark: median 87s across 20 runs (see perf report) |
| SC1: Zero errors in payment flow | Unmet | 2 errors observed in integration test run |
| G2: Improve conversion | Unmeasurable | No metric defined -- needs spec update before re-audit |

### Step 6: Update spec.md

_Steps 6-8 run in the main agent, applying the verdict from Step 2a._

For every target classified **Met**:

- Edit spec.md in place, flipping `- [ ]` to `- [x]` on the matching line
- Preserve exact wording and identifier
- Never reorder, rename, or drop items

For **Unmet** targets: leave `- [ ]` unchanged.

For **Unmeasurable** targets: leave `- [ ]` unchanged and report -- the spec
needs a rewrite, not an audit pass.

### Step 7: Determine Outcome

**Hard gate -- test re-run.** If the Step 2a re-run was red, audit cannot pass:
keep `status: to-review`, report the failing tests, and stop. A failing suite
means the implementation is not in its verified state, so no Goal tied to
behavior can be Met. Skip this gate only when no test runner exists -- audit
noted that limitation at re-run time.

**Hard gate -- UAT (user-facing only).** If spec.md frontmatter has
`user-facing: true` and `uat` is not `pass`, audit cannot set `done` even when
every Goal and Success Criterion is Met: keep `status: to-review`, report that UAT
is required, and direct the user to [validate.md](validate.md). A user-facing
feature reaches `done` only after a human walks the scenarios -- in autonomous
runs this is the point that requires a person. Features with `user-facing: false`
skip this gate.

**If every Goal and Success Criterion is Met:**

- Set `status: done` in spec.md frontmatter
- If the spec still lives in `.artifacts/specs/`, move it out so a later
  spec never forages it: `mv .artifacts/specs/{date}-{name}
  .artifacts/archive/{date}-{name}`. On a re-audit it is already in
  `archive/` -- leave it there. If a different spec already occupies the
  archive path, suffix the name. The archive is never read during
  discovery.
- Report "Audit passed. Feature closed."
- Suggest commit for the audit updates (if any checkboxes flipped)

**If any target is Unmet or Unmeasurable:**

- Keep `status: to-review`
- Report the failing targets with evidence gaps
- Suggest next action per category:
  - Unmet -> fix implementation or update tests, then re-run audit
  - Unmeasurable -> update spec.md (via specify) with a verifiable rewrite

### Step 8: Structural Delta Check

Independent of audit outcome. Inform the user when structural changes may
have outdated `CLAUDE.md ## Architecture` so they can decide whether to
refresh it. Never prompt, never block the status transition.

Run against the feature branch:

```bash
git diff --name-status $(git merge-base main HEAD)..HEAD
```

Flag as structural delta if any of the following is true:

- Any `A` (added), `D` (deleted), `R` (renamed), or `C` (copied) entry outside `.artifacts/`
- `package.json` `dependencies` or `devDependencies` sections changed
- `.env.example` changed
- New directory under `src/app/api/` or equivalent route root (framework-specific)

If any flag fires, append exactly one line to the audit report:

> Structural changes detected — consider refreshing `CLAUDE.md ## Architecture` to reflect them.

If no flag fires, emit no output for this step.

### Step 9: Source and Discovery Advisories

Independent of audit outcome; informing, never blocking. Two advisories.

**Input divergence (only when `inputs/` exists).** The audit subagent (Step 2a)
returns `input_divergences` from comparing the delivered feature and spec against the
raw input snapshot. Surface the **unaccounted** ones -- divergences no Non-Goal or
Decision explains. An accounted-for divergence (an intentional scope cut recorded in
Non-Goals or Decisions) is not reported.

> Source divergence (unaccounted): {what} -- in `inputs/` but not in the delivered feature; no Non-Goal or Decision explains it.

**Discovery risk.** If spec.md frontmatter is `discovery: autonomous-assumed`, or
`## Assumptions` holds `agent-assumed` rows the audit did not confirm, surface them --
the spec rests on premises no human validated, and the user should see that before
`done`.

> Discovery risk: {N} unvalidated agent-assumed assumption(s); discovery: {human|autonomous-assumed}. Review before close.

Emit nothing for an advisory whose condition does not fire (no `inputs/`, every
divergence accounted-for, `discovery: human` with no unconfirmed assumptions).
Together these are the oracle outside the spec: they catch silent narrowing of the
source and unvalidated premises, but inform -- the user adjudicates.

### Step 10: Relationship to Validate

Audit is evidence-based and automated. Validate ([validate.md](validate.md))
is user-observation based and interactive.

- For a **user-facing** feature (`user-facing: true`), validate gates `done`:
  audit holds at `to-review` until `uat: pass` (Step 7). For a non-user-facing
  feature the two are independent and may run in any order
- Audit transitions status to `done`; validate does not -- it records the `uat:`
  verdict that audit's user-facing gate reads
- Validate may revert any `[x]` (AC, Goal, Success Criterion) and set
  `uat: changes` if the user reproves a scenario -- audit must be re-run after
  such a revert

## Guidelines

**DO:**
- Require evidence for every `[x]` mark -- never flip based on plausibility
- Prefer automated evidence (tests, metrics) over manual observation
- Re-run the test suite during audit when a runner exists -- the evidence is the run, not verify's earlier claim; a red re-run blocks `done`
- Leave Unmeasurable targets unchecked and flag the spec for rewrite
- Keep audit deterministic -- same evidence yields same classification
- Consult UAT notes if validate ran before audit
- Suggest refreshing CLAUDE.md ## Architecture when structural deltas exist — inform only, never prompt
- Treat `## Operational Follow-ups` as non-audit -- route those items to runbooks or issues outside the spec, never as a blocker for `done`

**DON'T:**
- Touch AC checkboxes or status tags -- those belong to verify.md
- Set `status: done` if any Goal or Success Criterion is Unmet or Unmeasurable
- Close a user-facing feature (`status: done`) before `uat: pass`
- Rewrite Goals or Success Criteria during audit -- route to specify instead
- Assume Met because the code exists -- check the observable outcome
- Read or classify items under `## Operational Follow-ups` -- that section is non-audit by design and never gates status

## Error Handling

- Status is not `to-review`: follow Step 2 table
- No Goals or Success Criteria in spec.md: inform user spec is incomplete, suggest specify
- All targets Unmeasurable: stop, tell user the spec needs rewritten Goals/Success Criteria with verifiable wording
- Evidence source unavailable (no tests, no metrics): report gap, suggest adding the missing evidence before re-audit
- Conflicting evidence between automated and manual sources: report both, ask user to adjudicate
