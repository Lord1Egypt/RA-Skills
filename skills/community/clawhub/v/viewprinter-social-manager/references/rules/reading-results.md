# reading-results: Measured when it was measured, and missing is not zero

## Priority: MEDIUM

## What goes wrong

A follower count is quoted as if it were live, or an account that has never been
measured is rendered as "0 followers" — which reads as failure rather than as
absence.

## Two honesty constraints

- **Numbers are as of the last sweep, not live.** Every account and post carries
  the time it was measured. Quote that time rather than implying the number is
  current.
- **An unmeasured account has no metrics at all** — not zeroes. Say it has not
  been measured yet.

## Per destination, not aggregate

`posts_list` reports numbers for each destination separately, because the same
post does not do the same numbers everywhere. Summing them into one figure throws away
the finding the user actually wants: which destination worked.

`accounts_list` with `metrics: true` gives followers, posts, total likes and
following per account, each with how far it moved over the period, ordered by
followers.

## Context

Read publication from each destination, not only the parent post. A parent may
still say `scheduled` while a destination reports `published` with its live URL.
Report queued, published, failed and unverified destinations separately. For a
trial reel, successful publication does not establish later automatic sharing
to followers. Compare trials with other trials of similar age; their initial
non-follower audience differs from an ordinary Reel's audience.

- Not every platform reports every metric. A metric a platform does not return
  is absent, not zero — the same rule as an unmeasured account.
