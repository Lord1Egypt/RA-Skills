## Description:

On-device multilingual text-to-speech using Supertonic (Supertone) for local or offline speech synthesis, with optional voice cloning that requires a one-time upload to Supertone's Voice Builder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratyushchauhan](https://clawhub.ai/user/pratyushchauhan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate multilingual WAV speech locally from text, choose built-in or exported custom voices, and get guidance on Supertonic setup, language codes, expression tags, and deployment options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flagged reliance on an unrelated shared Python environment and unpinned downloaded components.

Mitigation: Install and run the skill in a dedicated virtual environment with pinned and hash-checked dependencies before using it in production.

Risk: Voice cloning requires uploading biometric voice audio to Supertone's online Voice Builder service.

Mitigation: Use built-in voices for offline or regulated environments, and use voice cloning only when third-party voice sample upload is acceptable.

## Reference(s):

- [Supertonic TTS Skill Page](https://clawhub.ai/pratyushchauhan/skills/supertonic-tts)
- [Deployment Options](references/deployment.md)
- [Expression Tags](references/expression-tags.md)
- [Supported Languages](references/languages.md)
- [Supertonic Voices](references/voices.md)
- [Supertonic GitHub Repository](https://github.com/supertone-inc/supertonic)
- [Supertonic Python SDK Documentation](https://supertone-inc.github.io/supertonic-py/)
- [Supertonic-3 Model Card](https://huggingface.co/Supertone/supertonic-3)
- [Supertonic Voice Builder](https://supertonic.supertone.ai/voice_builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include commands that synthesize 44.1 kHz 16-bit mono WAV audio through the Supertonic package.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
