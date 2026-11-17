## Description:

Supports publishing styled articles to one or more WeChat Official Accounts with custom themes, account-specific credentials, and optional intro and outro templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[web3aivc](https://clawhub.ai/user/web3aivc)

### License/Terms of Use:

MIT-0

## Use Case:

External publishers, developers, and automation operators use this skill to style HTML articles, manage per-account WeChat publishing configuration, import reusable intro/outro templates, and publish drafts to one or more WeChat Official Accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeChat app credentials and access tokens can be exposed if configuration files or token caches are stored in shared workspaces.

Mitigation: Keep real WeChat secrets out of committed or shared files, use secret-managed configuration where possible, and restrict token-cache permissions.

Risk: Template imports and publishing can fetch external URLs and call WeChat API endpoints.

Mitigation: Run the skill only against trusted URLs and use the default official WeChat API endpoint unless a proxy is explicitly trusted.

Risk: Local image and cover upload behavior can send workspace files to WeChat.

Mitigation: Review article HTML, image paths, and cover paths before publishing, and sandbox untrusted HTML or URL inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/web3aivc/skills/wechat-style-publisher)
- [ClawHub publisher profile](https://clawhub.ai/user/web3aivc)
- [WeChat API endpoint used by artifact configuration](https://api.weixin.qq.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, and generated or transformed HTML content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local files and perform network publication when the referenced scripts are executed with credentials.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; package.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
