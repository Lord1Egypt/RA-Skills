## Description: <br>
火山引擎豆包语音合成模型2.0 TTS。支持多种音色、情感参数、SSML标记，生成高质量中文语音，支持一键发送飞书语音气泡。使用HTTP单向流式API，稳定可靠。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raydoomed](https://clawhub.ai/user/raydoomed) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to synthesize Chinese speech with Volcengine Doubao TTS and optionally send the generated audio as a Feishu voice message. It supports command-line configuration for credentials, voices, emotions, SSML input, output files, and Feishu delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input text, generated audio, and credentials may be sensitive because the skill sends text to Volcengine and can upload generated audio to Feishu. <br>
Mitigation: Use only organization-approved text, protect the Volcengine and Feishu configuration files, and confirm provider use is allowed for the data. <br>
Risk: Sending to the wrong Feishu open_id can disclose generated voice content to an unintended recipient. <br>
Mitigation: Verify the Feishu open_id before using --send-to. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raydoomed/volcengine-tts-feishu) <br>
- [Volcengine voice list](https://www.volcengine.com/docs/6561/1257544) <br>
- [Volcengine TTS HTTP streaming API](https://www.volcengine.com/docs/6561/1598757) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The companion script can produce MP3 audio files and, when configured, upload Opus audio to Feishu.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
