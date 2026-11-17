## Description:

Publish Markdown articles to a WeChat Official Account with AI cover generation, inline styling, HTML card rendering, draft creation, and optional publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[864446285](https://clawhub.ai/user/864446285)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content publishers use this skill to prepare Markdown articles for a WeChat Official Account, generate or accept a cover image, optionally render HTML cards, create drafts, and publish after explicit review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish public content through a WeChat Official Account.

Mitigation: Create drafts first and use automatic publishing only after explicit human review.

Risk: The skill uses WeChat publishing credentials and caches access tokens on disk.

Mitigation: Protect ~/.wechat_publish with owner-only permissions, avoid shared machines, and rotate credentials if exposure is suspected.

Risk: The skill installs and runs Python dependencies, with optional Playwright browser automation for HTML card rendering.

Mitigation: Install dependencies in a dedicated virtual environment from trusted package indexes.

## Reference(s):

- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/)
- [WeChat Official Account API](https://api.weixin.qq.com)
- [ClawHub skill page](https://clawhub.ai/864446285/skills/wechat-md-publish)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, generated article assets, and script output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create WeChat drafts, upload article images and covers, render optional HTML cards to images, and publish drafts when requested.]

## Skill Version(s):

0.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
