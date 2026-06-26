## Description: <br>
Send text as voice-message audio across chat channels using edge-tts for speech synthesis and ffmpeg for audio conversion, with channel-specific handling for Feishu/Lark and Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xmanrui](https://clawhub.ai/user/xmanrui) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and teams use this skill to generate OGG/Opus voice files from text and prepare or send them as chat voice messages. It is especially useful when a platform needs channel-specific handling, such as Feishu/Lark audio-message uploads or Discord waveform metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice text is sent to an external text-to-speech service when generating audio. <br>
Mitigation: Avoid using sensitive text unless the external service is approved for that data. <br>
Risk: Generated audio and message metadata may be uploaded to Feishu/Lark or other chat platforms. <br>
Mitigation: Confirm that the destination platform and recipient are appropriate before sending generated voice messages. <br>
Risk: Feishu/Lark sending requires a tenant access token. <br>
Mitigation: Use short-lived tokens where possible and avoid placing long-lived tokens in shared transcripts, logs, or shell history. <br>


## Reference(s): <br>
- [Voice Reference](references/voices.md) <br>
- [Feishu Open API](https://open.feishu.cn/open-apis) <br>
- [ClawHub skill page](https://clawhub.ai/xmanrui/voice-message) <br>
- [Publisher profile](https://clawhub.ai/user/xmanrui) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates or describes OGG/Opus audio files, Discord waveform metadata, and Feishu/Lark API calls when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
