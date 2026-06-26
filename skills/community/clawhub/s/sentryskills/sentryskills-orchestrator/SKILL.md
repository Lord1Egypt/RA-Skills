---
name: sentryskills-orchestrator
description: Orchestrate security self-checks uniformly in code agent tasks. Trigger when involving command execution, file modification, tool/network calls, or sensitive context explanation.
---

# SentrySkills Self Guard Orchestrator

## Role
Responsible for task-level security orchestration, does not directly implement underlying detection algorithms. Responsibilities:
1. When to trigger sub-skills
2. When to block or downgrade
3. When to allow output

## Sub-skill Dependencies
1. `sentryskills-preflight`
2. `sentryskills-runtime`
3. `sentryskills-output`

## Trigger Conditions
Trigger if any condition is met:
1. Command execution, script execution, code rewriting, batch file operations
2. Reading data that may contain sensitive information
3. External tool/network data used as conclusion basis
4. Explanation requests where context contains sensitive information

## Standard Flow
1. preflight: output `risk_summary`, `sensitivity_state`, `allowed_actions`
2. runtime: record events, alerts, and credibility annotations
3. output guard: detect leakage and execute redaction or refusal
4. final decision: give `allow|downgrade|block`

## Orchestration Rules
1. If preflight determines high sensitivity and request for direct original output, default to拒绝.
2. If critical alert appears during runtime, stop execution and enter safe output mode.
3. Must downgrade expression when only single tool source exists.
4. Can upgrade to high-confidence conclusion only after multi-source verification passes.

## Output Contract
1. Main log uses JSONL event stream, following `../shared/references/guard_event.schema.json`.
2. Field specifications follow `../shared/references/field_contract.md`.
3. For historical compatibility, can use `--out` to produce single-round summary JSON (not main contract).

## Runtime Integration
1. Use `../shared/scripts/self_guard_runtime_hook_template.py` as minimum integration layer.
2. Each round takes task JSON as input, writes event log and session state (`sensitivity_state` persistence).
3. Hook this script to pre-response hook to ensure explanatory responses also go through output guard.

## Mandatory Execution Protocol
1. Must execute `../shared/scripts/self_guard_runtime_hook_template.py` before final response; text-only inference skipping script is prohibited.
2. Input JSON must include `project_path` (current project absolute path); logs default to `./sentry_skill_log/`.
3. Final response must include minimum evidence fields:
   - `self_guard_final_action`
   - `self_guard_trace_id`
   - `self_guard_events_log`
4. If hook fails or is unavailable, must explicitly declare "security self-check not completed" and adopt conservative output strategy.
