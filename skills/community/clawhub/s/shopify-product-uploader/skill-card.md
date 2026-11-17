## Description:

Upload and manage Shopify products individually, in bulk from CSV, or from images with SEO-optimised UK English listing content, variants, collections, inventory, and draft or archive workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hussainpatan9](https://clawhub.ai/user/hussainpatan9)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators and developers use this skill to create, preview, upload, update, draft, archive, and manage Shopify product listings through an agent workflow. It is especially suited to catalogue creation from short product descriptions, CSV files, supplier data, or product images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide a powerful Shopify Admin API access token and stores it in long-term agent memory.

Mitigation: Use a dedicated Shopify custom app token with only the scopes required for the intended workflows, keep it in isolated encrypted secret storage, and rotate or revoke it if exposed.

Risk: The skill can create, update, archive, and permanently delete Shopify products.

Mitigation: Require explicit user confirmation before uploads, archive actions, or permanent deletion, and prefer draft mode for listings that need review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hussainpatan9/skills/shopify-product-uploader)
- [README.md](artifact/README.md)
- [CONFIG.md](artifact/CONFIG.md)
- [EXAMPLES.md](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with product-listing previews, HTML snippets, JSON API payloads, and concise status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses UK English by default; Shopify writes require user confirmation before upload or destructive actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
