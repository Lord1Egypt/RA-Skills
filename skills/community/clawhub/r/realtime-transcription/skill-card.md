## Description:

Real-time transcription of system or microphone audio with automatic summary generation and date-based Markdown archival after stopping or idle timeout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeleoo](https://clawhub.ai/user/leeleoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to capture local microphone or macOS system audio, monitor the transcript, and turn completed recordings into summarized Markdown archives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill records microphone or system audio and stores transcripts plus summaries locally.

Mitigation: Use only where audio recording is appropriate and consented to; avoid sensitive meetings or private media and review retained transcript archives.

Risk: The skill relies on unpinned executable dependencies and model code.

Mitigation: Run it in a dedicated virtual environment with pinned dependencies and a pinned or verified model that does not require trust_remote_code.

Risk: The skill uses broad local file and process operations to manage transcripts, archives, and the background recorder.

Mitigation: Install it in a constrained workspace and review commands before running or automating the workflow.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/leeleoo/skills/realtime-transcription)
- [Publisher profile](https://clawhub.ai/user/leeleoo)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Timestamped transcript text, Markdown archive files, and concise agent guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes live transcript text to .tmp/transcript.txt and stores summarized archives under archive/YYYY/MM/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
