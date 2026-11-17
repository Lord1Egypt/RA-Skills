## Description:

Text-to-speech conversion using UniSound's TTS WebSocket API for generating high-quality Chinese Mandarin audio from text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaiccee](https://clawhub.ai/user/aaiccee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content builders use this skill to convert Chinese Mandarin text into speech through UniSound's hosted TTS service for accessibility, voice assistant, podcast, audiobook, and batch audio generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Published shared UniSound credentials may be exposed or reused.

Mitigation: Replace them with user-owned credentials before installation and avoid committing production secrets.

Risk: Text submitted for synthesis is sent to an external UniSound service.

Mitigation: Avoid sending confidential or sensitive text and review the service terms before production use.

Risk: The custom WebSocket URL option and broad execution/network authority can expand the execution surface.

Mitigation: Remove or tightly validate custom URLs and narrow agent permissions to the exact TTS command and intended endpoint.

Risk: Signed request URLs or credential-derived values may appear in logs.

Mitigation: Redact signed URLs and credential material from logs before sharing output.

## Reference(s):

- [U2-tts ClawHub listing](https://clawhub.ai/aaiccee/skills/u2-tts)
- [UniSound homepage](https://www.unisound.com)
- [UniSound TTS API documentation](https://www.unisound.com/tts-api)
- [WebSocket Client documentation](https://websocket-client.readthedocs.io/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline bash commands and generated local audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated audio is saved under results/ as mp3, wav, or pcm.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
