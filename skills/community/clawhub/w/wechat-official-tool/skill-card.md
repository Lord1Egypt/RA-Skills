## Description:

Guides WeChat Official Account operators through topic research, article drafting, image preparation, Markdown-to-WeChat draft generation, publishing, and performance analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liboss504](https://clawhub.ai/user/liboss504)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketing operators, and developers use this skill to plan WeChat Official Account content, prepare article assets, convert Markdown into WeChat draft JSON, and submit drafts through the WeChat API when account credentials are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to trust an unexplained fixed IP address for the WeChat allowlist.

Mitigation: Do not add 112.8.202.216 to a WeChat allowlist unless the publisher proves why that exact address is needed and who controls it.

Risk: The workflow depends on powerful WeChat AppID and AppSecret credentials stored in local files.

Mitigation: Store AppSecret and browser session files outside shared or synced workspaces, restrict file permissions, exclude them from Git, and rotate the AppSecret if it may have been exposed.

Risk: The publishing scripts can create or manage WeChat drafts for the configured account.

Mitigation: Use the skill only for accounts you intend to manage, and review generated drafts in the WeChat backend before publishing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/liboss504/skills/wechat-official-tool)
- [微信公众号 API 参考](references/api_ref.md)
- [微信公众号凭证配置指南](references/credentials_guide.md)
- [安装指南](assets/INSTALL.md)
- [微信公众平台](https://mp.weixin.qq.com)
- [WeChat Official Account API base](https://api.weixin.qq.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, JSON configuration examples, and generated WeChat draft JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local WeChat credentials and submit draft content to the WeChat API when the user runs the publishing scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
