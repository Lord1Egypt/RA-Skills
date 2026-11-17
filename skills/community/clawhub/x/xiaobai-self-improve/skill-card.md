## Description:

Self-improvement guidance for an AI agent that records mistakes, turns lessons into rules, and checks those rules before future work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aptratcn](https://clawhub.ai/user/aptratcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators can use this skill to prompt an AI agent to keep cross-session records of mistakes, learned rules, and self-audit checks intended to reduce repeated errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages persistent mistake logs and learned rules that may retain sensitive task details across sessions.

Mitigation: Review generated memory files regularly and avoid storing secrets, personal data, or sensitive operational details.

Risk: User corrections may become permanent operating rules without clear consent or deletion controls.

Mitigation: Require explicit approval before adding a correction as a permanent rule, and provide a review path for editing or removing learned rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aptratcn/skills/xiaobai-self-improve)
- [Publisher profile](https://clawhub.ai/user/aptratcn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON and shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask the agent to create or update persistent memory files such as memory/mistakes.json and WORK_RULES.md.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
