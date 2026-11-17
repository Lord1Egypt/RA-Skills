---
name: regression-hunt
description: >-
    Find what a change can break in the code that did NOT change — trace a diff, branch, commit
    range, or named feature outward through callers, consumers, shared state, and contracts,
    rank the concrete regression scenarios by blast radius, and prove or clear each one with an
    observed test run. Zero regressions is a valid outcome. Use this skill whenever the user says
    "look for regressions", "what could this break", "did this change break anything",
    "regression check", "impact of this change", "blast radius", "what else uses this", "is
    anything else affected", or "/regression-hunt" — even if they don't name the skill. Not for
    reviewing the diff's own quality (code-review) or a bug already observed (diagnose).
---

# Regression Hunt

Start from a change and look outward. code-review judges the lines that changed; this skill finds the lines that didn't change but now behave differently. Every candidate is a specific scenario with a citation, and every verdict is earned by a test that ran.

## When to use this skill

- "look for regressions", "what could this break", "did this change break anything"
- "regression check", "impact of this change", "blast radius", "what else uses this", "is anything else affected"
- `/regression-hunt`
- Called by `create-pr`'s review gate, or `goal-runner`'s regression step when a task touches shared code.

Do **not** auto-trigger for reviewing the change itself (`code-review`), a failure someone has already seen (`diagnose`), or a refactor planned as behavior-preserving from the start (`safe-refactor` owns that contract).

## Evidence rules

- A caller you found by grep or LSP is a fact; one you expect from the name is a hypothesis and is labeled one.
- **"Looked and found none" is a finding**, recorded per symbol with the search: "`formatDate` — no other callers; grep `formatDate\b` across `src/` and `tests/`: 1 hit, the definition."
- A `confirmed` regression needs a test or run that failed **because of this change** — quoted. A `suspected` one names the exact evidence still missing. Nothing is confirmed by reading alone.
- A result you did not observe is `not run`, never `passed`.
- Zero regressions is a valid outcome. The report earns it by listing what was traced and what ran.

## Workflow

Before each phase, restate in one line what changed and what you are protecting. If a phase drifts into reviewing the diff's style, stop — that's `code-review`.

### Phase 1 — Resolve the scope and inventory the change

Scope: dirty tree → `git diff` + `git diff --staged`; a branch → `git diff <base>...HEAD`; a range or SHA → that; a feature name → `git log --grep` / file paths, and if nothing resolves, ask once. Never `checkout`, `stash`, or `reset` — read-only git only.

List every changed **surface**, not every changed line. Surfaces that regress silently go first:

| Surface | Why it hides |
| --- | --- |
| Renamed or removed symbol, route, column, key, event name | string-keyed and dynamic callers don't fail at compile time |
| Changed default value, sort order, null/empty handling, exception type | callers keep compiling and get different answers |
| Changed signature, return shape, serialized format, enum members | consumers outside this repo, fixtures, and stored data |
| Changed shared state: DB schema, cache key, config/env name, feature flag | read by code that never imports the changed file |
| Changed timing: sync→async, added await, reordered side effects | races and ordering assumptions in callers |

- ❌ "Changed `OrderService` — check its callers." — a class-level entry hides the one method whose default flipped.
- ✅ "`OrderService.list(includeArchived = false)` default was `true` — every caller that omitted the arg now gets fewer rows."

### Phase 2 — Trace the blast radius

For each surface: grep the name as a word across the whole repo (source, tests, configs, SQL, templates, docs that are executed like OpenAPI); use LSP references where available; then hunt dynamic uses the grep misses — string keys (`obj["name"]`), reflection, template variables, SQL text, i18n keys, env names, job/queue names, CLI flags. Read each hit's enclosing function far enough to say whether the change reaches it.

Shared state gets its own pass regardless of imports: who else reads the column, key, flag, or event this change writes, and who writes what it reads.

**Council gate:** more than 5 surfaces, or callers in 3+ layers → send a **single message** with N `Agent` calls (`subagent_type=Explore`), one per surface group, each carrying the surface list verbatim and the evidence rules: "cite `file:line` for every caller; report none-found with the search you ran; read the enclosing function; do not edit; do not spawn agents; ≤400 words." Fewer → trace inline. The council is for width; you still adjudicate every hit.

### Phase 3 — Name the candidates

Turn each reached caller into a scenario or clear it:

`<what changed> → <who depends on the old behavior, file:line> → <observable wrong outcome>`

- ❌ "`exportCsv` may be affected by the date change." — no scenario; nothing to test.
- ✅ "`formatDate` now returns ISO → `exportCsv.ts:44` splits on `/` → date column exports empty for every row."

Rank by blast radius: money, auth, deletion, data migration, and anything user-facing at scale outrank the rest. A candidate with no nameable wrong outcome is **cleared**, with the reason ("caller passes the arg explicitly, `billing.ts:12`").

### Phase 4 — Audit the safety net and run it

For every candidate: which existing test exercises that path (`file:line`), or "no test covers this path — searched `tests/` for `exportCsv|formatDate`". Then:

1. Run the tests that cover the candidates (the narrowest set first, the full suite last) and quote each summary line.
2. A red test that fails because of the change → `confirmed`. Quote the assertion.
3. Uncovered candidate in the top of the ranking → write the missing test via `write-tests` if installed (else follow its shape: observable behavior, proven red-capable). Run it. Red → `confirmed`; green → `cleared by test <name>`.
4. Couldn't run (no environment, needs prod data, timing-dependent) → `suspected`, with the missing evidence named and `e2e-verify` suggested when a browser run would settle it.

Never weaken an existing assertion to get green — a legitimately red test is the regression you were looking for.

### Phase 5 — Report

The report has exactly these headings, in this order, every time — dry run, proposed change, or landed change alike. A heading with nothing under it says `none`. Every candidate from Phase 3 appears under exactly one of Confirmed / Suspected / Cleared; a candidate missing from all three is a report bug.

```markdown
## Verdict
<one sentence: N confirmed, M suspected, K cleared across S surfaces and T traced callers>

## Confirmed
- <scenario> — `file:line` — quoted failing output — fix in one line

## Suspected
- <scenario> — `file:line` — the exact evidence that would confirm or clear it

## Cleared
- <path> — cleared by <explicit arg | test name | no reachable caller>

## Coverage
- Surfaces traced: <list>
- Searches run: <pattern → paths → hit count>, one per surface
- Tests run: <command → quoted summary line>, or `tests: not run — <reason>`
- Not traced: <anything in scope you did not reach>

## Offer
<fixes by number; apply only what the user picks, one at a time, re-running the covering test after each>
```

- ❌ A prose narrative of what you looked at, ending in a paragraph called "Net risk." — the reader excavates the verdict, and candidates without a label can't be acted on.
- ✅ Verdict first, each candidate under one label, the searches and the quoted test line in Coverage — a reader who only sees this report knows what broke, what might, and what was checked.

## Examples

### Example 1: Default flipped

**User:** "I changed `list()` to exclude archived orders by default — what could this break?"

**Claude:** Inventories one surface (default `includeArchived` true → false). Greps callers: 6 hits, 4 pass the arg explicitly (cleared, cited), 2 omit it — the monthly report job (`jobs/report.ts:31`) and the admin export. Scenario for each. Finds `report.test.ts` fixtures include archived rows, runs it: red, quoted → confirmed. No test on the admin export → writes one, runs it red → confirmed. Reports 2 confirmed, 4 cleared, offers to add the explicit arg at both sites.

### Example 2: Nothing reaches

**User:** "regression check on this branch"

**Claude:** Two surfaces, both new files with one caller each, added in the same branch. Traces, finds no pre-existing callers ("searched `src/` for `parseInvoice\b`: 2 hits, both in this diff"), runs the suite, quotes green. Reports zero regressions with the searches listed. Does not invent a suspected item to look thorough.

## Anti-patterns

- ❌ Reviewing the diff's own quality — DRY, naming, error handling inside the changed lines. That's `code-review`; this skill looks outward.
- ❌ Stopping at compile-time callers. String keys, SQL text, templates, env names, and queue names don't import anything.
- ❌ "May be affected" without a scenario. If you can't say what goes wrong for whom, clear it or trace further.
- ❌ Declaring `confirmed` from reading. Confirmed means a test or run failed and you quoted it.
- ❌ Running the full suite once, seeing green, and reporting "no regressions" without tracing. Green proves only what the suite already asserted; the uncovered path is the risk.
- ❌ Padding a clean result with speculative items. Zero regressions with the searches listed is a good report.
- ✅ Surfaces inventoried, every caller cited or none-found recorded, scenarios ranked, tests run and quoted, verdict first.

## Notes

- Composes with: `code-review` (judges the change; run both on non-trivial diffs), `write-tests` (fills the uncovered paths), `create-pr` (calls this in its review gate), `goal-runner` (its regression step when a task touches shared code), `e2e-verify` (settles suspected items that need a real run), `safe-refactor` (owns behavior-preservation when the refactor is planned as such).
- Renames are the most common silent regression: after tracing a rename, grep the **old** name one more time across everything, including non-code files.
