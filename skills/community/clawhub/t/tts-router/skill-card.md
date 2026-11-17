## Description:

Local TTS router for Apple Silicon that helps agents pull models, serve OpenAI-compatible speech APIs, synthesize speech, and clone voices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hrhrng](https://clawhub.ai/user/hrhrng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill on macOS Apple Silicon systems to install and operate a local text-to-speech router, start a compatible API server, generate speech files, and configure OpenClaw TTS integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice cloning can be used on online or uploaded speaker audio without built-in consent safeguards.

Mitigation: Clone voices only when the speaker has clearly authorized that use, and avoid generating impersonation or misleading speech.

Risk: The install examples use executable package flows without pinned versions.

Mitigation: Review the package before use and pin known-good versions in isolated environments.

Risk: Reference audio can be fetched from arbitrary online media URLs.

Mitigation: Use trusted URLs only and avoid processing unknown or unauthorized media sources.

## Reference(s):

- [OpenClaw Integration](references/openclaw.md)
- [Voice Cloning Advanced Guide](references/voice-cloning.md)
- [OpenClaw TTS configuration reference](https://docs.openclaw.ai/gateway/configuration-reference#tts-text-to-speech)
- [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell, JSON, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local service commands, API request examples, OpenClaw configuration snippets, and generated audio file paths.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
