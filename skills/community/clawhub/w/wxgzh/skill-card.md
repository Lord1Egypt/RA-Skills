## Description:

微信公众号文章发布工具。使用 wxgzh CLI 将 Markdown 文章发布到公众号草稿箱。触发场景：用户要发公众号文章、配置公众号 AppID/AppSecret、生成封面图、Markdown 转 HTML。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyhue1991](https://clawhub.ai/user/lyhue1991)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content operators, and WeChat Official Account publishers use this skill to prepare configuration, convert Markdown, generate cover images, and publish articles to an official account draft box through the wxgzh CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles a sensitive WeChat Official Account AppSecret.

Mitigation: Avoid sharing AppSecret in ordinary chat or shell history, restrict permissions on ~/.config/wxgzh/wxgzh.json, and rotate the secret if it has appeared in logs or transcripts.

Risk: The documented install command installs the wxgzh CLI globally without pinning a version.

Mitigation: Install only after trusting the @lyhue1991/wxgzh package, and pin or review the CLI version before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lyhue1991/skills/wxgzh)
- [Public IP lookup used for WeChat IP whitelist setup](https://ip.sb/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown, Code, Files]

**Output Format:** [Markdown guidance with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or reference local .wxgzh/ intermediate files for generated covers and converted article HTML.]

## Skill Version(s):

0.1.4 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
