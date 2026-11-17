## Description:

Manage Shopify store data including orders, products, variants, customers, inventory, fulfillments, refunds, returns, transactions, collections, abandoned checkouts, and webhooks via the Shopify Admin REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zachgodsell93](https://clawhub.ai/user/zachgodsell93)

### License/Terms of Use:


## Use Case:

Developers and store operators use this skill to have an agent draft Shopify Admin REST API requests for store management workflows, including catalog changes, customer records, fulfillment, refunds, returns, payments, inventory, and webhook operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives agents broad Shopify Admin API authority, including store-changing and money-moving examples.

Mitigation: Use the narrowest Shopify scopes possible and require explicit human approval before deletes, cancellations, inventory replacement, refunds, transaction captures, webhook changes, or customer notifications.

Risk: Token-bearing requests could be sent to an unintended or untrusted store domain.

Mitigation: Validate the Shopify store domain before any request that includes the Admin API access token.

Risk: The Admin API access token can authorize sensitive store operations if exposed.

Mitigation: Keep the access token in a secrets manager and avoid exposing it in logs, prompts, or generated artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zachgodsell93/skills/shopify-admin-api)
- [Skill source artifact](artifact/skill.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with curl command examples, JSON request bodies, setup notes, and API reference guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Shopify store domain and Admin API access token; generated requests may read or modify store data.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact frontmatter, artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
