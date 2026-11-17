## Description:

Generate synchronized subtitles (SRT/VTT/ASS) from video audio with precise timestamps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, video editors, and content teams use this skill to generate synchronized subtitle files from video or audio, including SRT, VTT, ASS, timing JSON, and optional burned-in captions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Videos and extracted audio may contain sensitive content and are uploaded to a third-party transcription API.

Mitigation: Use the skill only when SenseAudio is an acceptable transcription provider for the content, and avoid submitting sensitive media without appropriate approval.

Risk: The SenseAudio API key could be exposed if placed directly in prompts, source files, or logs.

Mitigation: Store SENSEAUDIO_API_KEY in an environment variable or secret manager and avoid echoing it in generated commands.

Risk: Generated subtitles may include transcription or timing errors.

Mitigation: Review subtitle text and timing before publishing or burning captions into video.

Risk: External tools and dependencies such as ffmpeg, requests, and pydub may introduce supply-chain or local execution risk.

Mitigation: Install dependencies from trusted sources and run media processing in a non-privileged environment where practical.

## Reference(s):

- [Subtitle Generator on ClawHub](https://clawhub.ai/scikkk/skills/subtitle)
- [SenseAudio Homepage](https://senseaudio.cn)
- [SenseAudio API Key Page](https://senseaudio.cn/platform/api-key)
- [SenseAudio Speech Recognition API Documentation](https://senseaudio.cn/docs/speech_recognition)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with Python and shell snippets; generated artifacts may include SRT, VTT, ASS, JSON timing data, or video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg, Python dependencies requests and pydub, and a SenseAudio API key; extracted audio is sent to SenseAudio for transcription.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
