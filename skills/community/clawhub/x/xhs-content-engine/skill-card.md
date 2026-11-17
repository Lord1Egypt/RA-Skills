## Description:

小红书内容引擎帮助代理拆解小红书爆款链接，并基于拆解卡、品牌图谱和配置的生成服务产出脚本、文案、图片素材、封面、标签及可选视频提示或成片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dizhu](https://clawhub.ai/user/dizhu)

### License/Terms of Use:

MIT-0

## Use Case:

Content strategists, marketers, and agent operators use this skill to analyze Xiaohongshu reference posts and generate brand-adapted content packages for campaign planning and production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can call configurable third-party crawler, LLM, image, and video services using local environment or `.env` credentials.

Mitigation: Use provider keys dedicated to this skill, avoid untrusted project-local `.env` files, and only set custom base URLs to hosts you control.

Risk: Prompts, Xiaohongshu data, generated content, and brand context may be sent to external providers.

Mitigation: Confirm the selected crawler, LLM, image, and video providers are approved to receive the material before processing confidential brand information.

Risk: Real video generation can create paid API usage.

Mitigation: Use `--no-real-video` while drafting and review the cost estimate before intentionally approving video generation.

Risk: The skill can persist learned content into graph knowledge files that later influence generated brand content.

Mitigation: Review graph changes before reusing them as trusted brand context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dizhu/skills/xhs-content-engine)
- [Configuration guide](references/configuration.md)
- [Deconstruction output template](references/output-template.md)
- [Video example](references/example-video.md)
- [Image example](references/example-image.md)
- [Ofox](https://ofox.ai)
- [OpenRouter](https://openrouter.ai)
- [Volcengine Ark API keys](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey)

## Skill Output:

**Output Type(s):** [Markdown, Text, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown, plain text, JSON-backed workspace files, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate local deconstruction cards, content package files, image prompts or images, video prompts or optional composed video files, and graph updates.]

## Skill Version(s):

0.3.4 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
