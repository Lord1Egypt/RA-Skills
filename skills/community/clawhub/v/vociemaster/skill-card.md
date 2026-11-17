## Description:

专业级 AI 短视频配音助手，支持多角色音色映射、自动语速调节及 BGM 建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaocaijic](https://clawhub.ai/user/xiaocaijic)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and developers use this skill to turn short-video scripts or draft ideas into structured dialogue, SenseAudio TTS requests, local MP3 outputs, and background-music direction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper writes detailed plaintext .debug.json files beside generated audio, including user text and API responses.

Mitigation: Avoid confidential scripts or personal data, delete debug logs after use, or modify the helper/debug-log option before processing sensitive material.

Risk: Script text is sent to the external SenseAudio text-to-speech service.

Mitigation: Use only content approved for that service and review privacy or contractual requirements before sending proprietary material.

Risk: The SenseAudio API key is required for operation.

Mitigation: Provide the key through the SENSEAUDIO_API_KEY environment variable and do not place it in skill files, source code, prompts, or commits.

## Reference(s):

- [VoiceMaster skill page](https://clawhub.ai/xiaocaijic/skills/vociemaster)
- [SenseAudio API key documentation](https://senseaudio.cn/docs/api-key)
- [SenseAudio text-to-speech API documentation](https://senseaudio.cn/docs/text_to_speech_api)
- [SenseAudio voice API documentation](https://senseaudio.cn/docs/voice_api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, generated script text, MP3 file paths, and optional debug JSON paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write MP3 audio files, segmented audio files, concatenated outputs, and debug JSON logs beside generated audio.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
