## Description:

通用文生图技能。使用 MiniMax、OpenAI、DALL-E、Stability 等模型生成图片。用户需要配置自己的 API Key（MINIMAX_API_KEY、OPENAI_API_KEY 等）。当用户需要生成图片、AI绘图时使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoliang1319-cloud](https://clawhub.ai/user/xiaoliang1319-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate images from text prompts through configured MiniMax, OpenAI DALL-E, or Stability AI provider credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated-image prompts and requests may be sent to whichever configured external provider API key is available.

Mitigation: Use API keys controlled by the deploying user or organization and avoid sensitive text in image prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoliang1319-cloud/skills/publish-skill)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Files]

**Output Format:** [Markdown guidance with environment-variable examples and generated image outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes generated-image requests using available provider API keys in priority order: MiniMax, then OpenAI, then Stability AI.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
