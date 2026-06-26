# V2 Status

This is the current public mainline package for `personal-hooks`.

The package identity is V2. Publication should be judged against the explicit release acceptance matrix in [release-acceptance.md](release-acceptance.md).

## What V2 adds

- Phase 1 proactive chat
- Phase 2 arbiter integration
- proactive topic labeling and continuity summaries
- proactive writeback eligibility rules
- routine schedule / phase switching
- wake-seed path
- user-facing routine controls for sleep, wake, and work/dnd style suppression

## Acceptance line

V2 is considered structurally sound when:

- there is no structural routing failure
- there is no core arbiter misordering between task, wake seed, proactive, rhythm, and cron
- closure and writeback boundaries still hold
- `/new` continuity is not broken
- test and validation runs do not leave state pollution behind
- remaining issues can be handled as patch-level follow-up work

V2 would need further work if any of the following reappear:

- task/progress hooks lose to generic proactive follow-up
- sleep/work-dnd/wake phases fight each other
- closure becomes unreliable
- proactive self-pollutes long-term memory
- `/new` continuity misanchors or silently drops
- the implementation would still need a major path rewrite

## Current status

Current status: **V2 public mainline, publication gated by acceptance matrix**

- the validation line holds across arbiter, topic/summary, writeback, routine schedule, and isolated near-live checks
- no structural blocker remains in the V2 routing
- remaining concerns should now be treated as release-gate failures, neutrality gaps, or documentation gaps rather than redesign-level blockers

## What is still patch-level

- phrasing/tone tuning for proactive messages
- lexical tuning for natural switches and suppression phrases
- cadence tuning for real-world use after observation
- documentation refinement
- small thresholds or guard adjustments if observation exposes edge cases

See also [v2-known-limits.md](v2-known-limits.md) for the condensed reviewer-facing list.

## What still needs explicit release proof

- language neutrality at the public-package level
- timezone / offset neutrality at the public-package level
- `/new` + low-information greeting behavior under the release acceptance matrix
- host/adapter boundary checks for web/live hosts when live delivery is demonstrated

## Recommended next step

Execute the release acceptance matrix and treat any miss as a public-package gap to fix before publication.

If the matrix passes, the next step should be publication work, not another large extraction or rewrite round.
