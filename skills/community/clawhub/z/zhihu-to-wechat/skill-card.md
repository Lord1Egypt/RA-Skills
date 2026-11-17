## Description:

Automates a workflow that turns Zhihu trending topics into IT-style WeChat Official Account articles with images, WeChat-compatible HTML formatting, and draft publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dachenchen690-droid](https://clawhub.ai/user/dachenchen690-droid)

### License/Terms of Use:


## Use Case:

Content creators, technology bloggers, and developers use this skill to select Zhihu trending topics, research the selected topic, generate an IT-focused WeChat article, format it for WeChat, and create a WeChat draft for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires powerful WeChat service-account credentials.

Mitigation: Use a dedicated WeChat service account, provide credentials through environment variables or a secret manager, avoid sharing secrets in chat or command-line history, and rotate any secrets already exposed.

Risk: Generated article HTML could include inaccurate, misleading, or unsafe content before publication.

Mitigation: Inspect and edit generated HTML and draft content in the WeChat backend before publishing.

Risk: External image URLs are downloaded and uploaded during publishing.

Mitigation: Use trusted image sources, verify licensing and content, and block untrusted or user-supplied image URLs from reaching the publisher.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dachenchen690-droid/skills/zhihu-to-wechat)
- [WeChat API reference](artifact/references/wechat_api.md)
- [WeChat HTML style guide](artifact/references/wechat_html_style.md)
- [IT article template](artifact/assets/it_article_template.md)
- [WeChat Official Accounts platform](https://mp.weixin.qq.com)
- [Unsplash developers](https://unsplash.com/developers)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown articles, WeChat-compatible HTML, JSON script results, and WeChat draft identifiers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local HTML files and WeChat draft records when account credentials, image URLs, and service-account permissions are provided.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
