## Description:

Lightweight voice bridge service that provides OpenAI-compatible STT and TTS HTTP APIs using Whisper for transcription and Edge TTS or Piper for speech synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangbb-coder](https://clawhub.ai/user/fangbb-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run a local speech service that lets OpenAI-compatible clients request text-to-speech audio and speech-to-text transcription through HTTP endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audio HTTP service can be exposed too broadly without authentication.

Mitigation: Use it only on localhost unless authentication and firewall controls are added.

Risk: Running the persistent service as root increases the impact of compromise or misuse.

Mitigation: Run the service under a dedicated unprivileged account and avoid the recommended root systemd configuration as written.

Risk: Audio uploads and repeated requests can create resource exhaustion risk.

Mitigation: Add upload size, audio duration, concurrency, and rate limits before shared or production use.

Risk: The default Edge TTS backend sends input text to Microsoft’s online TTS service.

Mitigation: Use Piper for local-only TTS when needed, or disclose and approve external TTS processing before deployment.

Risk: Unpinned dependencies can change behavior or introduce vulnerable versions over time.

Mitigation: Use pinned dependencies or a vetted lockfile for repeatable installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fangbb-coder/skills/voice-bridge-light)
- [Publisher profile](https://clawhub.ai/user/fangbb-coder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces service setup guidance and OpenAI-compatible audio API usage examples; runtime endpoints return audio files or JSON transcription responses.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
