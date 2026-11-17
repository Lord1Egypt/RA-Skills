## Description:

为微信小店、视频号、社群和私域运营生成与编辑商品演示、直播预热、店主讲解、朋友圈视频及复购内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and agent users use this skill to prepare WeChat Shop and Channels ecommerce video prompts, command examples, and AI Hive generation tasks for product demos, livestream warmups, host-style explanations, group-buying clips, and repurchase content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer API credentials may be sent to a custom API endpoint if the user overrides the default AI Hive base URL.

Mitigation: Keep the API endpoint on the default trusted HTTPS host and avoid untrusted environment variables or config files.

Risk: Uploaded media, prompts, generated results, API usage, and account credits can be sensitive.

Mitigation: Use a virtual environment, limit inputs to approved business materials, and avoid unnecessary personal or customer information.

Risk: Generated ecommerce videos could include misleading claims about reviews, sales volume, scarcity, prices, customer stories, or platform rules.

Mitigation: Follow the skill's acceptance checks and add prices, rules, contact details, customer stories, and compliance-sensitive claims only after human review.

## Reference(s):

- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/wechat-shop-ecommerce-video-generation-editing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline bash commands and downloaded video or image files from AI Hive tasks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI Hive API credentials, optional media inputs, routing options, task polling, and optional automatic result downloads.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
