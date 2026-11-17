## Description:

Shiyi Proactive Agent monitors context, suggests actions, and proposes tasks for proactive agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[552134926-alt](https://clawhub.ai/user/552134926-alt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to add proactive context analysis, reminders, and task proposals to an agent workflow. It is aimed at trading, content publishing, task management, and learning routines where suggestions should remain advisory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads shared workspace memory, recent interaction history, planning files, and content metadata.

Mitigation: Install it only in workspaces where that local context is appropriate for review by the agent.

Risk: The monitor can run repeated background checks when daemon or heartbeat integration is enabled.

Mitigation: Enable daemon or heartbeat use only when repeated proactive checks are intended, and configure interval and cooldown settings before use.

Risk: Trading and content suggestions may be incorrect or unsuitable for the user's situation.

Mitigation: Treat generated trading and content recommendations as advisory and require human confirmation before trades, publishing, or external API actions.

Risk: The skill writes proactive task and monitor log files under memory by default.

Mitigation: Review generated task and log files and run the skill in a workspace where those writes are acceptable.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/552134926-alt/skills/shiyi-proactive-agent)
- [Publisher profile](https://clawhub.ai/user/552134926-alt)
- [Skill definition](artifact/SKILL.md)
- [Proactive configuration](artifact/config/proactive_config.yaml)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance, files]

**Output Format:** [Plain text or JSON command output, with optional JSON task and log files under memory.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Suggestions and proposed tasks are prioritized as high, medium, or low.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
