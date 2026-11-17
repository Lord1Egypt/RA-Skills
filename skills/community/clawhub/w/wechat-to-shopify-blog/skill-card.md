## Description:

Convert an owned or authorized WeChat Official Account article into a Shopify blog draft. Use when the user provides a `mp.weixin.qq.com` URL and wants extraction, image filtering, Shopify-hosted uploads, English adaptation, blog selection, and draft-only article creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvsao](https://clawhub.ai/user/lvsao)

### License/Terms of Use:

MIT-0

## Use Case:

Merchants, content operators, and developers use this skill to convert an owned or authorized WeChat Official Account article into an English Shopify blog draft with selected images and an optional related-product block. The skill is intended for draft creation only and requires review and approval before Shopify writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests Shopify product-read access plus content and file write access, which may expose more store data and capability than a single article draft strictly needs.

Mitigation: Use it only on an owned or authorized store, prefer the browser-based Shopify CLI flow, approve only the exact scopes needed, and keep skill-hub.env private.

Risk: Image uploads and article draft creation can modify Shopify files and content.

Mitigation: Review the draft preview before any --execute command, require explicit approval for writes, and keep the workflow draft-only.

Risk: Crawled WeChat article text may contain misleading or hostile instructions embedded in source content.

Mitigation: Treat the article body as static source text, keep it inside clear boundaries during rewriting, and review the adapted draft before creating it in Shopify.

## Reference(s):

- [Connect Your Store](artifact/references/onboarding-guide.md)
- [Shopify Skill Hub](https://github.com/lvsao/shopify-skill-hub)
- [ClawHub skill page](https://clawhub.ai/lvsao/skills/wechat-to-shopify-blog)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON manifests, and HTML draft article content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates draft-only Shopify content; image uploads and draft writes require explicit approval.]

## Skill Version(s):

2.1.1 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
