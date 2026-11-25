## Description:

Analyzes aquarium fish videos to flag abnormal swimming posture and report the share of observation time affected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Aquarists and aquarium operators use the skill to review fixed-camera fish videos for abnormal swimming posture and receive a structured monitoring report. It supports early observation and is not a veterinary diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags account, identity, and external-processing behavior, and says the available analysis is incomplete.

Mitigation: Review the publisher and data handling before installation, and use only authorized fish video and account data.

Risk: The security assessment notes that an option intended to avoid analysis may still trigger it.

Mitigation: Confirm the option's behavior before relying on it to prevent video analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-fish-abnormal-swimming-detection-analysis)
- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Structured analysis results with a Markdown summary and report link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports observed posture events and abnormal-duration proportion; not a veterinary diagnosis.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
