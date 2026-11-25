## Description:

Analyzes supplied window- or balcony-area video for possible child climbing or leaning behavior and returns a structured report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Parents, childcare operators, and home-security integrators can submit window- or balcony-area video for automated screening of possible child climbing and leaning incidents, then review the structured result or prior reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment marks this release suspicious because the monitoring claims do not match the supplied-video analysis workflow.

Mitigation: Treat it as on-demand media analysis; do not rely on it for continuous monitoring or urgent alerts, and maintain adult supervision while independently reviewing results.

Risk: The security assessment flags possible credential exposure and undisclosed transmission of private video, and notes that its analysis is partial.

Mitigation: Use non-sensitive footage until the destination, retention, and credential handling are reviewed; obtain guardian consent before submitting children's footage.

## Reference(s):

- [API interface documentation](artifact/references/api_doc.md)
- [Analysis API reference](artifact/skills/smyx_analysis/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [Structured analysis report with behavior findings, alert details, and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include detected behavior, confidence, event time, alert level, snapshot link, and report link when provided by the service.]

## Skill Version(s):

1.0.19 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
