## Description:

WeChat Official Account draft management toolkit for listing, creating, updating, and deleting drafts, uploading materials, generating cover images, and preparing article digests through the official WeChat API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy8663](https://clawhub.ai/user/andy8663)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to let an agent prepare and manage WeChat Official Account drafts, convert Markdown or HTML articles for WeChat rendering, upload images, and issue publishing-related CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Relay and hybrid modes can send WeChat account secrets and unpublished article content through a third-party relay server.

Mitigation: Prefer direct mode for production accounts. Use relay or hybrid only with a relay you fully trust and control, and rotate any AppSecret or relay key previously used with relay mode.

Risk: Draft and material delete commands can remove WeChat content without an interactive confirmation step.

Mitigation: List and inspect the target media ID and account before deletion, and restrict deletion commands to operators authorized to manage the account.

Risk: Publishing workflows rely on WeChat AppID, AppSecret, access tokens, and relay keys stored in local configuration.

Mitigation: Keep config.json out of source control, limit file access to trusted users, and rotate credentials after accidental exposure.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/andy8663/skills/wechat-oa)
- [WeChat Official Account Platform](https://mp.weixin.qq.com)
- [WeChat API Reference](references/wechat_api.md)
- [WeChat Article Layout Specification](design.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance, CLI commands, JSON configuration examples, converted HTML article content, and generated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update WeChat drafts, upload media, and generate a local cover image file.]

## Skill Version(s):

3.0.3 (source: SKILL.md frontmatter, pyproject.toml, skill.json, and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
