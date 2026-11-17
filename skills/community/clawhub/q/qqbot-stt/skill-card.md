## Description:

qqbot-stt helps agents configure and run a local Qwen3-ASR speech-to-text service for OpenClaw QQBot voice messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rekslee](https://clawhub.ai/user/rekslee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run local speech-to-text for OpenClaw QQBot and connect the transcription endpoint through channels.qqbot.stt. It is intended for local voice-message processing with Qwen3-ASR on compatible systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes voice messages through a local service.

Mitigation: Use it only where local voice processing is acceptable and keep the service bound to 127.0.0.1 unless authentication and firewall controls are added.

Risk: Weak upload controls and temporary-file handling can create operational or data exposure risks.

Mitigation: Add upload size limits, rate limits, and reviewed temporary-file cleanup before using the service with untrusted users.

Risk: Transcript logs, OpenClaw credentials, and mutable dependency installs can expose sensitive data or change runtime behavior.

Mitigation: Avoid logging transcript contents, protect OpenClaw credentials, and pin reviewed dependency and installer versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rekslee/skills/qqbot-stt)
- [Tencent QQ Bot OpenClaw guide](https://new.qq.com/rain/a/20260316A06XBW00)
- [OpenClaw voice configuration guide](https://blog.csdn.net/yangyin007/article/details/158649849)
- [Qwen3-ASR local deployment guide](https://blog.csdn.net/weixin_42509513/article/details/158311971)
- [QQBot plugin repository](https://github.com/tencent-connect/openclaw-qqbot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, JSON, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local HTTP transcription service guidance, OpenClaw QQBot STT configuration, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
