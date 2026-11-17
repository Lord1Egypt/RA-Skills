## Description:

Ultra-fast text-to-speech and speech-to-text via Smallest AI's Lightning v3.1 and Pulse models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhishekmishragithub](https://clawhub.ai/user/abhishekmishragithub)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate speech from text, transcribe audio files, choose voices, and support multilingual voice workflows through Smallest AI services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text, audio files, and related metadata are sent to a third-party Smallest AI API for processing.

Mitigation: Avoid sending secrets, regulated data, private recordings, or other sensitive content unless the user has reviewed the provider's privacy and retention terms.

Risk: Voice generation and voice cloning workflows can involve other people's voices.

Mitigation: Use voice cloning or identifiable voice data only with authorization from the voice owner and within applicable policy and legal requirements.

Risk: The Python path can depend on optional packages such as requests or the Smallest AI SDK.

Mitigation: Prefer the shell/curl scripts for minimal dependencies, or use pinned Python package versions in an isolated environment.

## Reference(s):

- [Smallest AI API Quick Reference](references/api-reference.md)
- [Supported Languages](references/languages.md)
- [Available Voices](references/voices.md)
- [Smallest AI API Docs](https://waves-docs.smallest.ai)
- [Smallest AI Waves Console](https://waves.smallest.ai)
- [Smallest AI Python SDK](https://github.com/smallest-inc/smallest-python-sdk)
- [ClawHub Skill Page](https://clawhub.ai/abhishekmishragithub/skills/smallest-ai)
- [ClawHub Publisher Profile](https://clawhub.ai/user/abhishekmishragithub)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, JSON transcription output, and generated audio file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [TTS scripts print MEDIA file paths for generated WAV audio; STT scripts return JSON, text, or summary output.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
