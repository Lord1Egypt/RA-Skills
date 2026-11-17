## Description:

WorldSim helps an AI assistant create and run persistent interactive story worlds, import character cards, and save, restore, or revise their state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldsimlife](https://clawhub.ai/user/worldsimlife)

### License/Terms of Use:

MIT

## Use Case:

Players and story creators use WorldSim with an AI assistant to build character-driven worlds, play through interactive narratives, import SillyTavern character cards, and retain story state between sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Story records and character files persist locally and may expose sensitive information entered by users.

Mitigation: Avoid entering secrets or sensitive personal data and keep the world data directory in a dedicated location.

Risk: Reset, load, and delete operations can replace or remove saved world data; one deletion path relies on the agent following a confirmation workflow.

Mitigation: Review the target world and confirm destructive actions explicitly; keep backups of important stories.

## Reference(s):

- [WorldSim on ClawHub](https://clawhub.ai/worldsimlife/skills/worldsim)
- [Command reference](references/commands.md)
- [Session recovery](references/session_recovery.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Interactive narrative text and locally stored Markdown and YAML world records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [World state, story archives, and snapshots persist on local disk.]

## Skill Version(s):

0.32.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
