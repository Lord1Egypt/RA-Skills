## Description: <br>
Converts text to speech and sends the resulting audio message to Feishu, using either a configured TTS API or a local ChatTTS service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enihsago](https://clawhub.ai/user/enihsago) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate spoken messages from text and deliver them to Feishu users or group chats. It supports API-based TTS for hosted voice generation and local ChatTTS for local voice generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local ChatTTS mode starts an unauthenticated service that may be reachable beyond the local machine. <br>
Mitigation: Bind the service to 127.0.0.1 or firewall port 8080, avoid exposing it to other machines, and stop it when finished. <br>
Risk: The skill requires Feishu message-sending credentials and may send message text to a configured TTS provider in API mode. <br>
Mitigation: Install only if the operator accepts those credential and data-sharing requirements; use scoped Feishu app credentials and a trusted TTS endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/enihsago/voice2feishu) <br>
- [Publisher profile](https://clawhub.ai/user/enihsago) <br>
- [ChatTTS](https://github.com/2noise/ChatTTS) <br>
- [ChatTTS model](https://huggingface.co/2Noise/ChatTTS) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [Zhipu AI TTS API](https://open.bigmodel.cn/api/paas/v4/audio/speech) <br>
- [OpenAI TTS API](https://api.openai.com/v1/audio/speech) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, audio files, API calls, guidance] <br>
**Output Format:** [Command-line guidance and shell execution that generates audio and sends Feishu messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu credentials, curl, jq, ffmpeg, and ffprobe; API mode also requires TTS API configuration.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
