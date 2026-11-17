## Description:

Researches Wish categories, products, related items, and reviews through the Crawlora API to help agents compare marketplace listings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers and research agents use this skill to browse Wish categories, find and compare products, and inspect product details, related items, and reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wish search terms, product IDs, and the API key are sent to Crawlora.

Mitigation: Avoid sensitive searches unless that disclosure is acceptable; store the key in CRAWLORA_API_KEY and never hardcode or commit it.

## Reference(s):

- [Wish research endpoint reference](reference/endpoints.md)
- [Wish research on ClawHub](https://clawhub.ai/crawlora-org/skills/wish-research)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON from the API, with concise text summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes product prices, ratings, merchant details, related items, or reviews depending on the request.]

## Skill Version(s):

1.0.16 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
