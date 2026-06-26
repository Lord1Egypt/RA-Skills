# Changelog

All notable changes to `swarm-coordinator` are documented here.

## [1.1.0] - 2026-04-25

### Added

- Added ClawHub-ready metadata with a standard `name` and public-facing `description`.
- Added a complete swarm execution workflow:
  - decide whether swarm is justified
  - define roles and ownership
  - create a `SwarmCommand`
  - validate before publish
  - publish/subscribe and track state
  - collect results and close the loop
- Added four core swarm invariants:
  - single task owner
  - explicit state
  - bounded cost
  - verifiable completion
- Added token-budget downgrade rules for budget pressure, repeated failure, and over-budget execution.
- Added negotiation rules for agent conflicts, blocked dependencies, and deadline/budget tradeoffs.
- Added failure-handling guidance for invalid commands, unavailable targets, blocked dependencies, missed deadlines, duplicate owners, incomplete results, and repeated failure.
- Added safety boundaries for destructive, public, costly, irreversible, and ambiguous swarm actions.
- Added a standard output format for swarm plans, commands, budget policy, fallback, and verification.
- Added `test-prompts.json` for Darwin-style future evaluation and regression testing.
- Added `darwin-results.tsv` to record one optimization round.

### Improved

- Refocused the skill for public multi-agent coordination use cases instead of a private agent-team-only workflow.
- Made role names generic and portable across different agent platforms.
- Improved practical guidance for when **not** to use a swarm.
- Improved operational safety by requiring explicit owner, budget, dependency, fallback, and done criteria.
- Improved validation and testing support for the bundled protocol implementation.

### Fixed

- Fixed protocol package import so Redis remains optional for protocol-only tests.
- Fixed missing `Tuple` import in `coordinator/swarm_protocol.py`.
- Fixed schema validation for nullable status fields such as `assigned_to`, `started_at`, and `completed_at`.

### Verified

- Ran protocol regression tests:

```bash
python3 -m pytest tests/test_swarm_protocol.py -q
```

Result:

```text
11 passed
```
