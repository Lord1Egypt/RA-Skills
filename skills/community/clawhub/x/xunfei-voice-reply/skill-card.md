## Description: <br>
Generates voice replies with Xunfei TTS and sends the resulting audio through Feishu when voice reply mode is enabled. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wglnngt](https://clawhub.ai/user/wglnngt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to switch between text and voice reply modes, synthesize replies through Xunfei TTS, and deliver Opus audio messages in Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice replies may send message content to Xunfei for synthesis and through Feishu for delivery. <br>
Mitigation: Use voice mode only for content approved for those services and switch back to text mode for sensitive conversations. <br>
Risk: Xunfei credentials are required and could be exposed if reused broadly. <br>
Mitigation: Use dedicated Xunfei credentials and store XUNFEI_APP_ID, XUNFEI_API_KEY, and XUNFEI_API_SECRET in the runtime environment rather than in shared text. <br>
Risk: Voice mode persists in USER.md until changed. <br>
Mitigation: Confirm the stored reply mode before sessions that require text-only responses. <br>
Risk: Audio generation depends on ffmpeg and the ws package being installed locally. <br>
Mitigation: Install ffmpeg and ws from trusted package sources and verify the audio path before enabling voice replies. <br>


## Reference(s): <br>
- [XunFei Voice Reply on ClawHub](https://clawhub.ai/wglnngt/xunfei-voice-reply) <br>
- [Setup Guide](references/setup.md) <br>
- [Voice Reply Flow](references/voice-flow.md) <br>
- [Xunfei Open Platform](https://www.xfyun.cn/) <br>
- [Xunfei Online TTS API Documentation](https://www.xfyun.cn/doc/tts/online_tts/API.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Audio files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated Opus audio file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces /tmp/openclaw/voice-reply.opus for Feishu voice delivery when configured with Xunfei credentials and ffmpeg.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
