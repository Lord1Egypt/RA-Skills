## Description:

Free local speech-to-text for Telegram and WhatsApp using MLX Whisper on Apple Silicon. Private, no API costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[impkind](https://clawhub.ai/user/impkind)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to transcribe Telegram, WhatsApp, and other audio messages on Apple Silicon Macs through OpenClaw or local command-line workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio may be sent to OpenAI or Groq if cloud fallback is available, despite local-only privacy claims.

Mitigation: Disable or remove cloud backends and related API keys before use when local-only transcription is required.

Risk: The local daemon is unauthenticated and can accept filesystem paths for transcription.

Mitigation: Run the daemon only in a trusted local environment, add access controls, and prefer upload-only handling that does not process arbitrary paths.

Risk: Auto-start configuration can keep the transcription daemon running after login.

Mitigation: Audit any LaunchAgent plist before loading it and confirm the unload process before enabling persistence.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/impkind/skills/whisper-mlx-local)
- [Declared Source Repository](https://github.com/ImpKind/local-whisper)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text transcription, JSON daemon responses, and Markdown instructions with shell and JSON configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audio transcription may include optional translation to English when requested.]

## Skill Version(s):

1.5.0 (source: server release metadata and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
