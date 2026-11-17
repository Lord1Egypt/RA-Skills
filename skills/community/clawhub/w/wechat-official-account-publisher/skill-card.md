## Description:

Publish articles to a WeChat Official Account draft box via API, including token management, local image upload to WeChat CDN, Markdown-to-HTML conversion, and draft creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuejiangli](https://clawhub.ai/user/yuejiangli)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and content teams use this skill to have an agent turn a Markdown article plus local cover and body images into a WeChat Official Account draft for manual review and publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles WeChat Official Account API credentials and caches access tokens locally.

Mitigation: Use environment variables or a protected secrets manager, keep config.json and .token_cache.json out of source control, and restrict permissions on token-cache files.

Risk: Article text, metadata, cover images, and selected body images are uploaded to WeChat.

Mitigation: Run the skill only for content approved for WeChat upload and review generated drafts in the WeChat backend before publishing.

Risk: WeChat API permissions, token expiry, or media constraints can prevent draft creation.

Mitigation: Confirm the account has the required draft and API access, re-upload media when IDs are invalid, and refresh cached tokens when authentication fails.

## Reference(s):

- [WeChat Official Account API Reference](references/wechat_api.md)
- [WeChat MP Backend](https://mp.weixin.qq.com)
- [ClawHub Skill Page](https://clawhub.ai/yuejiangli/skills/wechat-official-account-publisher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, generated HTML, and WeChat media IDs or URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads article text, metadata, cover images, and optional inline images to WeChat; the draft is not published automatically.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
