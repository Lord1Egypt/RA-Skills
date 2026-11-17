## Description:

Telethon Master helps an agent operate a Telegram account through Telethon MCP tools for messaging, chat history, media handling, channel management, and voice note generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[producedbysavant](https://clawhub.ai/user/producedbysavant)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent interact with Telegram through a Telethon bridge, including sending messages, reading and searching chats, forwarding or deleting messages, managing channels, downloading media, and generating ElevenLabs voice notes. It is best suited for authorized account workflows where broad Telegram access is acceptable and scoped by allowlists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose broad Telegram account access, including private chats and account-changing actions.

Mitigation: Use a dedicated Telegram account where possible, restrict allowed chat IDs, and verify that read and write allowlists are enforced before deployment.

Risk: Destructive or state-changing operations such as deletes, joins, forwards, media downloads, channel changes, and marking messages read can affect real conversations.

Mitigation: Require explicit user confirmation before executing destructive or account-changing Telegram operations.

Risk: Private message content, downloaded media, session credentials, and ElevenLabs TTS inputs may contain sensitive data.

Mitigation: Do not print environment files or session secrets, avoid logging message contents, and do not send private or sensitive text to ElevenLabs unless the account owner authorizes it.

## Reference(s):

- [Telethon Master on ClawHub](https://clawhub.ai/producedbysavant/skills/telethon-master)
- [ElevenLabs Voices API](https://api.elevenlabs.io/v1/voices)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with tool names, JSON snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Telegram MCP tool calls, configuration values, operational commands, and safety guidance for account-scoped workflows.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
