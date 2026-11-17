## Description:

Markdown 发布为微信公众号草稿（wenyan-cli；主题、代码高亮）。公众号发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hidebug](https://clawhub.ai/user/hidebug)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and developers use this skill to prepare Markdown articles with required frontmatter and local images, then publish them as WeChat Official Account drafts through wenyan-cli with theme and code-highlighting options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload selected Markdown and images to WeChat using the user's WeChat AppID and AppSecret.

Mitigation: Run it only on intended article files, provide credentials through environment variables or a managed secret mechanism, and avoid committing real credentials to TOOLS.md.

Risk: The script may install the wenyan-cli package globally with npm when the wenyan command is missing.

Mitigation: Prefer preinstalling and reviewing a pinned wenyan-cli version before running the skill in a production workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hidebug/skills/xqx-wechat-publisher)
- [wenyan-cli themes](references/themes.md)
- [wechat-publisher troubleshooting](references/troubleshooting.md)
- [wenyan-cli GitHub](https://github.com/caol64/wenyan-cli)
- [wenyan documentation](https://wenyan.yuzhi.tech)
- [wenyan upload documentation](https://yuzhi.tech/docs/wenyan/upload)
- [WeChat Official Account documentation](https://developers.weixin.qq.com/doc/offiaccount/)
- [wenyan-core theme assets](https://github.com/caol64/wenyan-core/tree/main/src/assets/themes)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishes a selected Markdown file as a WeChat draft when credentials, frontmatter, local images, Node/npm, and wenyan-cli are available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
