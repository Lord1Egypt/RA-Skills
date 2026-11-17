## Description:

Build, adapt, or run a speech-translation workflow that transcribes spoken audio, translates the transcript with the current agent model by default, and synthesizes translated speech with Piper, OpenClaw tts, or a mock backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[decin](https://clawhub.ai/user/decin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to process voice messages or local audio files into transcript text, translated text, generated audio, and metadata. It supports chat-native voice translation and deterministic local pipeline runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional transcript, translation, and audio notifier hooks can execute arbitrary shell commands and receive spoken-content outputs.

Mitigation: Leave command hooks disabled unless the exact command was written and reviewed for the deployment environment.

Risk: Audio transcripts and translations may contain sensitive spoken content.

Mitigation: Use trusted audio inputs, trusted output paths, and local LLM/Piper paths for private content.

Risk: External HTTP translation services can expose content or return unreviewed translations.

Mitigation: Avoid unaudited translation services; use a trusted provider only when unattended service translation is required.

Risk: Runtime dependencies and speech models affect local execution behavior.

Mitigation: Install dependencies in an isolated pinned environment and review models and binaries before use.

## Reference(s):

- [Runtime Notes](references/runtime-notes.md)
- [LLM Translation Pattern](references/llm-translation-pattern.md)
- [OpenClaw Chat Mode](references/openclaw-chat-mode.md)
- [ClawHub skill page](https://clawhub.ai/decin/skills/speech-translation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with bash and Python commands, plus local text, wav, and JSON artifacts when the pipeline runs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local pipeline output contract is 01_transcript.txt, 02_translation.txt, 03_translation.wav, and result.json; chat mode returns transcript, translation, then translated audio.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
