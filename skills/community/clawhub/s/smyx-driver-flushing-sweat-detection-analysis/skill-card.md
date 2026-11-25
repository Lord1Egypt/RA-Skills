## Description:

Analyzes submitted in-cabin driver video for visual signs of facial flushing and sweating, then returns a health-awareness alert and structured report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and fleet operators use the skill to review submitted driver-facing camera video for visible flushing or sweating and provide a prompt for the driver to rest or seek help. The output is a visual alert, not a medical assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags broad account, credential, and remote-service capabilities that do not fit the advertised driver-health task, and notes a mismatch between claimed live monitoring and submitted-video analysis.

Mitigation: Before use, verify the remote service, what video and identity data it receives, and how credentials are stored and protected; confirm that submitted-video analysis fits the intended workflow.

Risk: The security scan was partial, so the available assessment is incomplete.

Mitigation: Treat the assessment as incomplete and do not rely on an empty result from another scan as evidence that the skill is safe.

Risk: Driver video contains sensitive personal and biometric information, and visual signs can be affected by lighting, camera filters, and individual differences.

Mitigation: Obtain informed consent, protect video and reports in line with applicable privacy requirements, and treat alerts as visual prompts rather than clinical findings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-driver-flushing-sweat-detection-analysis)
- [API Interface Documentation](references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured analysis report with visual metrics, an alert or recommendation, and a report link.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Visual observations only; not a medical diagnosis. Detection quality can vary with lighting, camera color, and face visibility.]

## Skill Version(s):

1.0.14 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
