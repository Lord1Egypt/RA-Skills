# Verify Implementation

Check implementation against the spec design, project patterns, code
correctness, and visual references. Runs after every task or range —
never deferred to the end. Loads [code-correctness.md](code-correctness.md)
during Step 5 for the code correctness analysis.

## When to Use

Loaded internally by `implement.md` Step 5-After. Verify is not a user-invoked phase -- it runs automatically after every task or range, once `implement.md`'s quality gates pass.

- After completing a task or range of tasks (any scope) -- always via implement
- After quality gates pass in implement.md -- verify is the deeper check

## When to Skip

- Quick mode (small fixes, config changes)

## Workflow

### Step 1: Resolve Feature

1. If a name is given -> match `.artifacts/specs/{date}-{name}/` (glob `*-{name}` or `*-{name}-*` for a collision variant)
2. If no name -> match current git branch to `branch:` in spec.md frontmatter
3. If multiple or no match -> list available specs and ask user

### Step 2: Load Sources of Truth

Gather the references to verify against:

| Source | Location | Purpose |
|--------|----------|---------|
| Spec | `.artifacts/specs/{date}-{name}/spec.md` | Acceptance criteria, user stories, edge cases |
| Design | `.artifacts/specs/{date}-{name}/design.md` | Architecture, data model, file list, patterns |
| Project patterns | `.artifacts/codebase/{area}.md` cache | Conventions, naming, error handling, data fetching |
| Visual references | `.artifacts/specs/{date}-{name}/designs/` or MCP | Layout, UI behavior (optional) |

Skip sources that don't exist. Design and project patterns are the primary
sources. Visual references only when provided or explicitly requested.

### Step 3: Design Adherence

Compare implementation against design.md (if exists) or spec.md:

- **Planned vs implemented**: functions, endpoints, components, routes described
  in design -- do they exist in code?
- **Behavior**: does the implementation match the described behavior, data flow,
  and state management?
- **Data model**: do entities, relationships, and API contracts match the design?
- **File structure**: are files created/modified as listed in the design?

Report findings as:

| Finding | Severity | Description |
|---------|----------|-------------|
| Missing endpoint | high | `POST /api/auth/login` in design but not implemented |
| Behavior mismatch | medium | Token refresh uses polling instead of designed event-based approach |

### Step 4: Pattern Adherence

Compare implementation against project conventions in the
`.artifacts/codebase/{area}.md` cache (if exists) or against patterns
observed during exploration:

- **Naming**: files, components, functions, variables follow project conventions
- **File structure**: new files placed in correct directories per project patterns
- **Error handling**: uses project's error handling approach (not ad-hoc)
- **Data fetching**: uses project's data fetching patterns (hooks, server actions, etc.)
- **Imports**: follows barrel exports, path aliases, import ordering
- **Styling**: uses design tokens, CSS variables, not hardcoded values

Report findings with the same severity table.

### Step 5: Code Correctness

Load [code-correctness.md](code-correctness.md) for semantic code analysis.

Code correctness analysis checks for logic errors, semantic issues, and
correctness problems that linters and type checkers cannot detect. It
auto-detects project tooling and skips categories already covered.

Skip this step when the task only changed configuration, documentation,
or static assets.

Findings merge into the outcome table in Step 8.

### Step 6: Test Coverage

Branch on whether the project has a test runner (a test command from implement's
quality gates):

- **No test runner.** Do not skip silently — there is nothing to bind to, and the
  user must not read green as tested. Report in the Step 8 outcome that AC
  verification is read-only here (design adherence + code correctness only): no
  execution proof, no AC→test binding. Add a one-line Operational Follow-up to
  spec.md ("no test runner — ACs unverified by test") so the gap is durable, not
  assumed-green. Then skip the map, binding, and checks below.
- **Test runner present.** Run the map, binding, and checks below.

**AC → test map.** For each AC this task covers, identify the test(s) that exercise it
— match by the behavior the test asserts, not by any tag or annotation. Report the
mapping in the Step 8 outcome:

| AC | Covering test(s) | Red→green observed |
|----|------------------|--------------------|
| AC-1 | {{test name or describe block}} | {{yes / no}} |

**Binding.** Matching by asserted behavior says a test *looks* right; the red→green
transition says it *binds*. A covering test counts only if it was observed to fail
when the behavior was absent and pass once present — the red→green **captured in
`test-evidence.md`** by implement's test-first (see [implement.md](implement.md)
During). Read the recorded red-run output (exit code + failing assertion), not a
prose claim. A test with no entry in `test-evidence.md`, or one whose recorded run
was never red, may pass vacuously: flag it (medium) and re-derive it red→green
before the AC counts as covered. An AC covered only by a pre-existing test has no
fresh red→green — confirm its binding before counting it, never assume it.

**Checks.** From the map, assert:

- **No uncovered AC** — every AC this task covers has at least one covering test with an observed red→green
- **No orphan test** — every new test traces to an AC or Edge Case; a test mapping to
  nothing is dead or testing the wrong thing
- **No untraced task** — the task maps to at least one AC (cross-check tasks.md
  `## Requirements Coverage`)
- **No orphan code** *(only when a coverage tool is detected)* — every changed symbol
  is exercised by at least one test

A failed check is a finding (high for uncovered AC or orphan code, medium for orphan
test, untraced task, or unbound test) — fix before the task passes.

**Coverage (only when a coverage tool is detected).** Report changed-file coverage from
the tool's output. Flag a drop against the pre-change baseline as a finding — do not
enforce a fixed threshold; the project owns its threshold. Skip silently when no
coverage tool exists.

### Step 7: Visual Adherence (optional)

Only runs when visual references exist or user explicitly requests.

Sources of visual references:
- Screenshots or mockups in `.artifacts/specs/{date}-{name}/designs/`
- Figma via MCP (if available in session)
- Pencil via MCP (if available in session)
- Any reference the user provides during Specify phase

Compare:
- Layout structure matches reference
- Component hierarchy matches reference
- Responsive behavior matches reference (if specified)
- Spacing, alignment, visual hierarchy are consistent

### Step 8: Determine Outcome

**If all checks pass:**
- Report "Verification passed" with summary
- Mark covered ACs as `[x]` in spec.md (see [Step 9](#step-9-sync-ac-checkboxes))
- Continue to next task or mark done

**If issues found:**
- List findings with severity
- If a previously-marked AC is now failing, revert its `[x]` to `[ ]` in spec.md
- Fix issues immediately (verify → fix → verify loop)
- Re-run only the failed checks after fix

### Step 9: Sync AC Checkboxes

After verification passes for a task, update spec.md acceptance criteria.

**Which ACs to mark:**

1. If `tasks.md` exists: read `## Requirements Coverage` table -- mark every
   AC whose task list is fully verified (all listed tasks passed verify)
2. If no `tasks.md` (fallback): map by user story containing the code
   changed -- mark ACs inside that P1/P2/P3 user story

**How to mark:**

Edit `spec.md` in place: flip `- [ ]` to `- [x]` and change the status tag
from `` `in-tasks` `` to `` `verified` `` on the matching AC line.
Never reorder, rename, or drop ACs. Preserve the `AC-xxx:` identifier.

**Revert rule:**

If a later verify run reopens a finding on an already-marked AC, flip it back
to `- [ ]` and revert the status tag to `` `in-tasks` ``. The checkbox and
status always reflect current verification state, not historical pass.

**Never touch Goals or Success Criteria here** -- those are audit.md's job.

### Step 10: Loop Escape

Track fix attempts per finding. If the same finding fails N times (default: 3):
- Stop the loop
- Report the stuck finding with context
- Ask the user for input: "I've attempted to fix this 3 times without
  success. Here's what I've tried and what's still failing. How should
  I proceed?"

Never loop indefinitely.

## Guidelines

**DO:**
- Run after every task or range, regardless of scope
- Check design adherence first, then patterns, then code correctness, then test coverage, then visual
- Fix issues before moving to the next task
- Report findings with severity (high/medium/low)
- Skip visual check when no references exist
- Sync AC checkboxes in spec.md after every pass (and revert on regression)

**DON'T:**
- Defer verification to the end of all tasks
- Report code style issues that linters already catch
- Loop indefinitely on the same finding
- Assume visual references exist -- check first
- Run visual verification without explicit references
- Run code-correctness on config-only or docs-only changes
- Mark Goals or Success Criteria checkboxes -- audit.md owns those

## Error Handling

- No design.md: verify against spec.md acceptance criteria only
- No area cache: skip pattern adherence or scan representative files
- No visual references: skip visual adherence entirely
- All sources missing: inform user, suggest running design first
