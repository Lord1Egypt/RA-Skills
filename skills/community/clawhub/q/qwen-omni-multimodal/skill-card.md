## Description:

This skill helps an agent use Alibaba Cloud DashScope Qwen3.5-Omni for text, image, audio, and video understanding, with optional text or speech output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouweico](https://clawhub.ai/user/zhouweico)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Qwen Omni models for image analysis, audio transcription or summarization, video understanding, cross-modal question answering, and direct speech responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials and private media can be sent to a user-configurable endpoint.

Mitigation: Prefer DASHSCOPE_API_KEY from the environment or a secret manager, keep config files out of source control, and use the official DashScope HTTPS endpoints unless a custom endpoint is intentionally trusted.

Risk: Sensitive prompts, media, and conversation context may be processed remotely and retained in local session files.

Mitigation: Avoid sensitive inputs unless remote Alibaba Cloud processing and local session retention are acceptable, and use fresh or cleared sessions when context should not persist.

## Reference(s):

- [Qwen-Omni API Notes](references/api.md)
- [Alibaba Cloud Model Studio Qwen-Omni documentation](https://help.aliyun.com/zh/model-studio/qwen-omni)
- [Alibaba Cloud Model Studio Qwen API reference](https://help.aliyun.com/zh/model-studio/developer-reference/use-qwen-by-calling-api)
- [Alibaba Cloud Model Studio streaming guide](https://help.aliyun.com/zh/model-studio/stream)
- [ClawHub skill page](https://clawhub.ai/zhouweico/skills/qwen-omni-multimodal)

## Skill Output:

**Output Type(s):** [Text, Audio, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands, text responses, optional WAV audio files, and configuration JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses streaming API responses, optional local session history, and best-effort cost reminders when token usage is available.]

## Skill Version(s):

0.2.0 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
