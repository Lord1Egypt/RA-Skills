## Description:

Analyzes office workstation video for sitting duration and posture indicators, then returns alerts and a structured report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Office health program operators and developers can use the skill to review workstation video for prolonged sitting and posture alerts. It provides visual monitoring results, not medical diagnosis or treatment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workplace video may be uploaded for external processing even when export-only behavior is selected.

Mitigation: Avoid sensitive footage until the publisher fixes export-only behavior; confirm authorization for external processing and the provider's retention and deletion practices.

Risk: The user's selected API server may be ignored, so footage could be sent to an unexpected service.

Mitigation: Verify the processing destination and defer sensitive use until API-server selection is fixed.

Risk: Stored accounts or tokens and credential-bearing logs could expose access data.

Mitigation: Protect the workspace database and credential-bearing logs, and confirm how stored accounts and tokens can be removed.

## Reference(s):

- [Office posture analysis API reference](references/api_doc.md)
- [Analysis API response and error reference](skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis Results, Guidance]

**Output Format:** [Text with structured JSON results and a report export link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include posture metrics, sitting duration, alert type and message, and a session summary; results are not a medical diagnosis.]

## Skill Version(s):

1.0.14 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
