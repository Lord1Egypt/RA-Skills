## Description:

TTS WhatsApp helps agents generate Piper text-to-speech audio in 40+ languages, convert it to WhatsApp-compatible OGG/Opus, and send it to individual or group WhatsApp targets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create and deliver text-to-speech voice messages over WhatsApp, including personal messages and group broadcasts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger outbound WhatsApp voice-message delivery to individuals or groups.

Mitigation: Verify the final recipient or group ID before every send and avoid default targets for sensitive content.

Risk: The skill requires command execution and outbound messaging authority that the manifest understates.

Mitigation: Install only in environments where command execution and WhatsApp sending are acceptable, and correct capability disclosure before low-friction installation.

Risk: Automatic cleanup can remove generated files that may be needed for accountability.

Mitigation: Keep generated files when an audit trail is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/tts-whatsapp-paid)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash, JSON, and text examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for generating TTS audio, converting it to WhatsApp-compatible OGG/Opus, and sending or withholding delivery with command options.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
