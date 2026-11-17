## Description:

Shop across millions of stores: find products or look for matching offers for items found elsewhere. Find nearby stores, build carts, and track your orders. Use the shop CLI to ask a store questions, check out with Shop Pay, track delivery, access Shop account data and spend permissions, and get buyer approval and payment credentials for purchases an agent makes using a browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shopify](https://clawhub.ai/user/shopify)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers use this skill to find and compare products, locate stores, ask merchants questions, and manage carts, checkouts, and Shop account or order information. It helps an agent present recommendations with their source details and follow the documented buyer approval steps for purchases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image searches may transmit a user's image to Shop without a clear disclosure.

Mitigation: Tell the user before sending an image and get confirmation; offer a text search when they prefer not to share an image.

Risk: The security scan was partial because some referenced paths were unresolved.

Mitigation: Review the unresolved references before relying on the scan's benign verdict.

## Reference(s):

- [Catalog reference](references/catalog.md)
- [CLI reference](references/cli.md)
- [Transactions reference](references/transactions.md)
- [Shop setup instructions](https://shop.com/SKILL.md)
- [Shop ClawHub release](https://clawhub.ai/shopify/skills/shop)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Conversational text or Markdown, with product links and optional CLI command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations retain returned seller, product, option, price, currency, and source-link details; purchase steps include buyer review and approval guidance.]

## Skill Version(s):

1.3.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
