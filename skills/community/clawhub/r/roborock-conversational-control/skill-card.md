## Description:

Provides conversational Roborock vacuum control for OpenClaw or Telegram, including status, start, pause, stop, dock, room-specific cleaning, and room alias bootstrapping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[serdarsalim](https://clawhub.ai/user/serdarsalim)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an OpenClaw or Telegram agent control a Roborock vacuum with short natural-language commands, room aliases, and status queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat commands can move a physical vacuum without clear confirmation safeguards.

Mitigation: Require explicit confirmation before Telegram or shared-chat users can start, dock, stop, pause, or room-clean the vacuum.

Risk: The scripts source local shell configuration that may contain device IDs, Roborock credentials, or Telegram tokens.

Mitigation: Install only on a trusted machine, keep jojo.env private, and avoid publishing local config or tokens.

Risk: Broad exec allowlisting can expose more command surface than the skill needs.

Mitigation: Allowlist only the specific Jojo wrapper path and review the scripts before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/serdarsalim/skills/roborock-conversational-control)
- [README](artifact/README.md)
- [Setup guide](artifact/SETUP.md)
- [Agent operating notes](artifact/AGENTS.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and local configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Roborock CLI authentication, JOJO_DEVICE_ID configuration, and optional ROOM_* aliases.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
