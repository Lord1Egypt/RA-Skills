## Description:

Safely inspect a Shopify store's cart-to-checkout path, destination-specific delivery choices, visible payment methods, payment setup, and aggregated payment signals without placing an order, submitting payment details, or changing store data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvsao](https://clawhub.ai/user/lvsao)

### License/Terms of Use:

MIT-0

## Use Case:

Shopify merchants and their support or operations agents use this skill to check checkout reachability, delivery options, visible payment methods, payment setup, and aggregate payment signals. It produces a plain-language report with observed limitations and prioritized fixes while staying within a read-only Admin and safe storefront walkthrough boundary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An optional CLI JavaScript path can execute arbitrary local code if pointed at an untrusted file.

Mitigation: Only set SKILL_HUB_SHOPIFY_CLI_JS to a verified Shopify CLI file controlled by the operator.

Risk: The private env file can contain Shopify client secrets or automation tokens and is not forced to owner-only permissions by the evidence.

Mitigation: Keep skill-hub.env outside the skill folder and Git, restrict its permissions, and store secrets only in trusted local or server configuration.

Risk: Checkout and payment observations can be over-read as proof that a live charge will succeed.

Mitigation: Report visible payment methods and reachable handoffs only as observations, and require a separate merchant-authorized real-payment test before claiming payment completion works.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lvsao/skills/shopify-checkout-payment-connection-check)
- [ClawHub Publisher Profile](https://clawhub.ai/user/lvsao)
- [Project Homepage](https://github.com/lvsao/shopify-skill-hub)
- [Connect Your Store](references/onboarding-guide.md)
- [API surfaces and interpretation](references/api-surfaces.md)
- [ShopifyPaymentsAccount](https://shopify.dev/docs/api/admin-graphql/2026-07/objects/ShopifyPaymentsAccount)
- [OrderTransaction](https://shopify.dev/docs/api/admin-graphql/2026-07/objects/OrderTransaction)
- [deliveryProfiles](https://shopify.dev/docs/api/admin-graphql/2026-07/queries/deliveryProfiles)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with inline shell commands and redacted JSON evidence references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should keep browser observations, Admin evidence, unknowns, limitations, and prioritized fixes separate.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
