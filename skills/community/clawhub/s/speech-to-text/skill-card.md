## Description:

Transcribe and translate audio or video-derived audio with Whisper models through the inference.sh CLI, including optional timestamps for transcripts and subtitles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

Developers and content teams use this skill to run Whisper transcription or translation workflows for meetings, podcasts, subtitles, voice notes, interviews, and accessibility content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path executes a remote installer for the inference.sh CLI.

Mitigation: Use the manual checksum-verified CLI install path, inspect the installer before running it, and complete login only after verification.

Risk: Audio or video content may be processed by hosted inference.sh services.

Mitigation: Use the skill only with media that is appropriate for hosted processing under the user's data handling requirements.

Risk: Optional related-skill commands use mutable npx installs.

Mitigation: Avoid those commands unless the additional skills are intentionally needed and separately reviewed.

## Reference(s):

- [Skill listing](https://clawhub.ai/okaris/skills/speech-to-text)
- [inference.sh](https://inference.sh)
- [Running Apps](https://inference.sh/docs/apps/running)
- [Audio Transcription Example](https://inference.sh/docs/examples/audio-transcription)
- [Apps Overview](https://inference.sh/docs/apps/overview)
- [CLI checksums](https://dist.inference.sh/cli/checksums.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, json]

**Output Format:** [Markdown guidance with shell commands and JSON input/output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced inference.sh apps return JSON containing transcription text, optional timestamped segments, and detected language.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
