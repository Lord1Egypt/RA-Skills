## Description:

Voice Clone TTS helps agents clone voiceprints from audio samples and synthesize speech with cloned or preset voices across MiniMax, ElevenLabs, Fish Audio, Azure TTS, and OpenAI TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oliviapp8](https://clawhub.ai/user/oliviapp8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and production teams use this skill to clone permitted voices, generate narration or voiceover audio, and batch-produce scene-level speech assets for downstream video or avatar workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice cloning can enable misleading or unauthorized impersonation if samples are uploaded without consent.

Mitigation: Use the skill only for voices the operator owns or has explicit permission to clone, and avoid creating deceptive content.

Risk: Audio samples and synthesized text may be sent to third-party TTS providers with different retention, privacy, and commercial-use terms.

Mitigation: Check the selected provider's retention, privacy, and commercial-use terms before uploading samples or sensitive text.

Risk: The skill does not require a consent checkpoint before cloning a speaker's voice.

Mitigation: Add a human review step that confirms speaker authorization before executing any clone workflow.

## Reference(s):

- [Backend Setup Guide](references/backend-setup.md)
- [ElevenLabs API Reference](https://docs.elevenlabs.io/api-reference)
- [Fish Audio Documentation](https://docs.fish.audio/)
- [MiniMax Platform](https://www.minimax.chat/)
- [OpenAI Platform](https://platform.openai.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce voice identifiers, audio file paths, batch audio manifests, backend configuration snippets, and provider API call examples.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
