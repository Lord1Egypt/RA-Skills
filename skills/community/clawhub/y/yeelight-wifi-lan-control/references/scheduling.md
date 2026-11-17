# Host Scheduling

The Skill stores portable schedule drafts; the AI Host owns recurrence. The Skill
never installs or edits cron, launchd, systemd, Windows Task Scheduler, or a daemon.

When a scheduler capability exists, `schedule.create_draft` returns a structured
request with:

- `scheduleId`, scene ID/revision/hash, IANA timezone, closed cadence and target;
- lifecycle action, idempotency key, and `createdBy` marker;
- explicit consented actions and a bounded occurrence shape.

The Host creates the exact task and calls `schedule.bind` with the immutable task ID,
task revision, matching `scheduleId`, idempotency key, and `createdBy`.
Pause/resume/update/remove use the same exact ownership. Binding or deletion failures
remain pending and future runs fail closed.

The returned scheduler request uses opaque local refs for `scheduleId`, scene IDs, and
device/room/group targets. Pass those fields back unchanged in the Host reply; the
runtime resolves them only against the current private store before validating the
reply.

Each run request must provide `scheduledAt` as a UTC RFC3339 value ending in `Z`,
`localDateTime` as `YYYY-MM-DDTHH:MM`, and a numeric `fold` (`0|1`) for daily or
weekly cadence. The runner validates that the UTC instant formats to that local
minute in the schedule's IANA timezone and matches the cadence; once cadence may
omit `fold` (it is normalized to `0`). It then derives the private occurrence key
from the stored schedule ID plus canonical UTC instant. Any caller-supplied
`occurrenceKey` is ignored and cannot create a second lease. The canonical metadata
is recorded before any device write, a lease is acquired, and duplicate UTC
occurrences are skipped. Missing, ambiguous, malformed, or cadence-inconsistent
metadata fails closed without changing the store. A crash leaves `uncertain`;
missed occurrences do not catch up and non-idempotent actions are never
automatically replayed. Real Host APIs and platform DST behavior remain
capability-specific and unverified.
