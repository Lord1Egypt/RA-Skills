## Description:

Recommends SenseAudio voice options for scenarios or emotions and can optionally generate preview audio samples when configured with an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to choose SenseAudio voice IDs for narration, commerce, podcast, education, advertising, and emotion-specific voice scenarios. They can also request optional preview audio when they have a SenseAudio API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional preview generation sends preview text and an API key to SenseAudio.

Mitigation: Use recommendation-only mode for sensitive text, and generate previews only after explicit user confirmation with non-sensitive preview text.

Risk: The optional preview shell command uses unsafe JSON construction that can execute commands from preview text.

Mitigation: Review or rewrite the preview command with safe JSON construction before using arbitrary preview text.

## Reference(s):

- [ClawHub Voice Picker release page](https://clawhub.ai/scikkk/skills/voice-picker)
- [SenseAudio homepage](https://senseaudio.cn)
- [SenseAudio API key page](https://senseaudio.cn/platform/api-key)
- [SenseAudio TTS API endpoint](https://api.senseaudio.cn/v1/t2a_v2)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, files]

**Output Format:** [Markdown recommendations with optional bash commands and MP3 preview files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendation-only use requires no API key; preview generation requires SENSEAUDIO_API_KEY plus curl, jq, and xxd.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
