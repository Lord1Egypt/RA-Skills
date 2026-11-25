## Description:

Retrieves Staples US and Canada product and search data, including pricing, promotions, store stock, reviews, coupons, and store information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to look up Staples US and Canada products, prices, promotions, and related shopping information. It supports ink and paper price checks, pickup-stock lookups near a US ZIP code, and searches by keyword, model number, or item number.

### Deployment Geography for Use:

United States and Canada (Staples Canada product and top search results only)

## Known Risks and Mitigations:

Risk: Requests send query details and an API key to api.scavio.dev.

Mitigation: Use the service only if comfortable sharing those details, and keep SCAVIO_API_KEY in a protected environment variable rather than exposing it in chat or logs.

## Reference(s):

- [Staples API overview](https://scavio.dev/staples-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=staples-ink-prices-api)
- [Staples product API documentation](https://scavio.dev/docs/staples-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=staples-ink-prices-api)
- [Staples search API documentation](https://scavio.dev/docs/staples-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=staples-ink-prices-api)
- [Staples store stock API documentation](https://scavio.dev/docs/staples-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=staples-ink-prices-api)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured JSON responses with concise explanatory guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One response per API call; 12 endpoints, 1 credit per call.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
