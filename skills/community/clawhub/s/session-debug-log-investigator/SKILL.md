---
name: "session_debug_log_investigator"
description: "Use when diagnosing a failing or confusing Claude Code session by enabling debug logging, tailing recent logs, and explaining warnings or errors."
---


# Session Debug Log Investigator

Use this skill to diagnose runtime issues in an agent session.

## Workflow
1. Enable debug logging if it is not already active.
2. Read the latest portion of the debug log instead of the whole file.
3. Search for warnings, errors, and repeated failure patterns.
4. Cross-check config files that can explain the behavior.
5. Summarize likely causes and next reproduction steps.

## Guardrails
- Tail logs instead of loading giant files.
- Separate configuration issues from product/runtime bugs.
- If logging was just enabled, ask for reproduction before concluding too much.

## Example Requests
- Help me understand why this Claude Code session is misbehaving.
- Turn on debug logging and diagnose this issue from the latest logs.

## Inputs
- Issue description
- Current log availability
- Relevant settings files

## Outputs
- Error or warning analysis
- Likely causes
- Suggested reproduction or next steps

## Success Criteria
- Recent logs were interpreted correctly.
- The diagnosis distinguishes config vs runtime issues.
- Follow-up steps are specific.

## Non-Goals
- Reading giant logs in full without need
- Pretending to diagnose pre-log activity that was never captured

## Source Provenance
Derived from `src/skills/bundled/debug.ts`.
