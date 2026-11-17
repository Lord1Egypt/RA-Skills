## Description:

Local speech-to-text with the Whisper CLI (no API key).

This skill is ready for commercial/non-commercial use.

## Publisher:

[utromaya-code](https://clawhub.ai/user/utromaya-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users use this skill to transcribe and translate local audio files with the Whisper CLI without using an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing the Homebrew `openai-whisper` package and downloading Whisper models locally.

Mitigation: Install the package only from a trusted Homebrew source and account for local model storage before use.

Risk: Audio files may contain sensitive information.

Mitigation: Run transcription only on files you intend to process locally and apply your organization's handling rules for sensitive audio.

## Reference(s):

- [OpenAI Whisper](https://openai.com/research/whisper)
- [ClawHub skill page](https://clawhub.ai/utromaya-code/skills/whisper-local-stt)
- [Publisher profile](https://clawhub.ai/user/utromaya-code)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance assumes the local `whisper` binary is installed and available on PATH.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
