# Meta-Pulse: review the watch portfolio

Read the scheduler's actual list and each watch's target, scope, cadence, authority, last check and stopping condition. Independently inspect the targets before deciding a watch is obsolete.

Classify each watch: keep, retune, duplicate, terminal, unknown or missing coverage. Present a compact diff with reasons. A review request alone authorises inspection, not creation of new monitoring scope or deletion of unrelated timers.

For an authorised cleanup, stop exact terminal or redundant watches through the scheduler's supported update/disable mechanism. Prefer an in-place cadence update over delete-and-recreate. If replacement is necessary, verify the replacement and prevent overlap before retiring the old watch; disclose any gap. Unknown targets stay unknown until checked or escalated.

Do not silently remove live coverage. Ask before adding new targets or expanding actions beyond the user's request. Preserve notification preferences and deduplication state. Read back every changed watch and report which remained active, stopped or unresolved. Keep unchanged-state silence unless the user explicitly asks for periodic reports.
