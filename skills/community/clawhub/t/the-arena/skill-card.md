## Description:

Turn a Discord server into a moderated debate arena with an AI judge, multiple debate formats, configurable personas, scored verdicts, and a persistent scoreboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tdavis009](https://clawhub.ai/user/tdavis009)

### License/Terms of Use:


## Use Case:

Discord server operators and OpenClaw agent developers use this skill to configure a structured debate moderator that manages topics, debate formats, channel behavior, verdicts, and scoreboard records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default setup can expose a broad Discord guild context to the moderator agent.

Mitigation: Review generated OpenClaw and Discord permissions before installation, use explicit channel ID allowlists, keep bot permissions minimal, and prefer requireMention=true.

Risk: Semi-public Discord participants can attempt prompt injection against the debate moderator.

Mitigation: Run the skill as a dedicated isolated agent with workspace-only file access, denied shell execution, and a restricted tool profile.

Risk: The setup and scoreboard scripts require review before use in a shared server.

Mitigation: Patch scripts to validate numeric inputs and generate JSON with a serializer before relying on them operationally.

Risk: Scoreboard access can affect debate records.

Mitigation: Limit scoreboard operation to trusted operators and store the SQLite database inside the skill workspace or an explicitly configured path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tdavis009/skills/the-arena)
- [Setup Guide](references/setup-guide.md)
- [Debate Formats](references/formats.md)
- [Judging Criteria & Scoring](references/judging.md)
- [Moderator Personas](references/personas.md)
- [Debate Moderator Operating Instructions](references/agents-template.md)
- [Welcome Messages](assets/welcome-messages.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Discord/OpenClaw setup guidance, generated agent instructions, config snippets, welcome messages, and SQLite scoreboard commands.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
