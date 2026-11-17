## Description:

Publish one or multiple Markdown articles to a WeChat Official Account draft box, with support for combined drafts, cover selection, custom styling, inline image upload, digest extraction, and optional immediate publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x402spark-jpg](https://clawhub.ai/user/x402spark-jpg)

### License/Terms of Use:


## Use Case:

Developers and content operators use this skill to prepare Markdown articles, push single or multi-article drafts to WeChat Official Account, preview output with dry runs, and optionally trigger publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local files referenced by Markdown to WeChat CDN.

Mitigation: Only process trusted Markdown and images, use dry-run first, and avoid externally supplied content until image path confinement is fixed.

Risk: The skill can publish to a live WeChat account when the publish option is used.

Mitigation: Do not run with publish mode unless live publication is intended, and review rendered drafts before publishing.

Risk: WeChat credentials are required for live API calls.

Mitigation: Keep credentials in environment variables or a protected secret store when possible, and use owner-only permissions for any credentials file.

## Reference(s):

- [Setup Guide](references/setup.md)
- [WeChat Official Account API endpoint](https://api.weixin.qq.com/cgi-bin)
- [ClawHub skill page](https://clawhub.ai/x402spark-jpg/skills/wechat-multi-publisher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent guidance for publishing Markdown content and using dry-run, draft, and publish modes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
