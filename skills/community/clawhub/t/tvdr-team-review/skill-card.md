## Description:

Guides a Chinese-speaking agent team through hourly reviews that record errors, lessons learned, task progress, feedback, and concrete improvements into reusable skills and knowledge-base notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[admirobot](https://clawhub.ai/user/admirobot)

### License/Terms of Use:

MIT-0

## Use Case:

Team leads, PM agents, and operations agents use this skill to run recurring Chinese-language team retrospectives, capture task and decision status, and turn repeated mistakes into reusable rules, skill files, and memory records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring reviews, reminders, backups, and session restarts may run without clear user awareness or consent.

Mitigation: Require explicit opt-in, visible scheduling controls, and an easy way to list, expire, pause, or disable recurring jobs before use.

Risk: The skill asks agents to write persistent memory and shared knowledge, which can expose secrets or sensitive personal and business data.

Mitigation: Define which agents and memory stores may be accessed, apply redaction rules, and review stored notes before sharing or reuse.

Risk: Generated improvement rules can become active skills and influence future work even if they are inaccurate or overly broad.

Mitigation: Require human review and security scanning before promoted rules become active skills or team-wide requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/admirobot/skills/tvdr-team-review)
- [Publisher profile](https://clawhub.ai/user/admirobot)
- [MAST Multi-Agent Failure Analysis](https://arxiv.org/abs/2503.13657)
- [团队每小时复盘机制](artifact/SKILL.md)
- [系统性改进框架](artifact/systemic-improvement-framework.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration, Shell commands]

**Output Format:** [Chinese-language Markdown guidance with templates, checklists, and occasional inline configuration or command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces recurring review notes, task records, decision reminders, memory logs, Obsidian knowledge-base entries, and proposed reusable skill rules.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
