## Description: <br>
Uploads and manages Shopify products individually, in bulk from CSV, or from images while generating UK English SEO content and confirming changes before Shopify Admin API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hussainpatan9](https://clawhub.ai/user/hussainpatan9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce operators and store teams use this skill to create, update, bulk upload, draft, archive, and manage inventory for Shopify listings through an agent interface. It is designed for workflows that need SEO-ready product copy, CSV mapping previews, image-to-listing support, and confirmation before store changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Shopify Admin API token can modify products, inventory, and collections if exposed or over-scoped. <br>
Mitigation: Use the narrowest Shopify scopes possible, store the token in a secrets vault or environment variable, avoid pasting it into chat, and rotate or revoke it when the skill is no longer needed. <br>
Risk: Bulk uploads, updates, archive actions, and permanent deletes can change many storefront listings. <br>
Mitigation: Use draft mode for review, inspect CSV mappings and generated previews, and require explicit confirmation before uploads, destructive actions, or permanent deletes. <br>
Risk: Generated SEO descriptions can introduce inaccurate claims for safety-relevant, food, supplement, or compliance-sensitive products. <br>
Mitigation: Review generated listing text before publishing and confirm compliance claims such as CE, UKCA, food-safe status, or health-related statements from authoritative product information. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/hussainpatan9/shopify-product-uploader) <br>
- [Setup guide](artifact/CONFIG.md) <br>
- [Few-shot examples](artifact/EXAMPLES.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown-style confirmations, HTML product descriptions, CSV and bulk upload summaries, and Shopify Admin API request payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Shopify Admin API token and explicit confirmation before uploads, updates, archive actions, or permanent deletes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
