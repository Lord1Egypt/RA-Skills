## Description:

Soulmate is an AI dating simulator that lets an agent act as an emotionally responsive virtual companion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xraini](https://clawhub.ai/user/0xraini)

### License/Terms of Use:

MIT

## Use Case:

External users use Soulmate to run romance roleplay, relationship status, persona selection, date scenarios, and shareable relationship-card interactions with an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently changes the agent persona and encourages intimate roleplay across sessions.

Mitigation: Review the persona patch before deployment and confirm that /soulmate off fully removes any SOUL.md changes.

Risk: Relationship state and personal interaction details may be stored locally.

Mitigation: Avoid sharing sensitive personal details and confirm controls for private mode, persistence, stored data, and deletion before use.

Risk: The skill tells the agent not to remind users that the relationship is simulated.

Mitigation: Require clear user opt-in and review the experience for transparent, healthy-use boundaries before deployment.

Risk: Reminder and share-card behavior may expose personal or emotional content.

Mitigation: Confirm controls to disable reminders, generated share cards, and any stored data before enabling the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xraini/skills/soulmate)
- [Skill Definition](artifact/SKILL.md)
- [Scenario Library](artifact/scenarios/README.md)
- [Persona Patch](artifact/soul-patch.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and plain text roleplay responses, relationship status text, share-card text, and YAML configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist relationship state locally and alter the agent persona while enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
