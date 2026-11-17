## Description:

Smart Voice Reply helps an agent synthesize spoken replies, select voice styles, and configure custom voice instructions for voice responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slbqc](https://clawhub.ai/user/slbqc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to reply with generated voice audio, choose voice personas by scenario, or add reusable voice-instruction presets. The skill requires a DashScope API key and can send reply text and voice instructions to DashScope for synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reply text and voice instructions are sent to DashScope for text-to-speech synthesis.

Mitigation: Use the skill only when external processing is acceptable, avoid sensitive reply text, and treat DASHSCOPE_API_KEY as a secret.

Risk: Setup can add persistent USER.md behavior that makes the agent return voice messages by default.

Mitigation: Review USER.md changes before accepting them and enable always-on voice replies only when persistent voice behavior is intended.

Risk: The TTS tool writes local request, response, and audio files, and the security guidance flags temp-id handling for shared or untrusted workflows.

Mitigation: Use a scoped output directory, avoid untrusted temp-id values or shared paths, and clean generated files when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/slbqc/skills/smart-voice-reply)
- [Installation and configuration guide](docs/技能安装配置指导.md)
- [Voice instruction creation guide](docs/音色指令创建指导.md)
- [DashScope multimodal generation API endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation)
- [Installation support guide](https://flowus.cn/laoyuanxiaoketang/share/220f7758-5744-4fb8-92cd-17c71e3a304e?code=9M1N65)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands and generated audio file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local request and response JSON files plus OPUS audio output; requires DASHSCOPE_API_KEY and ffmpeg.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
