## Description: <br>
Provides Shopify Admin REST API guidance and request examples for managing orders, products, variants, customers, inventory, fulfillments, refunds, returns, transactions, collections, abandoned checkouts, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zachgodsell93](https://clawhub.ai/user/zachgodsell93) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and store operators use this skill to guide Shopify Admin REST API setup and generate request patterns for live store administration. It is suited for workflows that need help reading or changing orders, products, customers, inventory, fulfillments, refunds, returns, transactions, collections, checkouts, or webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad live-store read and write access can affect orders, products, customers, inventory, fulfillments, refunds, returns, transactions, and webhooks. <br>
Mitigation: Use a dedicated Shopify custom app token with the minimum required scopes and require manual approval before destructive or money-moving actions. <br>
Risk: The read_all_orders scope can expose older order history and should not be granted by default. <br>
Mitigation: Avoid read_all_orders unless the workflow explicitly requires access to orders older than 60 days and the store owner has approved that access. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Shopify store domain and Admin API access token environment variables supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
