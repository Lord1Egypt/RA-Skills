## Description:

Converts an agent's Telegram text replies into Chinese voice messages when voice mode is enabled.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yl11023](https://clawhub.ai/user/yl11023)

### License/Terms of Use:

MIT-0

## Use Case:

Agents operating in Telegram use this skill to add optional spoken replies after normal text responses. It is intended for users who want a toggleable voice mode backed by edge-tts and Telegram voice-message delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact hard-codes a Telegram bot token and recipient.

Mitigation: Remove embedded credentials, rotate the exposed token, and require per-chat configuration before use.

Risk: Enabled replies may be converted to audio and sent automatically to a fixed Telegram chat.

Mitigation: Require explicit user confirmation for each configured chat and make voice mode opt-in.

Risk: TTS text is passed into command execution for audio generation.

Mitigation: Avoid shell-string interpolation for user-visible text and keep dependencies pinned in a controlled environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yl11023/skills/voice-mode)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline PowerShell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger audio/mpeg Telegram voice messages after text replies when voice mode is enabled.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
