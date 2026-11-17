# Change Severity Heuristics

Use these as decision aids, not rigid scoring.

## High

A change can alter legal/financial obligation, safety, approval authority, eligibility, external interface compatibility, data interpretation, or automated behavior.

## Medium

A change affects workflow efficiency, ownership, reporting, training, non-critical defaults, or operational expectations.

## Low

Editorial clarification, formatting, examples, or metadata with no credible behavior change.

When impact depends on unknown dependencies, label it `potential` and use `know-enough` to inspect those dependencies only if the user needs impact analysis.
