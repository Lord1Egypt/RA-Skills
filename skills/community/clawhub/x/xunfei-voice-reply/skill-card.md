## Description:

Generates voice replies with Xunfei TTS and sends Opus audio to Feishu when voice mode is enabled.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wglnngt](https://clawhub.ai/user/wglnngt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let an agent switch between text and voice replies, synthesize reply text through Xunfei TTS, and send the resulting Opus audio to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reply content is sent to Xunfei for speech synthesis and then to Feishu as audio.

Mitigation: Use the skill only when that data sharing is acceptable, and avoid sending sensitive content unless the deployment policy allows it.

Risk: Voice mode can persist across sessions by writing USER.md.

Mitigation: Require confirmation before enabling voice mode or writing USER.md, and keep trigger commands narrow.

Risk: Audio conversion uses shell-based ffmpeg calls and predictable temporary audio paths.

Mitigation: Pin dependencies, replace shell string execution with argument-array execution, and use private per-run temporary files before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wglnngt/skills/xunfei-voice-reply)
- [Environment setup](references/setup.md)
- [Voice reply flow](references/voice-flow.md)
- [Xunfei Open Platform](https://www.xfyun.cn/)
- [Xunfei online TTS API documentation](https://www.xfyun.cn/doc/tts/online_tts/API.html)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and JavaScript examples; command execution may produce a VOICE_READY file path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When executed with credentials and ffmpeg available, the voice script writes a temporary Opus audio file under /tmp/openclaw.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
