# Field Contract

This document defines the core field contracts for TrinityGuard self-guard.

## 1. Event Log Primary Contract (Recommended)

The primary output is JSONL, with one event per line. See: `guard_event.schema.json`.

Each event must contain at minimum:
1. `ts`
2. `trace_id`
3. `session_id`
4. `turn_id`
5. `policy_profile`
6. `event_type`
7. `risk_level`
8. `decision`
9. `reason_codes`
10. `matched_rules`

`event_type` values:
1. `hook_start`
2. `preflight_result`
3. `runtime_result`
4. `output_guard_result`
5. `final_decision`
6. `hook_end`
7. `hook_error`

## 2. final_decision Event Extended Fields

1. `final_action`: `allow|downgrade|block`
2. `retention`: Tiered retention summary
3. `residual_risks`: `string[]`
4. `audit_notes`: `string[]`

## 3. output_guard Summary Fields

1. `output_guard.safe_response`: Final safe output for users
2. `output_guard.source_disclosure`: Source appendix text for single-source downgrades
3. `output_guard.source_items`: `[{source_id, source_type, confidence, reason}]`

## 4. Key Consistency Rules

1. If `runtime_result.decision = stop`, final `final_action` cannot be `allow`.
2. If leakage is detected in a highly sensitive session, final action should be `block` or stricter.
3. For single-tool-source conclusions, at minimum trigger downgrade or uncertainty warning.
4. If `output_decision=downgrade` and reason codes include `OG_SINGLE_SOURCE_DOWNGRADE`, must output `source_disclosure` and at least one `source_items` entry (explicitly state "Source information missing" when no sources available).

## 5. Compatibility Notes

Historical single-turn audit JSON can still be generated as a summary via `--out`; complete contract is defined by JSONL events.
