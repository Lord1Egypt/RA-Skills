## Description:

Provides a workflow for submitting night-time crib video for infant blanket coverage and kicking analysis and retrieving reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and baby-monitoring product developers can submit night-time crib video to request blanket coverage and kicking reports or retrieve earlier reports. Treat the results as auxiliary information; the skill documentation says it does not replace adult supervision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a mismatch between the advertised infant blanket monitoring and the skill's reported video analysis, identity, registration, credential handling, and remote account workflows.

Mitigation: Review and trust the remote service and its data handling before installation; only submit infant video or identity data when consent and appropriate protections are in place.

Risk: The security review says the scanners do not establish that real-time monitoring or alerts work, and its coverage is partial.

Mitigation: Treat reports as unverified supplementary information and maintain direct adult supervision.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-infant-blanket-kick-detection-analysis)

## Skill Output:

**Output Type(s):** [Analysis results, JSON, Text, Report links]

**Output Format:** [Structured JSON or text reports with coverage and event fields, alerts, and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report details depend on the remote analysis response.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
