## Description:

Automatically assess task complexity and adjust reasoning level before answering complex questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to classify request complexity and decide when deeper reasoning should be used. It is intended as a preprocessing guide for agent responses rather than a standalone tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can silently change reasoning behavior across messages.

Mitigation: Use it only in environments where automatic reasoning-mode changes are acceptable and make explicit user or system instructions override the skill.

Risk: The skill may alter final-answer formatting with visual indicators.

Mitigation: Avoid using it for strict output schemas, accessibility-sensitive outputs, or workflows where extra suffixes would break downstream processing.

Risk: The skill may use session-control commands without explicit approval.

Mitigation: Require review or policy controls before enabling it in environments where session state changes need user approval.

## Reference(s):

- [Adaptive Reasoning on ClawHub](https://clawhub.ai/tobeyrebecca/skills/toby-adaptive-reasoning)
- [Publisher Profile](https://clawhub.ai/user/tobeyrebecca)
- [Complete setup guide](https://skillboss.co/skill.md)

## Skill Output:

**Output Type(s):** [guidance, text, shell commands]

**Output Format:** [Markdown guidance with optional session-control commands and response suffix indicators]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append visual reasoning indicators to final answers when high complexity is detected.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
