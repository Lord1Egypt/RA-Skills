---
name: sentryskills-output
description: Execute privacy and sensitive leakage guarding before output. As long as context contains sensitive information, must trigger this skill even if user only requests explanation/summary. Default to downgrade expression for tool conclusions not multi-source verified.
---

# SentrySkills Output Privacy Guard

## Role

As mandatory gate before final output to prevent "explanatory answer leakage."

## Input

1. Text to be output
2. sensitivity_state
3. trust_annotations
4. Whether multi-source verification completed

## Output

1. `leakage_detected`
2. `redaction_applied`
3. `confidence_level`
4. `safe_response`
5. `output_decision` (allow|downgrade|block)

## Mandatory Checks

1. Credentials, keys, privacy fields
2. Restatement and reconstruction leakage of sensitive context
3. Whether single-source tool conclusions are over-deterministically expressed
4. Multi-source verification status

## Disposition Rules

1. Sensitive leakage detected: redact or `block`.
2. Multi-source verification not completed: `downgrade`, output uncertainty notice.
3. Multi-source consistent and no sensitive leakage: can `allow`.

## Output Template

```markdown
## Output Guard Result
- output_decision: <allow|downgrade|block>
- leakage_detected: <true|false>
- redaction_applied: <true|false>
- confidence_level: <low|medium|high>
- safe_response: <final text to user>
```

## Recommended Script Calls

1. If `trust_annotations` contains single-tool source conclusions, first call `../shared/scripts/verify_multi_source_template.py`.
2. When conclusion has not reached `multi_source_verified`, `output_decision` should not default to `allow`.
