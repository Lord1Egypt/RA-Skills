## Description:

Identifies unfamiliar people in supplied surveillance images or videos by comparing detected faces with a reference database, and supports stranger alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Security and facility teams can analyze supplied images or videos, compare detected faces with an enrolled reference database, and receive structured reports or query earlier reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted images or videos may contain sensitive personal information and are processed by a remote service.

Mitigation: Submit only media you are authorized to process, and review the service's handling and retention terms first.

Risk: The security review flags account creation and persistent credential handling as possible side effects.

Mitigation: Review account behavior before use and use a dedicated account with credentials stored securely.

Risk: Facial reference enrollment may store biometric information for later comparisons.

Mitigation: Enroll faces only with appropriate authorization and consent, and set clear access and retention controls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-stranger-recognition-analysis)
- [Skill demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Text]

**Output Format:** [Structured analysis reports in JSON or text, and Markdown report listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include recognition results, alerts, recommendations, and report links; reference enrollment is supported.]

## Skill Version(s):

1.0.20 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
