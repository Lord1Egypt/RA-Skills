## Description:

Automates publishing WeChat Official Account articles with media upload, draft management, status queries, and draft deletion through the WeChat MP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan32382](https://clawhub.ai/user/ryan32382)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators managing WeChat Official Accounts use this skill to upload media, create drafts, publish articles, check publication status, and delete drafts through the WeChat MP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish articles publicly or delete drafts for a WeChat Official Account.

Mitigation: Require explicit human approval before public publishing or deleting drafts.

Risk: The skill uses WeChat application credentials and caches access tokens.

Mitigation: Use least-privilege credentials and protect configuration and token files with restrictive permissions or a secret manager.

Risk: Media upload tools accept local file paths.

Mitigation: Avoid uploading arbitrary local paths and review selected files before upload.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ryan32382/skills/ryan-wechat-mp)
- [WeChat Official Account API Overview](https://developers.weixin.qq.com/doc/offiaccount/en/Getting_Started/Overview.html)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance, Configuration]

**Output Format:** [JSON tool responses with concise human-readable status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool responses use success, message, and optional data fields; some workflows can publish or delete account content.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
