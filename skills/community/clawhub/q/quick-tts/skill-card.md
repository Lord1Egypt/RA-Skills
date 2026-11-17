## Description:

Quick TTS helps an agent synthesize user-provided text into an MP3 file through SenseAudio, with natural-language voice selection and pacing breaks for longer text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to convert text into speech without manually configuring SenseAudio API calls or voice IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends provided text to SenseAudio and stores response metadata and generated audio locally.

Mitigation: Use it only when that data flow is acceptable, avoid confidential text, and remove local response or audio files according to the user's retention needs.

Risk: The provided shell command can mishandle user text in a way that may execute unintended local commands.

Mitigation: Review commands before execution and build JSON request bodies with jq or another safe encoder.

Risk: The skill requires a SenseAudio API key.

Mitigation: Provide the key through SENSEAUDIO_API_KEY, keep it out of shared logs and files, and rotate it if exposure is suspected.

## Reference(s):

- [Quick TTS ClawHub Page](https://clawhub.ai/scikkk/skills/quick-tts)
- [SenseAudio Homepage](https://senseaudio.cn)
- [SenseAudio API Key Page](https://senseaudio.cn/platform/api-key)
- [SenseAudio TTS API Endpoint](https://api.senseaudio.cn/v1/t2a_v2)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown status text with shell command guidance and generated MP3 file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY; sends provided text to SenseAudio and stores response metadata and audio locally.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
