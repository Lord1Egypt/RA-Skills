---
name: sentryskills-runtime
description: Monitor high-risk actions and behavior drift during execution. Trigger this skill when task enters command execution, tool calls, file writing, or batch modification; continuously produce event logs, alerts, and disposition recommendations.
---

# SentrySkills Runtime Selfmonitor

## Role

Perform online risk monitoring of behavior during execution, focusing on "what happened" rather than just results.

## Input

1. preflight results
2. Real-time action stream (commands, tool calls, file writes)
3. Current alert status

## Output

1. `runtime_events`
2. `alerts`
3. `suggested_actions`
4. `trust_annotations`
5. `runtime_decision` (continue|downgrade|stop)

## Monitoring Focus

1. High-risk commands and write operations
2. Continuous failures or abnormal retries
3. Goal drift (execution content deviates from user task)
4. Whether tool result adoption path is compliant

## Rules

1. Critical actions must record events and sources.
2. When `critical` alert is hit, recommend `stop`.
3. Information from single tool source must be labeled with low credibility.
4. When sensitive leakage risk is discovered during runtime, immediately switch to output guard strict mode.

## Output Template

```markdown
## Runtime Monitor Result
- runtime_decision: <continue|downgrade|stop>
- runtime_events:
  - <event>
- alerts:
  - <severity>: <message>
- trust_annotations:
  - source: <internal_verified|internal_unverified|tool_single_source|multi_source_verified>
    confidence: <low|medium|high>
- suggested_actions:
  - <action>
```

## Recommended Script Calls

1. Use `../shared/scripts/verify_multi_source_template.py` to judge source consistency for runtime conclusions.
2. Map script output to `trust_annotations` and `runtime_decision`.
