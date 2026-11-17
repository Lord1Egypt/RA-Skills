## Description:

Query Zara catalog data across markets, including product details, prices, promotions, availability, stores, categories, and new arrivals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and shopping assistants use the skill to retrieve Zara product and pricing information across markets, check online or store availability, and find stores or catalog listings. It can also support price tracking when the caller stores repeated readings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Store searches can send location coordinates to Scavio.

Mitigation: Use location-based store lookups only when sharing the location is appropriate; use previously obtained store IDs for store-stock requests when possible.

## Reference(s):

- [Scavio Zara API documentation](https://scavio.dev/docs/zara-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=zara-api)

## Skill Output:

**Output Type(s):** [JSON, Text, Analysis]

**Output Format:** [Structured JSON data with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live catalog results; prices remain in each market's currency and are not automatically converted.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
