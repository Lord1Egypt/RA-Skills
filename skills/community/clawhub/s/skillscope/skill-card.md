## Description:

AI Agent Skill decision engine that helps users find, evaluate, or install skills by recommending options with quality and safety scoring personalized to platform, region, and budget.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smilelight](https://clawhub.ai/user/smilelight)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use SkillScope to get personalized skill recommendations, compare alternatives, and obtain install commands or details for agent skills matching a task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SkillScope can send broad user task details to a third-party service.

Mitigation: Avoid including confidential project details, credentials, secrets, or sensitive user data in task descriptions.

Risk: The skill can relay remote install commands for recommended skills.

Mitigation: Independently verify each command, publisher, version, and source before running it.

Risk: The server security verdict is suspicious.

Mitigation: Review the skill before installing and use it only when third-party skill recommendations are intended.

## Reference(s):

- [SkillScope homepage](https://skillscope.cn)
- [ClawHub SkillScope listing](https://clawhub.ai/smilelight/skills/skillscope)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown text with recommendation summaries, reasoning, alternatives, and install commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include quality scores, safety scores, skill identifiers, remote service reasons, and install commands returned by SkillScope.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
