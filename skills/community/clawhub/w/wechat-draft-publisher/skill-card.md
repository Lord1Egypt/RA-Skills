## Description:

Generates Chinese WeChat Official Account articles from a short topic, optionally creates images, formats Markdown as WeChat-compatible HTML, and saves the result to the WeChat draft box.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuzhudewenjian](https://clawhub.ai/user/zhuzhudewenjian)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and developers use this skill to draft Chinese WeChat Official Account articles from a short topic, add optional AI-generated images, format the article for WeChat, and create a draft in the account backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify a WeChat Official Account by uploading media and creating drafts, and its --publish option can submit a draft for publication.

Mitigation: Use credentials for a dedicated low-privilege account, review the generated draft in the WeChat backend, and avoid --publish unless a human has approved the content.

Risk: Article topics and image prompts may be sent to a configured external image-generation provider.

Mitigation: Use only approved image providers, avoid sensitive content in prompts, and disable images with --no-images when external image processing is not acceptable.

Risk: The skill relies on WeChat and image-provider API keys.

Mitigation: Store keys in environment variables or a local config file that is not shared, rotate them regularly, and never paste secrets into the conversation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhuzhudewenjian/skills/wechat-draft-publisher)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/)
- [WeChat Official Account API Base](https://api.weixin.qq.com/cgi-bin)
- [SiliconFlow](https://siliconflow.cn/)
- [Default Image Generation Endpoint](https://api.siliconflow.cn/v1/images/generations)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown articles, inline shell commands, configuration JSON, and WeChat draft/API result summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WeChat credentials and python3; optional image generation uses a configured OpenAI-compatible image API. The skill can upload media, create WeChat drafts, and optionally submit drafts for publication.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
