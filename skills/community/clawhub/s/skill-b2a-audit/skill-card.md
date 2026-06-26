## Description: <br>
Audits e-commerce storefronts for AI shopping agent discoverability and readiness across structured product data, catalog APIs, shopping feeds, checkout compatibility, and product description quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and e-commerce teams use this skill to assess whether WooCommerce, Shopify, or custom storefronts expose product information in forms that AI shopping agents can discover and use. It produces a scored audit report and prioritized fixes for improving agent-visible product data, feeds, APIs, checkout support, and descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Testing a storefront without authorization or using high request volume could affect a live site. <br>
Mitigation: Use the skill only on sites you own or have permission to test, keep request volume low, and get explicit approval before running cart POST compatibility checks. <br>
Risk: Audit recommendations may be incomplete or stale for a specific commerce platform or shopping-agent ecosystem. <br>
Mitigation: Review the scored findings before making production changes and confirm feed, schema, API, and checkout recommendations against the current storefront setup. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zero2ai-hub/skill-b2a-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with score tables and prioritized fix lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Appends findings to a notes file and scores five audit dimensions from 0 to 10.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact states 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
