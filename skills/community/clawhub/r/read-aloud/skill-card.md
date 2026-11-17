## Description:

Turn user-provided text into a playable MP3 with AudioFlow TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niuzb](https://clawhub.ai/user/niuzb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn approved text into playable speech without rewriting or transforming the source text. It is intended for read-aloud, narration, and speech-generation requests that can be sent to AudioFlow for remote text-to-speech processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected text is sent to AudioFlow over HTTPS for remote text-to-speech processing and may be billed by AudioFlow.

Mitigation: Require explicit per-request approval before synthesis, disclose the remote processing and character-based billing, and avoid highly sensitive text unless the user accepts that processing.

Risk: AudioFlow credentials are needed for synthesis and could enable account usage if exposed.

Mitigation: Use the AUDIOFLOW_TOKEN environment variable or the skill's private credential store, never print the full token, and review or revoke the token from the AudioFlow dashboard when needed.

Risk: Retrying an uncertain synthesis request could create duplicate charges.

Mitigation: Attempt each TTS POST once and retry only after the user explicitly requests a new attempt.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/niuzb/skills/read-aloud)
- [AudioFlow TTS service endpoint](https://asr.audioflow123.com)
- [AudioFlow dashboard](https://audioflow123.com/dashboard)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands; synthesis returns JSON metadata and a local MP3 file path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts non-empty text up to 4096 Unicode characters and optional speed from 0.5 to 2.0; generated audio is MP3.]

## Skill Version(s):

1.0.2 (source: release evidence and SKILL.md Version section)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
