## Description:

Analyzes driver-facing cabin video for head pitch and yaw, identifies sustained head-down or side-view events, and returns a structured distraction report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and fleet safety teams use it to review driver-facing cabin footage for head-down or side-view events and inspect the resulting reports. Use it as an assistive review tool, not as the basis for live driving safety decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Driver videos may be submitted to a remote service, and identity or account information may be sent and stored.

Mitigation: Obtain informed consent and confirm the service's privacy, retention, and access practices before uploading driver video.

Risk: The security review advises against relying on this skill for live driving alerts.

Mitigation: Use results for review and keep live driving safety decisions under human and vehicle-system oversight.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill usage introduction](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-driver-head-pose-abnormality-analysis)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured JSON report with a brief text heading and report link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports head pose and distraction events; results depend on usable driver-facing video.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
