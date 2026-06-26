## Description: <br>
Manage Shopify products, orders, customers, inventory, collections, and store operations via the Shopify Admin API with OAuth authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Shopify store operators and developers use this skill to inspect and manage store data, including products, orders, customers, inventory, collections, fulfillment, discounts, webhooks, and billing through authenticated Shopify Admin API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses stored OAuth credentials to call the Shopify Admin API for the connected store. <br>
Mitigation: Install only when the user is comfortable connecting a Shopify store through ClawLink, and verify the active Shopify integration before making tool calls. <br>
Risk: Write operations can change store data, including products, inventory, customers, orders, refunds, webhooks, and billing charges. <br>
Mitigation: Describe and preview write operations first, then execute only after the user explicitly confirms the target resource and intended effect. <br>
Risk: Destructive or bulk operations, such as product deletion, customer address deletion, refunds, cancellations, and bulk mutations, can be difficult or impossible to undo. <br>
Mitigation: Prefer read, list, search, and count operations to reduce ambiguity, verify target IDs before execution, and use dedicated preview or calculation tools such as refund calculation before committing changes. <br>


## Reference(s): <br>
- [ClawHub Shopify Skill Page](https://clawhub.ai/hith3sh/shopify-commerce) <br>
- [Shopify Admin API](https://shopify.dev/docs/api/admin) <br>
- [Shopify REST Admin API Reference](https://shopify.dev/docs/api/admin-rest) <br>
- [Shopify GraphQL Admin API](https://shopify.dev/docs/api/admin-graphql) <br>
- [Shopify OAuth Documentation](https://shopify.dev/docs/apps/auth/oauth) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected Shopify store through ClawLink OAuth before Shopify Admin API calls can run.] <br>

## Skill Version(s): <br>
0.1.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
