## Description: <br>
Audits Shopify and WooCommerce product listings against a 10-criterion SEO rubric, reports weak listings, exports scores, and can propose or apply listing improvements after confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hussainpatan9](https://clawhub.ai/user/hussainpatan9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce operators and agencies use this skill to audit Shopify or WooCommerce product SEO, identify priority fixes, generate UK English rewrites, and optionally update product listings after reviewing previews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide live Shopify or WooCommerce credentials in chat. <br>
Mitigation: Use least-privilege credentials, prefer read-only access for audits, add write permissions only when applying approved fixes, and rotate any credentials pasted into chat. <br>
Risk: The skill can make bulk changes to production product listings. <br>
Mitigation: Review each before-and-after preview carefully, require explicit confirmation before writes, and start with small batches or a read-only audit before bulk updates. <br>
Risk: Generated titles, descriptions, tags, or SEO metadata may be inaccurate for a product. <br>
Mitigation: Verify proposed content against the product details and store policy before approving updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hussainpatan9/seo-product-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/hussainpatan9) <br>
- [README.md](artifact/README.md) <br>
- [CONFIG.md](artifact/CONFIG.md) <br>
- [EXAMPLES.md](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, before-and-after previews, CSV exports, API request examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can store audit and fix results in agent memory; can generate workspace CSV files for audit exports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
