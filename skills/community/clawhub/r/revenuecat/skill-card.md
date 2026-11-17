## Description:

RevenueCat metrics, customer data, and documentation search. Use when querying subscription analytics, MRR, churn, customers, or RevenueCat docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeiting](https://clawhub.ai/user/jeiting)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to query RevenueCat subscription metrics, customers, products, purchases, and project documentation through local API references and a curl-based API helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is primarily read-oriented but includes reference coverage for sensitive RevenueCat admin actions such as refunds, cancellations, deletes, and webhook changes.

Mitigation: Use a least-privilege or read-only RevenueCat API key where possible, and require explicit confirmation before using credentials that can perform admin actions.

Risk: RevenueCat API credentials may expose project customer, subscription, and revenue data according to the key's permissions.

Mitigation: Keep RC_API_KEY out of shared logs and prompts, rotate it if exposed, and scope it to the minimum RevenueCat project and permissions needed.

## Reference(s):

- [RevenueCat skill page](https://clawhub.ai/jeiting/skills/revenuecat)
- [RevenueCat documentation](https://www.revenuecat.com/docs)
- [RevenueCat documentation index](https://www.revenuecat.com/docs/llms.txt)
- [RevenueCat Developer API v2 Reference](references/api-v2.md)
- [Audit Log](references/audit-logs.md)
- [Chart Dashboard Links](references/chart-links.md)
- [Customer](references/customers.md)
- [Entitlement](references/entitlements.md)
- [Error Handling](references/error-handling.md)
- [Integration](references/integrations.md)
- [Charts & Metrics](references/metrics.md)
- [Offering](references/offerings.md)
- [Paywall](references/paywalls.md)
- [Product](references/products.md)
- [Project](references/projects.md)
- [Purchase](references/purchases.md)
- [Rate Limits](references/rate-limits.md)
- [Subscription](references/subscriptions.md)
- [Virtual Currency](references/virtual-currencies.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses when commands are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and RC_API_KEY; RevenueCat API key permissions determine accessible projects and actions.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
