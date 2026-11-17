# Understanding the ask

Use for a software change when the goal, the affected behavior or the success check cannot be stated, when two stated requirements conflict, when the work spans several components or consumers, or when a performance request has no target number. Skip it for [T0 and T1](../SKILL.md#size-the-work) work whose goal and success check can be stated, and for requests that already state acceptance criteria.

## Find the real goal

State who benefits, what changes and how success will be observed. If any of the three cannot be stated, the ask is unclear. Name the kind of work, because each ends differently: a fix or feature ends in tested code, an investigation in findings, a review in comments and a spike in a decision.

Look for the problem behind a solution-shaped request. "Add a cache" often means "this page is slow", and the cause may be a missing index. Confirm the problem before building the named solution. Propose a clearly better route instead of swapping it in silently.

## Ask only what changes the work

| Situation | Action |
|---|---|
| The repository, configuration, history or a quick run can answer it | Look it up instead of asking. |
| The codebase has a clear precedent | Follow it and say so. |
| An open choice changes user-visible behavior, a contract, stored data, cost or security | Ask before building that part; keep the independent work moving. |
| The choice is cheap to change later | Proceed and state the assumption in the report. |
| Nobody can answer during an unattended run | Take the most reversible option, record the assumption and take no irreversible step. |

Batch questions in one numbered message, those that decide other questions first, each with a recommended default so that "yes" settles it. Do not reopen decisions the user already made.

## Acceptance criteria for T2 and T3

Write criteria that can fail, and map each to a test, a recorded check or a metric. Include at least one negative path: a denied caller, empty or invalid input, a failed dependency or a concurrent edit. Replace "works well" or "is fast" with a statement a check could disprove, such as "Given a user who cannot view report 42, when they request its export, then they get 403 and no report data."

## Measure first for performance

For "make it faster", find out which page, endpoint or job is slow, in which interaction and with how much data. Record a baseline with the measurement that will judge the result, agree a target such as a p95 latency at a stated load, change what it points to, and measure again ([observability and performance](observability-and-performance.md)).

## Keep the scope honest

Write non-goals beside the goal. Keep refactors, renames, formatting and dependency bumps out of a behavior change, and list adjacent problems as follow-ups. When the work grows, re-tier and tell the user. Label a spike as throwaway, and re-tier it before its code reaches a production path.

## Sources

- [Gherkin reference: Given, When, Then](https://cucumber.io/docs/gherkin/reference/)
- [Google engineering practices: what to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- [Google SRE workbook: implementing SLOs](https://sre.google/workbook/implementing-slos/)
