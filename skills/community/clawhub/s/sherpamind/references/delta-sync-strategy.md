# Delta Sync Strategy

> SherpaDesk API reference: <https://github.com/sherpadesk/api/wiki>

## Goal

Keep SherpaMind fresh enough for:
- near-real-time visibility into new and active tickets
- low API pressure
- eventual correction of older ticket drift
- reliable local analytics and OpenClaw retrieval

## Current live findings that matter

From low-volume live probing against the real account, we currently know:

- `status=open` and `status=closed` filters work on `/tickets`
- the returned ticket rows include useful timestamps and activity signals such as:
  - `created_time`
  - `updated_time`
  - `closed_time`
  - `is_new_tech_post`
  - `is_new_user_post`
  - `next_step_date`
  - `status`
- naïve `updated_time=<date>` and `created_time=<date>` query params appear to be **ignored** by `/tickets`
  - even absurd future dates returned the normal first page of results
- page order looks recent-ish, but we do **not** yet have proof that it is strictly sorted by `updated_time`
- the documented `Content-Range` header was **not** observed in live ticket-list responses during our probes

## Conclusion

The safest current assumption is:

1. we **cannot rely** on server-side updated-since filtering yet
2. we **cannot rely** on strict stable ordering yet
3. we **can rely** on status filtering and on ticket rows carrying their own timestamps/activity hints

That means the right delta strategy is **tiered recency rescans**, not blind full-history rescans and not a fragile single-watermark design.

## Adopted operating model

This is now the intended SherpaMind direction:
- maintain a local list/state of ticket IDs observed to be open
- poll the hot open lane every ~5 minutes
- when a ticket leaves the observed open set, remove it from the active-open tracking set
- treat closed tickets newer than 7 days as **warm**
- treat closed tickets older than 7 days as **cold** and audit them on a slow rolling cadence

## Recommended operating model

### 1. New-ticket watcher lane
Purpose:
- detect newly created tickets with high freshness

Approach:
- poll the first few pages of `status=open`
- run every ~5 minutes
- compare the returned ticket IDs against the local DB + watcher state
- alert on unseen IDs

Why this works:
- new tickets should appear near the front of the active/open set
- we only need high freshness for the hot active slice, not for the entire historical corpus

### 2. Hot active-ticket sync lane
Purpose:
- keep active/in-flight tickets fresh enough for operational use

Approach:
- poll the first N pages of `status=open`
- run every ~5 minutes
- upsert all returned open tickets
- maintain a local active-open ticket ID set
- when a ticket disappears from the observed open slice, remove it from the active-open set and hand it off to warm/closed handling
- optionally prioritize detail enrichment for rows where:
  - `updated_time` changed
  - `is_new_user_post` changed
  - `is_new_tech_post` changed
  - `next_step_date` changed
  - `status` changed

Default starting shape:
- first 3-10 pages of open tickets
- tune upward or downward once we see real open-ticket volume

### 3. Warm recently-changed ticket lane
Purpose:
- catch tickets that recently closed or fell out of the hot open pages
- catch edits to recent history without rescanning everything

Approach:
- rescan a larger recent slice of `status=closed`
- treat closed tickets newer than **7 days** as warm by default
- run every few hours
- compare `updated_time`, `closed_time`, and key fields against local state

This is the lane that protects us from:
- recent closures
- reopens
- post-close edits
- short-lived tickets that are created and closed between hot-lane runs

### 4. Cold historical audit lane
Purpose:
- preserve eventual consistency for older tickets
- converge historical detail coverage quickly enough for meaningful analysis

Approach:
- scan older closed-ticket pages in rolling batches
- before the first full historical pass completes, use spare hourly headroom aggressively to accelerate cold auditing and enrichment
- after the first full historical pass completes, slow the cold lane back down and keep it as a maintenance/audit loop
- record the last audited page/range locally
- persist whether the cold corpus has completed at least one full pass

This is our answer to:
- “closed usually means lower churn, but not zero churn”
- “historical analytical depth should ramp quickly once, then settle into slower maintenance”

### 5. Periodic deep audit lane
Purpose:
- guard against silent API weirdness or missed slices over long periods

Approach:
- very infrequent long-tail rescan
- tiny bounded slices per run
- never try to re-read the whole corpus in one go

## Why not treat closed tickets as immutable?

Because that would be convenient, not trustworthy.

Closed tickets can still change because of:
- backfilled notes
- technician/user updates
- categorization changes
- account/user reassignment
- resolution metadata cleanup
- reopen/close cycles

So the correct posture is:
- **open tickets = high-churn, sync aggressively**
- **closed tickets = lower-churn, sync lazily but not never**

## Local sync state we should keep

SherpaMind should persist local sync state for each lane, for example:

- watcher:
  - last poll time
  - recent seen ticket IDs / newest observed ticket number or created timestamp
- hot open lane:
  - pages scanned
  - last run time
  - newest/oldest observed `updated_time` in the scanned window
- warm lane:
  - last successful open-window refresh
  - last successful recent-closed refresh
- cold audit lane:
  - last closed page/range audited
  - audit cycle progress

This allows the scheduler to be intentional instead of stateless.

## Freshness target recommendation

Given the documented 600 requests/hour limit, the current default pacing, and the need for operational awareness:

- **new/open active slice:** target ~5-minute freshness
- **recently closed / recent history:** target ~1-6 hour freshness
- **older historical backlog:** target daily/weekly eventual consistency

That is a sane starting point and should be enough for the visibility goals currently described.

## Optimization rules

1. Prefer list endpoints over detail endpoints for broad change detection.
2. Only fetch expensive per-ticket enrichments for tickets that look changed or strategically important.
3. Separate **freshness lanes** from **depth lanes**.
4. Keep every sync idempotent.
5. Log observed API behavior whenever the live system contradicts the docs.

## Proposed next implementation order

1. finish/verify the initial seed snapshot
2. implement watcher/new-open polling lane
3. implement hot open-ticket delta lane
4. implement warm recent-closed reconciliation lane
5. add cold rolling audit state and scheduler support
6. add retrieval/document refresh hooks so changed tickets reflow into OpenClaw-facing search indexes
