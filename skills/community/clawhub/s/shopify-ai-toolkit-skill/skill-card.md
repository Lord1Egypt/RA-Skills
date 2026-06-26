## Description: <br>
Search Shopify developer docs and validate GraphQL, Liquid, Hydrogen, and other Shopify code for app, theme, or storefront development tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jtcchan](https://clawhub.ai/user/jtcchan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to build Shopify apps, themes, storefronts, functions, and integrations with a search, code, validate workflow against Shopify documentation and validators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, validation results, and raw code or file context may be sent to Shopify-operated endpoints by default. <br>
Mitigation: Set OPT_OUT_INSTRUMENTATION=true for private or regulated work, avoid submitting secrets or customer data, and review endpoint behavior before deployment. <br>
Risk: Some GraphQL validators may reference missing schema asset files in this package. <br>
Mitigation: Treat validator failures as review signals and manually verify generated GraphQL against Shopify documentation before using it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jtcchan/shopify-ai-toolkit-skill) <br>
- [Shopify developer documentation](https://shopify.dev/) <br>
- [Shopify Admin GraphQL API](https://shopify.dev/docs/api/admin-graphql) <br>
- [Shopify Storefront API](https://shopify.dev/docs/api/storefront) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and validation workflows may call Shopify-operated endpoints unless telemetry is disabled.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
