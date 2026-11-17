## Description:

Creates drafts and optionally publishes WeChat Official Account articles using either the WeChat API for service accounts or browser automation for personal subscription accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antaeus001](https://clawhub.ai/user/antaeus001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content teams use this skill to create WeChat Official Account drafts from titles, Markdown-like article content, and cover images, then publish or submit those drafts when account permissions allow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser mode can expose authenticated WeChat page data to an analyzer model or endpoint.

Mitigation: Prefer API mode when possible, or use a local/self-hosted analyzer endpoint and avoid external analyzer API keys for sensitive accounts.

Risk: Debug and step modes can persist screenshots, page HTML, and browser session data on disk.

Mitigation: Avoid debug and step modes for sensitive accounts, and clear ~/.openclaw/wechat-mp-browser plus generated debug files when finished.

Risk: Model-driven browser automation can act on broad authenticated page access.

Mitigation: Review browser-mode behavior before installing and supervise account actions, especially before publishing or saving content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antaeus001/skills/wechat-official-account)
- [WeChat Official Account API endpoint](https://api.weixin.qq.com)
- [WeChat Official Account admin](https://mp.weixin.qq.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and Python script usage; API mode can return JSON status output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Article titles are limited to 32 characters by the scripts, content is capped below 20,000 characters, and browser analysis truncates page HTML before model analysis.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
