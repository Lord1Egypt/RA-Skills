# graphtrail changelog

Earlier history lives in the repo-level CHANGELOG.md.

## 0.1.1 - 2026-07-09

- Added a "Brigade loop" section: verify and run receipts carry `code_graph_delta`, `brigade receipts export miseledger --new-only --import` archives them, the next run can attach a MiseLedger evidence brief, and `brigade operator checkup` reports graph and ledger status with the last brief hit rate.
- The `diff` entry now notes Brigade attaches graph deltas to verify and run receipts automatically and records `context_eval.brief_hit_rate` when a pre-run code-graph brief is compared to the post-run delta.

## 0.1.0 - 2026-07-08

- Added skill.json metadata (tests, changelog) for the Brigade skill registry.
