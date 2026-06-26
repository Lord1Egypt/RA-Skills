---
name: violation-entry-template
---

# <YYYY-MM-DD-workflow-id-rule-id>

## Meta
- Workflow:    <workflow-id>
- Rule:        <rule-id>
- Rule type:   hard-do | hard-dont | soft-do | soft-dont | gate | checkpoint
- Severity:    hard | soft
- Status:      raw
- Captured:    YYYY-MM-DD HH:MM IST
- Step:        <which step was executing>

## What Happened
[What exactly was violated. Specific. No vague language.]

## Context
[What was being done when the violation occurred]

## Impact
[What is blocked, degraded, or at risk as a result]

## Post-Fix Required
- Required: yes | no
- Corrective action: [what needs to happen to resolve this]
- Autonomous fix possible: yes | no | uncertain

## Timeline
- YYYY-MM-DD HH:MM — Entry created
