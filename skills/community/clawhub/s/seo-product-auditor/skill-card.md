## Description:

Scans Shopify or WooCommerce product listings, scores product SEO against a 10-criterion rubric, prioritizes weak listings, and can propose or apply UK English rewrites after confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hussainpatan9](https://clawhub.ai/user/hussainpatan9)

### License/Terms of Use:

MIT-0

## Use Case:

External store operators, ecommerce teams, and developers use this skill to audit product listing SEO across Shopify or WooCommerce, identify low-scoring products, export reports, and generate reviewed fixes for titles, descriptions, tags, metadata, and image alt text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for store API credentials and can read or update live product listings.

Mitigation: Use least-privilege credentials, prefer read-only access for audits, avoid pasting live admin secrets into chat when possible, and verify required Shopify scopes before use.

Risk: Bulk fixes can change many product titles, descriptions, tags, metadata fields, or image alt text.

Mitigation: Review product IDs, changed fields, and before/after previews before approving any bulk update.

Risk: Generated SEO copy or inferred keywords may be inaccurate for a product.

Mitigation: Confirm suggested rewrites against the product details and do not apply changes when specifications are missing or uncertain.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hussainpatan9/skills/seo-product-auditor)
- [README](artifact/README.md)
- [Setup guide](artifact/CONFIG.md)
- [Examples](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, CSV exports, JSON-like memory records, API request examples, and before/after change previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Shopify or WooCommerce update proposals and product audit files; writes should require explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
