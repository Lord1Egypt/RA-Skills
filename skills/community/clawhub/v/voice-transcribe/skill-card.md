## Description:

Transcribe audio files using OpenAI's gpt-4o-mini-transcribe model with vocabulary hints and text replacements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darinkishore](https://clawhub.ai/user/darinkishore)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to transcribe voice memos and other audio files, then respond based on the transcribed content. The skill supports vocabulary hints and deterministic text replacements for names, jargon, and recurring transcription errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes potentially private audio through OpenAI transcription.

Mitigation: Use it only for audio the user is allowed to send to OpenAI, and avoid confidential or regulated recordings unless approved.

Risk: The artifact references a user-specific local transcription script that is not included in the reviewed package.

Mitigation: Verify the referenced local script before installation or execution.

## Reference(s):

- [Voice Transcribe on ClawHub](https://clawhub.ai/darinkishore/skills/voice-transcribe)
- [uv Documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text transcription with Markdown setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses custom vocabulary hints, post-processing replacements, English transcription assumptions, and SHA-256 audio-file caching.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
