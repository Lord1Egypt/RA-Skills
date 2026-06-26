## Description: <br>
SenseAudio Voice provides text-to-speech and automatic speech recognition workflows with automatic language-based engine selection for Chinese, English, and Japanese. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cowboy231](https://clawhub.ai/user/cowboy231) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent builders use this skill to add speech synthesis, speech playback, and audio transcription workflows to OpenClaw agents. It is suited for multilingual voice interaction where Chinese requests use SenseAudio services and English or Japanese requests use Edge TTS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends text and audio data to external voice services. <br>
Mitigation: Avoid confidential recordings or prompts unless third-party processing is acceptable for the deployment. <br>
Risk: The skill can reuse a SenseAudio API key from existing OpenClaw configuration files. <br>
Mitigation: Use a dedicated SenseAudio API key for this skill and review shared OpenClaw configs before installing. <br>
Risk: Generated audio files and filename previews can expose sensitive content locally. <br>
Mitigation: Delete generated audio files when their content or filenames contain sensitive information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cowboy231/senseaudio-voice-cn) <br>
- [SenseAudio text-to-speech API documentation](https://senseaudio.cn/docs/text_to_speech_api) <br>
- [SenseAudio speech recognition HTTP API documentation](https://senseaudio.cn/docs/speech_recognition/http_api) <br>
- [SenseAudio website](https://senseaudio.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated audio or transcription files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local audio files and may print transcription text or save transcription output to a user-specified file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
