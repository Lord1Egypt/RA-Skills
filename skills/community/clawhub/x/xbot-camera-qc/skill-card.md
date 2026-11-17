## Description:

Professional visual inspection for xbot.coffee Lite, detecting drink volume, screen, table, robotic arm, dirt, environment and pests, and outputting structured English JSON for API automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mszren](https://clawhub.ai/user/mszren)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and developers use this skill to classify xbot.coffee Lite camera images for automated quality control, anomaly alerting, API integration, reporting, and operations workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The returned JSON may not match a backend parser or alerting workflow if the expected schema differs.

Mitigation: Confirm the fixed output fields and allowed values before integrating the skill into production automation.

Risk: Camera images may contain operational or sensitive visual information.

Mitigation: Only provide images that are appropriate for analysis in the configured OpenClaw environment.

## Reference(s):

- [Project homepage](https://github.com/yourname/xbot-camera-qc-pro)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Structured English JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns fixed camera quality-check fields, a boolean anomaly indicator, and an alert message.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
