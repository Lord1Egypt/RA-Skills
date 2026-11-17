## Description:

Local speech-to-text with the Whisper CLI (no API key).

This skill is ready for commercial/non-commercial use.

## Publisher:

[utromaya-code](https://clawhub.ai/user/utromaya-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to install and invoke the local Whisper CLI for transcribing or translating user-selected audio files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the Whisper CLI through Homebrew adds local software and may download model files to the user's cache.

Mitigation: Install only when the Homebrew formula and local storage behavior are acceptable for the environment.

Risk: Transcripts can contain sensitive information from user-selected audio.

Mitigation: Review audio contents before transcription and handle generated transcript files according to applicable data handling requirements.

## Reference(s):

- [OpenAI Whisper](https://openai.com/research/whisper)
- [ClawHub skill page](https://clawhub.ai/utromaya-code/skills/whisper-speech-to-text)
- [Publisher profile](https://clawhub.ai/user/utromaya-code)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance assumes the local whisper binary is installed and model files may be downloaded to the user's local cache.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
