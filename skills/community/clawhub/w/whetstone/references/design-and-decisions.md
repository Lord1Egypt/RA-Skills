# Design and decisions

Use when choosing an approach, library, datastore, service boundary or architecture, or when a change crosses module, service or team boundaries.

## Frame before choosing

Describe the problem in terms of users or operators, with current numbers where they exist: "p95 page load is 4.1 s; the target is 1.5 s." List the goals, non-goals and constraints, such as deadlines, budget, compliance, existing contracts, team skills and supported platforms. Name the two or three qualities that matter most, for example latency, cost or auditability, because they cannot all be maximized.

## Compare real options

Set out at least two viable options, including doing nothing when that is viable. Compare them on those qualities plus cost of reversal, operational burden, security impact and migration path. When one unknown dominates, such as a library's behavior or a performance limit, settle it with a time-boxed spike, then discard the spike or re-tier it before reuse. State the choice, the reason and the evidence that would reopen it.

## Prefer boring and reversible

Use the stack the team already runs unless there is evidence it cannot work. Every new language, framework, datastore or managed service is something to operate, patch and staff for years. Decide cheap-to-reverse choices quickly. Slow down for expensive ones: data models, public contracts, vendor lock-in and security architecture.

Change running systems in releasable steps. Add the new form beside the old one, move consumers, then remove the old form ([contracts](api-design.md) and [data](data-and-privacy.md) show how). Replace a subsystem piece by piece behind a stable interface rather than in one rewrite.

## Design for operations

For each new component, decide how it is configured without code changes, how it starts and stops cleanly, what happens when each dependency is slow or down, and what will show that it works ([observability and performance](observability-and-performance.md)). Estimate the running cost at expected load and at ten times that load.

## When a decision record is worth writing

Write one when a decision is expensive to reverse, affects other teams, or will make a future reader ask why the code looks this way. Cover the context, options, decision, consequences and what would prompt a revisit. Store it where the repository keeps such records, and mark a reversed decision as superseded instead of deleting it. For most T2 choices, a note in the pull request is enough. The [decision record template](../templates/decision-record.md) is optional.

## Sources

- [Google SRE book: simplicity](https://sre.google/sre-book/simplicity/)
- [Architectural decision records](https://adr.github.io/)
- [MADR decision record format](https://adr.github.io/madr/)
- [Parallel change](https://martinfowler.com/bliki/ParallelChange.html)
- [Strangler fig application](https://martinfowler.com/bliki/StranglerFigApplication.html)
- [The Twelve-Factor App](https://12factor.net/)
