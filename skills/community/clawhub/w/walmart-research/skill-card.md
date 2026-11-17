## Description:

Researches Walmart products, prices, sellers, and reviews through the Crawlora API and returns structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers and researchers use this skill to find Walmart listings, compare prices and availability, and summarize product reviews using Crawlora's API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, Walmart item IDs, and the API key are sent to Crawlora.

Mitigation: Use only if sharing these inputs with Crawlora is acceptable, and limit requests to the documented Walmart endpoints.

Risk: Hardcoding or committing the API key can expose it.

Mitigation: Keep the key in CRAWLORA_API_KEY; never hardcode or commit it.

## Reference(s):

- [Walmart endpoint reference](artifact/reference/endpoints.md)
- [Walmart Research on ClawHub](https://clawhub.ai/crawlora-org/skills/walmart-research)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Markdown summaries or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are paginated; reviews are an on-page snapshot, not a full feed.]

## Skill Version(s):

1.0.18 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
