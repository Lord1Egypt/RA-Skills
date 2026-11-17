## Description:

Helps agents research Shop.app products, variants, merchants, and reviews through Crawlora's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers, researchers, and agents use this skill to compare Shop.app products and prices, inspect variants and availability, and review merchants or customer feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product or shop queries and public identifiers are sent to Crawlora, a third-party API.

Mitigation: Use public search terms and avoid sending secrets or unrelated personal data.

Risk: The Crawlora API key could be exposed if shared in prompts or saved in files.

Mitigation: Set CRAWLORA_API_KEY in the environment; do not paste or commit the key.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/shop-app-research)
- [Shop.app endpoint reference](artifact/reference/endpoints.md)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Concise research summaries based on structured product, shop, and review data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source API responses are JSON; result counts are limited by endpoint.]

## Skill Version(s):

1.0.17 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
