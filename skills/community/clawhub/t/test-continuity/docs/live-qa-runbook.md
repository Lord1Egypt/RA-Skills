# Live QA Runbook

## Goal

Validate V2 on a real chat path after code/state integration.

## 10 manual scripts

1. parked topic
2. parked topic follow-up supplement
3. watchful state
4. delegated task
5. sensitive event
6. user reply closes active hook
7. duplicate follow-up suppression
8. dispatch cap
9. `/new` carryover
10. unrelated event does not overwrite active chain

## Expected outcomes

- staged/tracked state is observable
- carryover only appears when needed
- active hook closes on matched user reply
- duplicate or capped hooks do not keep re-firing
- different event chains stay separate
- frontstage output stays natural and does not leak internal labels

## If a script fails

Check:

- `event_kind`
- `event_chain_id`
- `source_stage`
- `followup_decision`
- `trigger_reason`
- `render_reason`
- `closure_reason`
- `continuity_source`
- `live_dispatch_result`

Primary trace file:

- `followup_trace.jsonl`

## Safe rollback

Keep a timestamped backup of:

- `scripts/personal_hooks.py`
- state files under the chosen data dir
- package-level config file

Then restore those files and rerun a minimal smoke check.
