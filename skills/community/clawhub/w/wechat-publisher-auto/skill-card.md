## Description:

Converts Markdown or HTML articles into WeChat Official Account-ready content, optionally rewrites drafts with an AI provider, and publishes them to the WeChat draft box.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuesf](https://clawhub.ai/user/yuesf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and agents use this skill to prepare WeChat Official Account articles from Markdown or HTML, manage publishing credentials, test WeChat connectivity, upload images, and create draft posts. It is useful when repeated article formatting and draft publication need to be automated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper shell wrapper can execute unintended shell code through unsafe command construction and direct environment-file sourcing.

Mitigation: Prefer the Python CLI with explicit commands and avoid the shell wrapper until the unsafe eval and direct .env sourcing behavior are fixed.

Risk: Article drafts and credentials may be sent to WeChat and any configured AI provider.

Mitigation: Use non-sensitive drafts unless external processing is acceptable, protect the local config file with owner-only permissions, and use narrowly scoped WeChat and AI credentials.

Risk: Installing an unpinned release can expose users to unreviewed package changes.

Mitigation: Pin installation to a trusted release or commit and review the skill before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuesf/skills/wechat-publisher-auto)
- [WeChat Official Accounts developer platform](https://developers.weixin.qq.com/)
- [WeChat Official Accounts platform](https://mp.weixin.qq.com/)

## Skill Output:

**Output Type(s):** [text, markdown, html, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, configuration snippets, and generated HTML or WeChat draft-publication results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send article content to WeChat and, when AI humanization is enabled, to the configured AI provider.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence; artifact package metadata lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
