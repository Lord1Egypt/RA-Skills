## Description:

Search Sephora product listings and retrieve prices, shades, stock, ingredients, and review summaries as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to search Sephora products, browse categories, and retrieve product details such as prices, shade availability, ingredients, and review sentiment.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Search terms and, when provided, a ZIP code may be transmitted to Scavio, a third-party service.

Mitigation: Avoid sensitive search terms and omit the ZIP parameter unless local delivery eligibility is needed.

Risk: The security scan was partial, so its benign verdict is not a guarantee of safety.

Mitigation: Treat the scan as preliminary and review the skill before installing it.

## Reference(s):

- [Scavio Sephora API overview](https://scavio.dev/sephora-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data)
- [Sephora search endpoint documentation](https://scavio.dev/docs/sephora-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data)
- [Sephora category endpoint documentation](https://scavio.dev/docs/sephora-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data)
- [Sephora product endpoint documentation](https://scavio.dev/docs/sephora-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=sephora-product-data)

## Skill Output:

**Output Type(s):** [Structured data]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by search or category request; product responses include shade and review details.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
