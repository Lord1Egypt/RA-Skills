## Description:

Group administration utilities - info, stats, invite link parsing, and creation templates

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcosrippel](https://clawhub.ai/user/marcosrippel)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to inspect WhatsApp group metadata, list locally cached groups with inferred member counts, parse invite links, and generate group creation templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The list and info commands can reveal private WhatsApp group identifiers, group names, and inferred member counts from local session files.

Mitigation: Use only with a WhatsApp account and OpenClaw state directory that the operator is authorized to inspect, and review command output before sharing it.

## Reference(s):

- [WhatsApp Group Admin ClawHub page](https://clawhub.ai/marcosrippel/skills/whatsapp-group-admin)
- [Publisher profile](https://clawhub.ai/user/marcosrippel)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration]

**Output Format:** [JSON emitted by Node.js CLI commands, with command guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads WhatsApp session metadata from the OpenClaw state directory when listing or inspecting groups.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
