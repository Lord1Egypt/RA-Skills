## Description:

High-performance audio library with text-to-speech (TTS) and speech-to-text (STT).

This skill is ready for commercial/non-commercial use.

## Publisher:

[darknoah](https://clawhub.ai/user/darknoah)

### License/Terms of Use:


## Use Case:

Developers and agents use Qwen Audio to generate speech, create and list reusable voice profiles, clone voices from reference audio and transcripts, and transcribe audio to text or subtitle files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can download models and uses a third-party model mirror by default.

Mitigation: Use an explicit trusted model endpoint, review downloaded model sources, and prefer pinned dependencies before deployment.

Risk: The skill may modify its Python environment on macOS by installing mlx-audio automatically.

Mitigation: Run it in an isolated environment and approve dependency changes before executing audio commands.

Risk: Voice profiles persist reference audio, transcripts, and voice style instructions.

Mitigation: Store only voice samples with clear permission, limit access to the voices directory, and remove profiles that are no longer needed.

Risk: Custom voice IDs have unsafe path-handling concerns in the security evidence.

Mitigation: Review or patch voice ID handling before using custom IDs, and restrict IDs to simple safe names.

## Reference(s):

- [Environment Check List](references/env-check-list.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; command results are JSON, WAV audio, text, ASS, or SRT files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Voice profiles may persist reference audio, transcript text, and style instructions under the skill's voices directory.]

## Skill Version(s):

0.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
