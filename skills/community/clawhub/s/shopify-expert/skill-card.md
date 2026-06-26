## Description: <br>
Provides OpenClaw agents with structured Shopify development guidance and bundled reference excerpts across apps, APIs, CLI, themes, extensions, webhooks, metafields, Liquid, Hydrogen/headless storefronts, and deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realm1lf](https://clawhub.ai/user/realm1lf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to help OpenClaw agents navigate Shopify development tasks, select the smallest relevant bundled reference, and draft implementation guidance or API examples. It is useful for Shopify apps, Admin and Storefront APIs, extensions, webhooks, themes, Liquid, Hydrogen/headless storefronts, and deployment planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopify Admin API operations can alter orders, products, inventory, refunds, customer data, and other production resources. <br>
Mitigation: Use least-privilege tokens, prefer a dev store for testing, and require explicit human approval before refunds, deletes, inventory changes, customer-data access, or bulk mutations. <br>
Risk: Bundled Shopify documentation is a point-in-time reference and may not match the current API version or supported payload shape. <br>
Mitigation: Verify current Shopify API documentation and the target shop's supported API version before production changes. <br>
Risk: Shopify credentials and customer or order data are sensitive. <br>
Mitigation: Store tokens in environment variables or secret stores, never paste secrets into chat, and use only apps the merchant explicitly authorized. <br>
Risk: Shopify API calls are rate limited. <br>
Mitigation: Use pagination, backoff, and bounded request loops for live API interactions. <br>


## Reference(s): <br>
- [Shopify Developer Documentation](https://shopify.dev/) <br>
- [Shopify Expert ClawHub Listing](https://clawhub.ai/realm1lf/shopify-expert) <br>
- [Overview](references/OVERVIEW.md) <br>
- [Official Sources and Shopify Versions](references/SOURCES_AND_VERSIONS.md) <br>
- [Authentication and Secrets](references/AUTH.md) <br>
- [Safety](references/SAFETY.md) <br>
- [Admin REST API](references/ADMIN_REST_API.md) <br>
- [GraphQL Admin API](references/DOC_ADMIN_API.md) <br>
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, configuration snippets, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference SHOPIFY_SHOP_DOMAIN, optional curl, and Shopify API tokens without echoing secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata; packaged bundle metadata reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
