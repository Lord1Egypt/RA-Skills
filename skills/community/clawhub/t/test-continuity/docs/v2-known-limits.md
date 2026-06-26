# V2 Known Limits

This note lists the remaining limitations for the current V2 package.

These are not treated as structural blockers. They are the areas that may still
need patch-level tuning before or during publication review.

## Current known limits

- proactive wording can still be tuned for warmth and naturalness
- phrase lists for state switches and suppress triggers can still be tightened
- cadence thresholds may still need adjustment after more observation
- package documentation can still be smoothed and clarified

## What is not a current blocker

The following are **not** currently considered open structural blockers:

- arbiter ordering between task, wake seed, proactive, rhythm, and cron
- closure cleanliness
- proactive writeback boundary
- `/new` continuity alignment
- state cleanup after validation

## What would still block publication

If any of the following reappear, the package should not be considered
ready to freeze:

- task/progress follow-up loses to generic proactive behavior
- sleep, wake, or work/dnd phases conflict in a way that breaks routing
- proactive writes into long-term memory without stronger confirmation
- `/new` carryover misanchors or drops a tracked thread
- validation or review runs leave package contamination behind

## Practical takeaway

At this point, the package should be judged against the explicit release gate:

- tuning issues are acceptable
- structural path failures are not
- publication still requires the matrix in `docs/release-acceptance.md`
