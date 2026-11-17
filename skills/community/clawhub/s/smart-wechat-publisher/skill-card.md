## Description:

自动收集 AI 新闻，生成 HTML 内容，并将内容发布到微信公众号草稿箱，支持模板和发布时间配置。

This skill is ready for commercial/non-commercial use.

## Publisher:

[403914291](https://clawhub.ai/user/403914291)

### License/Terms of Use:

MIT-0

## Use Case:

公众号 operators and content automation users can use this skill to prepare AI-news articles, configure WeChat account credentials, and create scheduled WeChat draft posts for human review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles WeChat AppSecret credentials and the security evidence says secret handling is unsafe.

Mitigation: Use a restricted, rotatable WeChat credential, prefer environment-based secret handling, and avoid entering AppSecret values in shell history or ordinary shared files.

Risk: The security evidence flags risky privileged installation guidance.

Mitigation: Review and change the setup flow before installation; avoid sudo and curl-to-bash style setup paths unless they have been independently reviewed.

Risk: The security evidence says the generated draft can include hardcoded or fabricated publishing content.

Mitigation: Inspect every generated WeChat draft before publication and remove hardcoded footer, author, or source claims that are not accurate.

Risk: The release is marked suspicious by the authoritative security scan.

Mitigation: Install only after security review, keep the credential scoped and rotatable, and monitor generated drafts and local status files during initial use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/403914291/skills/smart-wechat-publisher)
- [Publisher profile](https://clawhub.ai/user/403914291)
- [User guide](artifact/docs/user_guide.md)
- [Release changelog](artifact/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, HTML, shell commands, configuration]

**Output Format:** [Markdown guidance, JSON configuration, HTML article content, and WeChat draft/status identifiers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When executed, it uses WeChat credentials to create draft content and records local status, token cache, usage, and result files.]

## Skill Version(s):

1.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
