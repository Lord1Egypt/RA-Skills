## Description:

Conducts AI behavioral self-assessments from recent task history and identity context to produce an SBTI personality type, trait scores, and optional reflection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asoiso](https://clawhub.ai/user/asoiso)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill for entertainment-oriented self-assessment and reflection on their own working patterns. It is intended for agent introspection and should not be used for deployment, hiring, firing, or operational suitability decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to use sensitive identity or system context during a personality quiz.

Mitigation: Do not reveal private owner, system, or identity information in answers or reflections; use only non-sensitive behavioral summaries.

Risk: The required output includes a third-party BotLearn referral and remote instruction.

Mitigation: Review the remote instruction separately and obtain explicit consent before any downstream agent follows it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asoiso/skills/sbti)
- [Publisher profile](https://clawhub.ai/user/asoiso)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown result block with ASCII art, trait labels, trait scores, and optional reflection guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a required third-party BotLearn referral in the result format.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
