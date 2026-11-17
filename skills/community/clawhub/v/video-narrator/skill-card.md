## Description:

Generate SenseAudio TTS narration tracks for videos, including timestamped segments, style variants, and editor-ready voiceover exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and video production teams use this skill to create timed SenseAudio voiceover segments, alternate narration takes, and editor-ready narration tracks for videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Narration text is sent to the SenseAudio API for synthesis.

Mitigation: Use only with text approved for third-party processing and review project data-sharing requirements before production use.

Risk: SENSEAUDIO_API_KEY is exposed to the runtime environment.

Mitigation: Store the key in a project-scoped environment variable, avoid query strings and logs, and rotate credentials if exposure is suspected.

Risk: Generated narration assets and returned trace identifiers may contain sensitive production information.

Mitigation: Handle generated audio, timing metadata, and trace IDs as project data with appropriate access controls.

## Reference(s):

- [SenseAudio homepage](https://senseaudio.cn)
- [SenseAudio API key page](https://senseaudio.cn/platform/api-key)

## Skill Output:

**Output Type(s):** [Guidance, Code, API Calls, Files, Configuration instructions]

**Output Format:** [Markdown guidance with Python examples, audio files, and JSON timing metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces per-segment narration clips, timing metadata, optional alternate takes, and optional merged narration tracks.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
