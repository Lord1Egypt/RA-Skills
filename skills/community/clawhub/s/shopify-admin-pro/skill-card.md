## Description:

Helps Shopify store administrators audit store data and make confirmed changes to products, inventory, orders, customers, and storefront content through the Admin GraphQL API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[artificialintelligently](https://clawhub.ai/user/artificialintelligently)

### License/Terms of Use:

MIT

## Use Case:

Shopify store administrators and their agents use this skill to audit operations and prepare, approve, and verify individual store changes, including catalog updates, fulfillment, and refunds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write access can alter store data or trigger refunds, cancellations, and publishing.

Mitigation: Start with read-only scopes; grant write scopes only for the task, review previews, and explicitly confirm each change, with a second exact confirmation for high-risk actions.

Risk: The skill's confirmed writes have not yet been exercised against a live store.

Mitigation: Try the first low-risk writes on a development store and verify the resulting store state before wider use.

Risk: Admin access exposes credentials and customer data.

Mitigation: Keep secrets out of chat, use only the store's authorized credentials, and redact personal data in reports unless the task requires it.

## Reference(s):

- [Shopify Admin Pro on ClawHub](https://clawhub.ai/artificialintelligently/skills/shopify-admin-pro)
- [Shopify GraphQL cookbook](artifact/references/graphql-cookbook.md)
- [Safety, scopes, and data handling](artifact/references/safety-and-scopes.md)
- [Shopify Admin Pro workflows](artifact/references/workflows.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown reports, previews, and Shopify helper commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write proposals require explicit per-change approval; high-risk actions require an additional exact confirmation.]

## Skill Version(s):

1.0.1 (source: server-resolved release and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
