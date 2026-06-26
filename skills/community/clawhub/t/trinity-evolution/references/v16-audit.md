# v16.0 Audit Baseline

This reference summarizes the public, non-sensitive v16.0 baseline for the Trinity/OpenClaw self-evolution loop.

## Release Meaning

v16.0 is a closed-loop self-evolution baseline for OpenClaw. It is intended to keep capability improvement claims grounded in independent validation and practical user impact.

The baseline covers:

- Direction discovery from source-backed signals.
- Capability candidate materialization.
- Repair and holdout creation.
- External or configured judge scoring.
- Repair-level promotion gates.
- Failure preservation and conservative replacement repairs.
- Plain-language user-facing progress reporting.

## Readiness Criteria

The system should be considered ready only when:

- The local status command reports the expected version.
- The preflight command passes.
- There are no pending holdouts for the current release gate.
- Current repairs have enough independent external passes.
- Current repairs have no current external failures.
- At least one explicit positive validation exists where required.
- Internal metrics or auto-scored results are not used as verified evidence by themselves.

## Practical Reporting Standard

A useful report should answer:

- What OpenClaw can now do better.
- Why that matters in normal use.
- How the user should use the improved behavior.
- What evidence supports the claim.
- What remains uncertain or needs future validation.

Avoid reporting only internal framework names or raw validation counts without explaining user impact.
