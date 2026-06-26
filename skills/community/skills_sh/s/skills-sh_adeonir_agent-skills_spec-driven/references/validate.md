# Interactive UAT

User acceptance testing where the user manually verifies behavior. Required before `done` for user-facing features (`user-facing: true`); on-demand for the rest.

## When to Use

- Required before `done` when spec.md has `user-facing: true` -- audit blocks the close until UAT passes
- User explicitly requests UAT or manual testing (any feature)
- Feature is in `to-review` (implement finished)
- Any scope -- not restricted to Complex

## When to Skip

- Feature has `user-facing: false` (no visual surface to approve — backend/API/logic) and the user does not request UAT

## Relationship to Audit

Validate is the human-observation layer. Audit ([audit.md](audit.md)) is the
evidence-based layer.

- Audit transitions status `to-review` -> `done`; validate does **not** -- it
  records the UAT verdict in `uat:` (`pass` / `changes`), and audit reads it
- For a **user-facing** feature, validate gates `done`: audit will not close until
  `uat: pass`. For a non-user-facing feature the two are independent and may run in
  any order
- Audit gates the PR; validate does not
- If UAT reproves a scenario, validate may revert any `[x]` (AC, Goal, or
  Success Criterion) in spec.md and set `uat: changes` -- after a revert, audit
  must be re-run before the feature can move to `done`

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

### Step 1: Resolve Feature

1. If a name is given -> match `.artifacts/specs/{date}-{name}/` (glob `*-{name}` or `*-{name}-*` for a collision variant); a completed feature may live in `.artifacts/archive/`, so check there too
2. If no name -> match current git branch to `branch:` in spec.md frontmatter, checking `.artifacts/specs/` then `.artifacts/archive/`
3. If multiple or no match -> list available specs and ask user

### Step 2: Pre-UAT Check

Verify that implementation is complete:
- All tasks marked done (or all inline steps completed)
- Quality gates pass
- Verify has passed (design and pattern adherence)

If not complete, inform user and suggest finishing implementation first.

### Step 3: Build Test Scenarios

From spec.md, extract testable scenarios:

1. For each P1 user story: create a step-by-step test
2. For P2/P3 user stories: create key scenario tests (not exhaustive)
3. Include edge cases from spec.md that are user-facing

Present the test plan to the user before starting.

### Step 4: Run Interactive UAT

Walk the user through each scenario:

1. Describe the steps to perform
2. Ask user to verify the expected behavior
3. Record pass/fail with observations

### Step 5: Determine Outcome

**If all pass:**
- Confirm feature is validated by user observation
- Set `uat: pass` in spec.md frontmatter
- Suggest running `audit` (if not already run) to close status `to-review` -> `done`
- Suggest commit if not already committed

**If issues found:**
- List what needs fixing with severity
- Set `uat: changes` in spec.md frontmatter
- If a previously-checked AC, Goal, or Success Criterion is reproved, revert
  its `[x]` to `[ ]` in spec.md and tell the user audit must be re-run
- Suggest specific areas to re-implement
- User decides whether to fix now or defer

## Guidelines

**DO:**
- Let the user drive -- they decide when to run UAT
- Focus on behavior, not code quality (verify handles that)
- Prioritize P1 user stories in test scenarios
- Keep test steps concrete and actionable
- Revert `[x]` to `[ ]` in spec.md when the user reproves a previously-checked item

**DON'T:**
- Run UAT automatically without user request
- Report code style or pattern issues (that's verify's job)
- Make UAT exhaustive for non-P1 user stories
- Block completion on minor P3 issues
- Transition `status: done` -- that is audit.md's exclusive job

## Error Handling

- No spec.md: suggest running specify first
- Implementation not complete: redirect to implement
- No user-facing behavior: inform user UAT is not applicable
