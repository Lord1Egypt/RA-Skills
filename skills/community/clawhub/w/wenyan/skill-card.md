## Description:

通过 wenyan-cli，快速将带 frontmatter 的 Markdown 文章发布到微信公众号，支持主题管理和图片自动上传。

This skill is ready for commercial/non-commercial use.

## Publisher:

[caol64](https://clawhub.ai/user/caol64)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content publishers use this skill to prepare Markdown articles with frontmatter, install and verify wenyan-cli, publish to WeChat Official Accounts, manage themes, and troubleshoot common publishing errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a third-party npm CLI globally can execute package code on the local machine.

Mitigation: Verify the npm package and publisher before installing, avoid sudo, and prefer a pinned or local install when possible.

Risk: Publishing may send Markdown content, images, and WeChat account data to the configured Wenyan server and WeChat.

Mitigation: Publish only approved content and images, and keep WeChat credentials in secure environment variables or secret storage rather than shared files, logs, or screenshots.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caol64/skills/wenyan)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks and option tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language workflow guidance for using wenyan-cli with Markdown, themes, images, and WeChat credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
