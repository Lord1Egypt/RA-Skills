## Description:

SenseAudio Text-to-Speech (TTS) API for converting text to natural speech, with synchronous and SSE streaming modes, multiple voices, emotion control, speed, pitch, volume adjustment, and Chinese/English support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to integrate SenseAudio's hosted text-to-speech API, configure voice and audio parameters, and generate example curl or Python requests for synchronous or streaming speech synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for synthesis is sent to SenseAudio's hosted service.

Mitigation: Use the skill only when sending the target text to SenseAudio is acceptable for the user's data handling requirements.

Risk: Examples require SENSEAUDIO_API_KEY and show bearer-token authentication.

Mitigation: Store SENSEAUDIO_API_KEY as a secret and avoid pasting it into shared logs, prompts, or source files.

Risk: Example commands write response.json and output.mp3 in the working directory.

Mitigation: Change output filenames or run examples in an isolated directory when existing files should not be overwritten.

## Reference(s):

- [SenseAudio Text-to-Speech Documentation](https://senseaudio.cn/docs/text_to_speech_introduction)
- [ClawHub Skill Page](https://clawhub.ai/scikkk/skills/text2speech)
- [Publisher Profile](https://clawhub.ai/user/scikkk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, bash, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include example API requests that send submitted text to SenseAudio and write response.json or output.mp3 files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
