## Description:

Analyzes a resting pet video to estimate breathing rate, compare it with species and size ranges, and return an informational alert report; it does not provide a veterinary diagnosis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners, animal-care staff, and veterinary teams can review a resting pet video for an estimated respiratory rate and an alert when the result falls outside reference ranges. Treat the report as informational and seek veterinary care for persistent or urgent concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags possible external video uploads, account creation, and stored authentication data.

Mitigation: Review the service endpoint and authentication behavior before use, and submit only videos and credentials you are authorized to share.

Risk: The security review marks the skill suspicious and notes a gap between its advertised monitoring purpose and the behavior demonstrated by reviewed code; the scan was partial.

Mitigation: Review the complete skill and confirm its behavior matches the intended monitoring task before relying on its reports.

Risk: Respiratory-rate estimates could be mistaken for a veterinary diagnosis or delay care.

Mitigation: Treat results as informational only and contact a veterinarian for persistent abnormalities or urgent symptoms.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-respiratory-rate-abnormal-detect-analysis)
- [API interface notes](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured respiratory-rate report as text or JSON; Markdown tables for report lists.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are informational and are not a veterinary diagnosis.]

## Skill Version(s):

1.0.11 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
