## Description:

Converts user-provided text into MP3 speech audio through a disclosed remote TTS service with selectable voices, speed, pitch, and style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinsuso](https://clawhub.ai/user/yinsuso)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill when a user asks to hear text aloud or receive generated speech as an audio file. It is suited for converting single or batched text inputs into downloadable speech output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for conversion is sent to tts.wangwangit.com, which may expose sensitive or regulated content to an external provider.

Mitigation: Do not use the skill for secrets, credentials, regulated data, or confidential documents unless that provider has been approved.

Risk: Using a fixed temporary output path such as /tmp/tts_output.mp3 can overwrite existing files or expose generated audio to later processes.

Mitigation: Use a unique private temporary output file for each generation and clean it up after delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinsuso/skills/tts-wangwang)
- [Disclosed remote TTS API endpoint](https://tts.wangwangit.com/v1/audio/speech)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, audio files, guidance]

**Output Format:** [Markdown with JSON, bash, and Python examples; generated MP3 audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes text to a remote TTS endpoint; documented examples write audio output to /tmp.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
