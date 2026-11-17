# Collection contract

| Parameter | default | conservative | aggressive |
|---|---:|---:|---:|
| Minimum scroll pixels | 400 | 600 | 600 |
| Pause seconds | 1.5-3.5 | 1-2 | 0.8-1.8 |
| Long pause every steps | 10 | 10 | 15 |
| Long pause seconds | 4-8 | 3-5 | 2-4 |
| Step ceiling | 80 | 300 | 120 |
| Rate-limit backoff seconds | 60 | 120 | 30 |
| Active time ceiling minutes | 8 | 45 | 6 |

Start conservatively. For native scrolling use the greater of configured distance and 85% viewport height. Keep list and detail tabs separate. Count failures and expansion toward actual step/time limits. Split waits into segments of at most 60 seconds.

The conservative daily count ceiling is 500; preserve all collected in-window posts when a whole batch exceeds it. Native invocations are limited to 1800 seconds and pause around 1500 seconds as invocation_budget. Resume the same run/session only through authorized supported resume with remaining cumulative budget. Never reset window, raw data, steps or elapsed active time.

Freeze IDs from completed historical receipts. Archived posts are not new collection/analysis/detail work. List-visible IDs still provide pagination evidence. Only a batch without newly visible IDs contributes to the five-batch stall condition. Details do not advance pagination or window-boundary counters.

Three old list batches must be nonempty, newly visible, wholly before window_start, descending within batch and move backward without reversals. Actual verified chronological ordering permits boundary_observed. Unknown ordering yields window_boundary_unverified and partial. Five batches without new visible IDs yield pagination_stalled when not at the bottom, otherwise exhausted_observed; both remain partial.

Finish rechecks persisted events. Unexpanded text or unproved threads keep overall coverage partial, regardless of a separate window_coverage boundary. Steps and post counts are different metrics. Login/CAPTCHA stop immediately; clear rate limiting permits one backoff; repeated limits stop. Transient errors are not automatically rate limits. Stop reasons and original snapshots must reflect actual observations.
