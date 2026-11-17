## Description:

Audio Transcribe uses local Whisper to convert audio files into plain text, SRT subtitles, or JSON transcripts for meetings, podcasts, voice notes, and similar recordings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-tesing](https://clawhub.ai/user/ai-tesing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and end users use this skill to transcribe local audio files into readable text, subtitle files, or structured JSON. It is suited to meeting notes, podcast transcripts, voice memos, and other audio-to-text workflows where local processing is preferred.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or upgrade openai-whisper and download Whisper models even though its documentation frames processing as offline.

Mitigation: Preinstall pinned dependencies and required models in a controlled environment before using the skill.

Risk: The skill reads the supplied audio file and writes transcript files next to that audio.

Mitigation: Run it only on audio files approved for local processing and in directories where transcript output is expected.

Risk: The server security verdict is suspicious and calls for review before use.

Mitigation: Review the script and scan the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-tesing/skills/wav-audio-transcribe)
- [Publisher profile](https://clawhub.ai/user/ai-tesing)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Transcript files and console output in TXT, SRT, or JSON formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes transcript files next to the provided audio file using an _transcript suffix.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
