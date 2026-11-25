## Description:

Analyzes fixed-camera video from emergency shelters for visible acute stress behaviors and returns crisis alerts and response guidance for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized emergency command centers and qualified psychological rescue teams use the skill to review shelter video for observable distress behaviors, locate people who may need support, and guide responders. Alerts should be reviewed by qualified personnel and are not clinical diagnoses.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The security review flags account creation and credential handling, including unrestricted credential-bearing requests.

Mitigation: Review account and credential handling before installation or use, and ensure credentials are protected and appropriately scoped.

Risk: Shelter video sent for remote analysis may contain sensitive personal information.

Mitigation: Use only footage authorized for emergency response, and verify access, retention, and handling controls before processing.

Risk: Behavioral alerts may be mistaken for clinical conclusions or acted on without review.

Mitigation: Treat results as behavioral observations only; require qualified human review before response escalation and do not use them as diagnoses.

## Reference(s):

- [API documentation](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [Structured JSON analysis results and Markdown report summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Behavior observations, alert levels, location guidance, and response suggestions; no clinical diagnosis.]

## Skill Version(s):

1.0.19 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
