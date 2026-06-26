## Description: <br>
Runs a local Qwen3-ASR speech-to-text service for QQBot and OpenClaw voice-message transcription. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rekslee](https://clawhub.ai/user/rekslee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to connect QQBot voice messages to a locally hosted speech-to-text pipeline. It provides setup guidance, configuration examples, and Python entry points for running Qwen3-ASR through a local HTTP service or CLI script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence says the skill instructions point to a differently named skill. <br>
Mitigation: Confirm whether qqbot-stt and local-stt refer to the same trusted package before installation or deployment. <br>
Risk: The release evidence flags under-scoped network and server risk. <br>
Mitigation: Prefer the localhost-only server path and avoid exposing the transcription service to a network without authentication and request limits. <br>
Risk: The release evidence flags dependency and model-loading review concerns. <br>
Mitigation: Pin and audit Python dependencies, and review any trust_remote_code model-loading examples before use. <br>
Risk: OpenClaw configuration can contain QQBot credentials and other secrets. <br>
Mitigation: Keep OpenClaw configuration files private and avoid sharing logs or examples that include real bot secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rekslee/qqbot-stt) <br>
- [QQBot OpenClaw guide](https://new.qq.com/rain/a/20260316A06XBW00) <br>
- [OpenClaw voice configuration guide](https://blog.csdn.net/yangyin007/article/details/158649849) <br>
- [Qwen3-ASR local deployment guide](https://blog.csdn.net/weixin_42509513/article/details/158311971) <br>
- [QQBot plugin repository](https://github.com/tencent-connect/openclaw-qqbot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and Python scripts that return transcription text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The HTTP path returns OpenAI-compatible JSON transcription responses; the CLI path prints plain text to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
