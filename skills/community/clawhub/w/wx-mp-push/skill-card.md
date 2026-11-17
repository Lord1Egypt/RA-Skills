## Description:

Automates WeChat Official Account article publishing by creating and managing article drafts through the WeChat API, supporting Markdown and HTML input, Markdown-to-WeChat HTML conversion, cover image upload, and inline image upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onceyoungs](https://clawhub.ai/user/onceyoungs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and content operations teams use this skill to configure WeChat Official Account credentials, convert article content, upload images, and create WeChat article drafts through scripted API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses WeChat AppID/AppSecret credentials and may cache access tokens on disk.

Mitigation: Keep credentials out of source control, protect or disable the token cache on shared machines, and restrict configuration file permissions.

Risk: The publishing script can read local image paths and fetch remote image URLs from article content.

Mitigation: Use trusted article content only, run from a narrow content directory, and avoid external image URLs unless they are intended to be fetched and uploaded.

Risk: The skill sends credentials, media, and draft article data to a configured API endpoint.

Mitigation: Keep apiBaseUrl pinned to the real WeChat API endpoint and review drafts before operational use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/onceyoungs/skills/wx-mp-push)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com)
- [WeChat API Base URL](https://api.weixin.qq.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide execution of a Python script that reads article content and images, uploads media, caches access tokens, and creates WeChat article drafts.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
