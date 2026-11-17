## Description:

Simple local speech-to-text skill using Whisper, with one-command setup, automatic model download, and support for 99+ languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lkisme](https://clawhub.ai/user/lkisme)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to install and run a local Whisper-based speech-to-text workflow that transcribes audio files into text, subtitle, and JSON outputs without using an API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer makes broad host-level changes, including automatic system package installation and replacement of the fixed stt-simple virtual environment.

Mitigation: Review install.sh before running and use a disposable or contained environment unless those host changes are acceptable.

Risk: Setup downloads unpinned dependencies and a Whisper model during installation.

Mitigation: Pin and review dependencies and model sources, or perform installation in a controlled environment before routine use.

Risk: Transcripts are persisted locally after processing.

Mitigation: Process only appropriate audio and manage files in /root/.openclaw/workspace/stt_output/ according to local retention requirements.

## Reference(s):

- [OpenAI Whisper research page](https://openai.com/research/whisper)
- [ClawHub skill page](https://clawhub.ai/lkisme/skills/stt-simple)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash commands; transcription results are plain text, JSON, SRT, or VTT files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The Python helper writes transcript text under /root/.openclaw/workspace/stt_output/ and prints a JSON success or error object.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
