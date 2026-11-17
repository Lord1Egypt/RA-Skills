## Description:

Analyzes video of a resting pet to estimate breathing rate and flag readings outside species and body-size reference ranges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners and animal care staff can use resting-pet video to estimate respiratory rate and receive an alert when a reading falls outside reference ranges. The results are for health monitoring and do not provide a medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pet video or identity information may be sent to external services, and the reported behavior may not clearly match the pet-monitoring purpose.

Mitigation: Review the skill's data handling and actions before use, and share only footage or identity information you are authorized and comfortable sending to external services.

Risk: Account setup and token handling may not fit the installer's requirements.

Mitigation: Review how accounts and tokens are handled before installation and use.

Risk: The security assessment is partial because a local reference could not be resolved.

Mitigation: Review the unresolved reference before relying on the assessment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-respiratory-rate-abnormal-detect-analysis)
- [Publisher profile](https://clawhub.ai/user/smyx-sunjinhui)
- [API interface notes](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Markdown]

**Output Format:** [Structured analysis report in text or JSON, with a report link when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses resting-pet video; results are health reference only and are not a medical diagnosis.]

## Skill Version(s):

1.0.10 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
