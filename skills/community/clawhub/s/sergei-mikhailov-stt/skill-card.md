## Description:

Speech recognition from voice messages using Yandex SpeechKit (with an extensible architecture for other providers). Use when you need to convert a voice message to text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bzsega](https://clawhub.ai/user/bzsega)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this OpenClaw skill to transcribe voice messages or local audio files into text through Yandex SpeechKit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice audio is sent to Yandex SpeechKit for transcription.

Mitigation: Use the skill only when sending audio to Yandex SpeechKit is acceptable for the user, data, and deployment context.

Risk: Yandex credentials are required for operation.

Mitigation: Store credentials through OpenClaw skill environment configuration and use a narrowly scoped Yandex API key.

Risk: Diagnostics or local configuration can expose operational details on shared hosts.

Mitigation: Avoid running diagnostics on shared hosts where process arguments may be logged, and do not display or log API keys.

Risk: Dependency versions are specified as minimum ranges rather than pinned releases.

Mitigation: Pin dependencies for higher-assurance deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bzsega/skills/sergei-mikhailov-stt)
- [Publisher profile](https://clawhub.ai/user/bzsega)
- [OpenClaw documentation](https://docs.openclaw.ai/)
- [OpenClaw skill configuration documentation](https://docs.openclaw.ai/tools/skills-config)
- [Yandex Cloud documentation](https://yandex.cloud/ru/docs)
- [FFmpeg downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text transcription results, Markdown guidance, and inline shell/configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful recognition returns transcribed text and may include language, provider, confidence, and processing-time metadata.]

## Skill Version(s):

1.1.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
