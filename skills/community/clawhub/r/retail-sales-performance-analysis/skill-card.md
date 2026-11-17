## Description:

Analyzes store or clerk retail sales performance across comparison periods, attributes changes to order count or average transaction value, detects anomalies, and returns diagnostic findings with improvement recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwyang7](https://clawhub.ai/user/gwyang7)

### License/Terms of Use:

MIT-0

## Use Case:

Retail operators, store managers, and business analysts use this skill to compare store or clerk performance across periods, diagnose revenue movement, identify sales anomalies, and generate action-oriented recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill loads an external API client from a hard-coded local path, so the data-access code may be outside the reviewed artifact.

Mitigation: Install only in an authorized retail BI environment and confirm the external API client path is trusted and controlled before use.

Risk: The store-versus-clerk data scope is unclear, which may expose clerk-level analysis before explicit handling and privacy guidance are reviewed.

Mitigation: Limit use to store-level or otherwise authorized requests until clerk handling, input validation, and privacy guidance are confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gwyang7/skills/retail-sales-performance-analysis)
- [Publisher profile](https://clawhub.ai/user/gwyang7)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON analysis result with findings, attribution, risks, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authorized retail BI data access for the requested store or clerk and time window.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
