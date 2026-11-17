## Description:

Creates opus/ogg WhatsApp voice notes from text with ElevenLabs or macOS say, then sends them through an OpenClaw WhatsApp channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georgecot99](https://clawhub.ai/user/georgecot99)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill when an OpenClaw agent needs to convert message text into a WhatsApp voice note, either sending it to an approved recipient or writing the generated audio for another channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can send WhatsApp voice notes to unintended recipients if recipient control is too broad.

Mitigation: Configure a recipient allowlist or confirmation rule before enabling sends, and test workflows with --dry-run or --out-only.

Risk: Message text may be sent to ElevenLabs when cloud text-to-speech is enabled.

Mitigation: Avoid ElevenLabs for sensitive message text unless that provider use is approved; use the local macOS say fallback when local synthesis is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/georgecot99/skills/whatsapp-voice-note)
- [Build Your Own Chief starter kit](https://chief.natalicot.com/kit/?utm=clawhub)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and environment variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate an opus/ogg voice note file with --out-only or send it through OpenClaw WhatsApp when a target is supplied.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
