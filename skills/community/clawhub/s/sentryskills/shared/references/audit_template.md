# Audit Template (Legacy)

This template is for historical compatibility scenarios: generating single-turn audit JSON.

The main contract has migrated to JSONL event streams: `guard_event.schema.json`.

## Usage Recommendations
1. For new integrations, prioritize using `self_guard_runtime_hook_template.py` + `--events-log`.
2. Only use single-turn audit JSON when backward compatibility is required.
3. Single-turn JSON can be generated as a summary by the runtime hook via `--out`.

## Minimum Required Fields
1. `session_id`
2. `policy_profile`
3. `final_action`
4. `decision_reason_codes`
5. `matched_rules`
