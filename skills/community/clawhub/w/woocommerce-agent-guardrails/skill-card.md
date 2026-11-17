## Description:

Safety guardrails for AI agents that write to live WooCommerce stores, requiring risk tiering, dry-run previews, explicit approvals, failure circuit breakers, and prompt-injection handling before risky product, price, inventory, order, coupon, or customer-data changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arbazex](https://clawhub.ai/user/arbazex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, store operators, and automation agents use this skill to reduce the risk of unsafe WooCommerce write operations on live stores. It is intended for tasks that create, update, delete, or bulk-modify products, prices, inventory, orders, coupons, settings, exports, or customer data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents with WooCommerce write access can make public, costly, or irreversible store changes if risky actions proceed without review.

Mitigation: Use this skill only with agents that may touch real WooCommerce stores and require explicit approval gates for price changes, bulk edits, deletes, exports, settings changes, and similar high-impact writes.

Risk: Imported or scraped store content can contain instruction-like text that attempts to redirect the agent during bulk processing.

Mitigation: Treat product descriptions, reviews, customer notes, supplier feeds, and scraped pages as data rather than instructions; flag suspicious rows or fields before acting on them.

Risk: Repeated write failures can hide schema, authentication, rate-limit, or targeting problems while partial changes continue to accumulate.

Mitigation: Stop the operation after three consecutive write failures and report which items succeeded, failed, or remain untouched.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/arbazex/woocommerce-agent-guardrails)
- [ClawHub skill page](https://clawhub.ai/arbazex/skills/woocommerce-agent-guardrails)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown guidance with checklists, approval prompts, preview-table expectations, and operational rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Risk-tiered WooCommerce operating guidance covering approval gates, batching caps, failure circuit breaker behavior, kill-switch handling, and prompt-injection defense for imported or scraped store content.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
