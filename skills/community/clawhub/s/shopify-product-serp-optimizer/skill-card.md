## Description:

Audit and improve Shopify product SERP performance for product pages using five-product batches, evidence-backed metadata recommendations, product image alt-text checks, HTML reports, and approval-gated write bundles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvsao](https://clawhub.ai/user/lvsao)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, ecommerce operators, and agents use this skill to audit Shopify product pages, generate HTML SERP reports, and prepare approval-gated updates to product titles, descriptions, SEO metadata, and product image alt text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require broad Shopify write scopes for connected updates.

Mitigation: Prefer public storefront or read-only access for audits, and grant write scopes only when applying a reviewed change bundle.

Risk: Private Shopify client secrets or automation tokens could be exposed if placed in chat, logs, or tracked files.

Mitigation: Store credentials only in private local configuration, verify skill-hub.env is ignored by Git, and avoid pasting secrets into chat.

Risk: The skill can update itself before use, which may change behavior before review.

Mitigation: Review and scan any new version before allowing it to run against a production store.

Risk: Approved write bundles can change Shopify product titles, descriptions, SEO fields, and product image alt text.

Mitigation: Use preview first, require explicit approval before execution, and keep public storefront mode report-only.

## Reference(s):

- [Product SERP Methodology](artifact/references/serp-methodology.md)
- [Product Media Alt Text Rules](artifact/references/alt-text-rules.md)
- [Public Data Extraction - No-API Mode](artifact/references/public-data-extraction.md)
- [Connect Your Store](artifact/references/onboarding-guide.md)
- [Project homepage](https://github.com/lvsao/shopify-skill-hub)
- [ClawHub skill page](https://clawhub.ai/lvsao/skills/shopify-product-serp-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, html files]

**Output Format:** [Markdown guidance, JSON command output, and single-file HTML audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can prepare Shopify write bundles for preview and explicit approval before execution; public storefront mode is report-only.]

## Skill Version(s):

2.1.2 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
