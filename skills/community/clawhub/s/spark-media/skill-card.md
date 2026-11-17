## Description:

Generates or edits images, creates videos, checks media tasks, and publishes user-generated assets to Xiaohongshu when explicitly requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youteacher](https://clawhub.ai/user/youteacher)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to create or edit images and videos through the AI Skills platform and track task results. They may also publish their own generated media to a linked Xiaohongshu account when they explicitly request it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and images are sent to the configured API provider, and the security review is incomplete.

Mitigation: Check that you trust the provider, avoid sending sensitive images or prompts, and review the referenced materials before use.

## Reference(s):

- [AI Skills platform](https://ai-skills.open-idea.net/)
- [API key configuration](https://ai-skills.open-idea.net/skill-docs/spark-media/API-KEY.md)
- [Image generation and editing](https://ai-skills.open-idea.net/skill-docs/spark-media/IMAGE-GENERATION.md)
- [Video generation and task polling](https://ai-skills.open-idea.net/skill-docs/spark-media/VIDEO-GENERATION.md)
- [HTTP requests and task handling](https://ai-skills.open-idea.net/skill-docs/spark-media/HTTP-REQUESTS.md)
- [Authorization, errors, and retries](https://ai-skills.open-idea.net/skill-docs/spark-media/BEHAVIOR-RULES.md)
- [Xiaohongshu publishing](https://ai-skills.open-idea.net/skill-docs/spark-media/XIAOHONGSHU.md)

## Skill Output:

**Output Type(s):** [Images, Videos, Text]

**Output Format:** [Generated image or video assets or result links, with task status and guidance in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation can use up to five reference images and video generation up to nine. Publishing to Xiaohongshu requires an explicit user request and defaults to private.]

## Skill Version(s):

2.11.1 (source: server-resolved release and packageVersion metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
