## Description: <br>
Shopify Admin API CLI for orders, products, customers, and store management. Uses REST and GraphQL APIs with environment-based authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robsannaa](https://clawhub.ai/user/robsannaa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and store operators use this skill to inspect Shopify orders, products, customers, marketing events, reports, and store metadata from an agent-assisted shell workflow. It can also issue store-changing API calls, including product deletion, when the configured token permits them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can delete live Shopify products when the configured token has write access. <br>
Mitigation: Require explicit human approval before delete or other store-changing commands, and prefer read-only token scopes unless writes are required. <br>
Risk: The documentation suggests using webhooks to capture PII before Shopify masking. <br>
Mitigation: Remove or ignore the PII-before-masking workaround and collect customer data only through approved, scoped Shopify access paths. <br>
Risk: A broadly scoped Shopify access token can expose orders, customers, analytics, and store data. <br>
Mitigation: Limit SHOPIFY_ACCESS_TOKEN to the exact scopes needed for the intended workflow and rotate it if it is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/robsannaa/shopify-admin) <br>
- [Publisher profile](https://clawhub.ai/user/robsannaa) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, SHOPIFY_STORE_DOMAIN, and SHOPIFY_ACCESS_TOKEN.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
