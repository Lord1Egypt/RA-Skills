## Description:

XiaoDu Bedtime Soother Official coordinates child bedtime routines through the installed xiaodu-control-official skill, using scene-first XiaoDu smart-screen and IoT actions for requests such as bedtime mode, bedtime stories, white noise, or room preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dueros-mcp](https://clawhub.ai/user/dueros-mcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to let an agent coordinate XiaoDu bedtime routines for children, including safe scene selection, conservative bedroom-device adjustment, smart-screen announcements, bedtime content, and timed story shutdown. It is intended for homes where xiaodu-control-official and the XiaoDu smart-screen and IoT MCP servers are already configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control XiaoDu smart screens and relevant IoT devices during bedtime routines.

Mitigation: Confirm the target room or device before ambiguous multi-step home-control actions, avoid defaulting to whole-home control, and report only actions that actually succeeded.

Risk: The skill may save household or child bedtime preferences.

Mitigation: Require explicit consent before saving preferences and define retention or deletion expectations for household and child-related data.

Risk: A bedtime story or media session could continue longer than expected if delayed shutdown is unavailable or fails.

Mitigation: Set a reasonable maximum delay, prefer the provided timed stop and screen-off step, and tell the user when automatic shutdown could not be scheduled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dueros-mcp/skills/xiaodu-bedtime-soother-official)
- [Publisher profile](https://clawhub.ai/user/dueros-mcp)
- [Usage notes](references/usage-notes.md)
- [Test cases](references/test-cases.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and concise user-facing response text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are intended to run serially; outputs may include preference updates and delayed stop or screen-off actions.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
