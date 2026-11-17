# wdp-prd-en Test Scenarios

All scenarios are dry-run in a temporary scratch project directory. Each scenario: Setup (prepare environment) → Action (execute the corresponding command section in SKILL.md) → Expected (check invariants).

## S1 Initialization + Card Creation
- Setup: an empty scratch project `dryrun-1/` (no `.wdp-prd` pointer).
- Action: follow SKILL.md "Initialization"; then use `/wdp-prd-new` to create a requirement.
- Expected:
  1. `<PRD_ROOT>/<slug>/` is created containing `backlog/`, `plans/`, `execution-plan.md`; `docs/superpowers/specs/` is created inside the project.
  2. `.wdp-prd` content = the absolute path of that global root (`<PRD_ROOT>/<slug>/`).
  3. `backlog/R-001.md` exists with all frontmatter fields (id/title/status/priority/depends_on/conflicts_with/created/updated), status=draft.
  4. created and updated are both today's date.

## S2 List + Update
- Setup: 3 cards exist: R-001(draft,high), R-002(draft,low), R-003(confirmed,medium).
- Action: run `/wdp-prd-list`; then run `/wdp-prd-update R-002` (change priority to high, status to confirmed).
- Expected:
  1. The list outputs a table with id/title/status/priority/dependencies, all 3 rows complete with correct fields.
  2. Row order by priority high→low: R-001(high) → R-003(medium) → R-002(low); by created ascending within the same priority.
  3. After update, R-002's priority=high, status=confirmed, updated=today.
  4. created is unchanged.
- Action: run `/wdp-prd` (main entry).
- Expected: shows the backlog summary + command hints.

## S3 Scheduling Report
- Setup:
  - R-001 confirmed, no dependencies, conflicts_with=[R-002].
  - R-002 confirmed, no dependencies.
  - R-005 confirmed, depends_on=[R-002] (dependency R-002's actual state is confirmed).
  - R-007 confirmed, depends_on=[R-099], and R-099's state is cancelled.
- Action: run `/wdp-prd-dispatch` step 1 (only output the scheduling status report; S3 only observes the report, does not pick or dispatch).
- Expected:
  1. Ready to dispatch = [R-001, R-002, R-007]: the mutually-conflicting pair R-001 and R-002 are both listed, with the hint that "they conflict, pick only one".
  2. R-005 → report `⏳ wait for R-002(confirmed) to finish` (dependency R-002's actual state is confirmed, not in-progress).
  3. R-007 → not blocked (cancelled dependency counts as satisfied), listed as ready.

## S4 Dispatch
- Setup: scratch project `dryrun-4/`, a git repository; R-001 and R-002 both confirmed, no conflicts, no dependencies.
- Action: run `/wdp-prd-dispatch`, pick [R-001, R-002].
- Expected:
  1. The report correctly shows the ready list; the concurrency cap is not exceeded.
  2. One background subagent is spawned per requirement; R-001/R-002 status → in-progress.
  3. `execution-plan.md` is rewritten: contains in-progress=[R-001,R-002], ready=[], blocked=[], conflicts=[].
  4. After the subagent returns its report, the cards → needs-review.
- Action: re-run dispatch in a non-git project (or a git repo with isolation capability removed).
- Expected: clearly warns `cannot isolate via worktree, falling back to serial/non-isolated`, no silent failure.

## S5 Full Lifecycle
- Setup: a single card R-001 starting from draft, in a git repository.
- Action: run in sequence confirm → dispatch → simulate the subagent returning a report → accept.
- Expected:
  1. The full state migration draft→confirmed→in-progress→needs-review→accepted→done is correct throughout.
  2. The accept flow includes: merging the worktree branch, running the full test suite, code review, presenting to the user for confirmation.
  3. After done, the card's Acceptance Record section is filled with test results and the review verdict.
  4. Any gate (test failure / review not passed / user not confirming) → does not enter done, returns to needs-review.

## S6 Error Branches
- Setup:
  - R-001 and R-002 both confirmed and mutually conflicts_with (same-batch conflict).
  - R-003 depends_on=[R-004], R-004 depends_on=[R-003] (dependency cycle).
  - R-005 depends_on=[R-999] (missing dependency).
  - R-008 confirmed, conflicts_with=[R-009]; R-009 is in-progress (the conflicting target is under development).
  - PRD_MAX_CONCURRENT lowered (e.g. =0), so cards that should be dispatchable are suppressed by the concurrency cap.
- Action: `/wdp-prd-dispatch` everything.
- Expected:
  1. Same-batch conflict → prompt to pick only one, no silent parallel execution.
  2. Dependency cycle → clearly report the cycle (R-003↔R-004), do not dispatch.
  3. Missing dependency → report `dependency R-999 does not exist; check depends_on`.
  4. R-008 → report `⚠ conflicts with R-009(dev in progress); wait for it or let the user decide`.
  5. Concurrency cap exceeded → report `concurrency cap reached; accept what's in hand first`, and suppressed cards do not appear in the ready list.
