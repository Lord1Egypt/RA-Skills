## Description:

teammate.skill helps an agent distill a colleague's approved communications and work artifacts into a reusable AI Skill with work knowledge, persona, quality checks, privacy scanning, and ongoing updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myclaw-ai](https://clawhub.ai/user/myclaw-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to capture a teammate's work practices, domain knowledge, and communication style from authorized source material, then generate and maintain a teammate-specific agent skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may collect or persist sensitive coworker communications and work artifacts.

Mitigation: Use it only with authorization and the teammate's consent, prefer approved source files, and run a privacy review before sharing generated outputs.

Risk: Slack and GitHub collection can access private or overbroad data if scopes and tokens are not constrained.

Mitigation: Avoid private-channel Slack scopes unless explicitly approved, use fine-grained read-only GitHub tokens, and secure or avoid persisted tokens.

Risk: Generated teammate skills may contain inaccurate, sensitive, or over-personalized instructions.

Mitigation: Review generated SKILL.md, work, and persona files before global installation or distribution.

Risk: Raw knowledge files and generated personas can expose personal or confidential information if shared.

Mitigation: Do not share raw knowledge directories or generated personas without a privacy review and redaction where needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/myclaw-ai/skills/teammate-skill)
- [README](artifact/README.md)
- [Installation and setup guide](artifact/INSTALL.md)
- [AgentSkills standard](https://agentskills.io)
- [Slack app setup](https://api.slack.com/apps)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON files with inline shell commands and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces teammate work and persona files, metadata, generated SKILL.md content, quality checks, smoke-test guidance, privacy-scan guidance, comparisons, and portable export packages.]

## Skill Version(s):

2.0.0 (source: server release metadata, target metadata, and changelog released 2026-03-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
