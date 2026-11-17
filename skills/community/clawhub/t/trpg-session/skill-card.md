## Description:

Set up and run tabletop RPG campaigns with OpenClaw agents for dungeon mastering, player-character roleplay, rule references, session memory, and group play through Discord or Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gejiliang](https://clawhub.ai/user/gejiliang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure and run tabletop RPG campaigns with DM and PC agents, campaign workspaces, character files, rule references, session logs, and channel-based play.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Campaign notes, character files, and session logs may contain private or sensitive roleplay details that persist on disk.

Mitigation: Decide where logs and campaign files are stored before use, and avoid putting real personal or confidential information into shared campaign directories.

Risk: The skill describes private character secrets while also placing multiple agents in the same campaign workspace.

Mitigation: Use separate workspaces or filesystem permissions for DM-only notes and per-character files before relying on isolation.

Risk: AI player characters and DM notes can affect group play and reveal or preserve unintended information.

Mitigation: Review the skill before installing, define which agents can access each file, and test the campaign setup with non-sensitive content first.

## Reference(s):

- [TRPG Session ClawHub Page](https://clawhub.ai/gejiliang/skills/trpg-session)
- [DM Agent Behavior Guide](references/dm-guide.md)
- [Session Log Template](references/session-template.md)
- [Rule System Presets](references/systems.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent setup guidance, workspace layouts, character templates, reference files, and session-management instructions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
