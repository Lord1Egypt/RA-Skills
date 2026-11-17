## Description:

Multi-provider Text-to-Speech: Speechify API (primary) + Edge TTS (fallback). Gera .ogg (Opus) para voice messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rickkbarbosa](https://clawhub.ai/user/rickkbarbosa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to generate Opus .ogg speech audio from text for messaging workflows, with Speechify as the primary TTS provider and Edge TTS as fallback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input text is sent to Speechify and may be sent to Microsoft Edge TTS during fallback.

Mitigation: Avoid secrets, regulated data, and sensitive private content in TTS input unless the deployment has approved those providers.

Risk: Helper commands such as edge-tts, vault-resolver, and ffmpeg are executed from the local environment.

Mitigation: Use trusted command paths and an isolated Python environment with reviewed or pinned dependencies.

Risk: The default output path is under /tmp, which can be predictable on shared systems.

Mitigation: Configure a private output path for shared or multi-user environments.

## Reference(s):

- [Speechify API Docs](https://docs.sws.speechify.com/)
- [Speechify Audio Speech API](https://api.speechify.ai/v1/audio/speech)
- [Edge TTS](https://github.com/rany2/edge-tts)
- [SSML W3C Specification](https://www.w3.org/TR/speech-synthesis11/)
- [Voices Reference](references/voices.md)
- [Architecture Diagram](docs/diagrama.svg)
- [ClawHub Skill Page](https://clawhub.ai/rickkbarbosa/skills/speechfy)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The invoked script writes an .ogg Opus audio file and prints the output path on success.]

## Skill Version(s):

1.1.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
