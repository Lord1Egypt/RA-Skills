## Description: <br>
专业级 AI 短视频配音助手，支持多角色音色映射、自动语速调节及 BGM 建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaocaijic](https://clawhub.ai/user/xiaocaijic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and operators use VoiceMaster to draft and confirm short-video scripts, map roles to SenseAudio voices, synthesize TTS audio, concatenate segments, and receive background music direction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User scripts and API responses may be saved locally in debug JSON files. <br>
Mitigation: Use the skill only with text acceptable for local debug logging, delete sidecar debug logs after use, or make debug logging opt-in and redacted before deployment. <br>
Risk: TTS input is sent to SenseAudio for synthesis. <br>
Mitigation: Do not submit confidential scripts unless the user has approved sharing them with SenseAudio. <br>


## Reference(s): <br>
- [ClawHub VoiceMaster release page](https://clawhub.ai/xiaocaijic/vociemaster) <br>
- [SenseAudio API key documentation](https://senseaudio.cn/docs/api-key) <br>
- [SenseAudio text-to-speech API documentation](https://senseaudio.cn/docs/text_to_speech_api) <br>
- [SenseAudio voice API documentation](https://senseaudio.cn/docs/voice_api) <br>
- [SenseAudio TTS API endpoint](https://api.senseaudio.cn/v1/t2a_v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown responses with helper command output and generated MP3 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY and declares curl, jq, and ffmpeg as required binaries; ffmpeg is used for local audio concatenation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
