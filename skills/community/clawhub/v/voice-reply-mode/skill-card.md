## Description:

Add same-modality conversation behavior to an agent: voice in -> voice out, text in -> text out, with Edge TTS helpers and gateway snippets for inbound-only TTS auto replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nasplycc](https://clawhub.ai/user/nasplycc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure same-modality replies so text inputs receive text responses and voice inputs receive voice responses. It is intended for Telegram, Feishu, or similar channels where gateway TTS routing and media permissions are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic voice replies require the intended channel and gateway to support inbound audio, outbound audio, and TTS routing.

Mitigation: Review gateway messages.tts changes, confirm channel media permissions, and validate with one text message and one voice message before rollout.

Risk: The helper script defaults to a shared /tmp output path, which can overwrite prior output or expose audio on shared hosts.

Mitigation: Pass a unique private output path when running scripts/edge-tts.sh or change the default path before deployment.

## Reference(s):

- [Workspace snippets](references/workspace-snippets.md)
- [Gateway config](references/gateway-config.md)
- [Channel notes](references/channel-notes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with configuration snippets and an optional shell helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace behavior snippets, gateway configuration guidance, validation steps, and Edge TTS shell command usage.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
