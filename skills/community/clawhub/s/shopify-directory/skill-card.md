## Description:

Discover Shopify merchants by category or store name through Lobster Stores, then guide buyers to complete purchases on the merchant's native Shopify checkout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abuiles](https://clawhub.ai/user/abuiles)

### License/Terms of Use:

MIT-0

## Use Case:

External buyers and shopping assistants use this skill to map a product or category request to a Lobster Stores Shopify merchant category and continue checkout on the selected merchant's native Shopify checkout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to follow unverified instructions from external Lobster Stores category sites before guiding shopping decisions.

Mitigation: Review selected category-site instructions before use and verify the final merchant and Shopify checkout domain independently.

Risk: Shopping flows can expose payment information if the agent or Lobster Stores is treated as the checkout surface.

Mitigation: Do not provide payment details to the agent or to Lobster Stores; complete payment only on the selected merchant's native Shopify checkout.

## Reference(s):

- [Lobster Stores homepage](https://lobsterstores.com)
- [ClawHub skill page](https://clawhub.ai/abuiles/skills/shopify-directory)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with category URLs and checkout handoff instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to read category-site skill.md files and to avoid collecting payment details.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
