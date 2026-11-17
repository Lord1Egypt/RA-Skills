## Description:

Guides agents in searching TikTok Shop products and prices, retrieving product details and reviews, browsing categories and seller catalogs, and resolving shop links through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and commerce researchers use this skill to guide agents in TikTok Shop price research, competitor catalog analysis, product discovery, and review analysis through Scavio's API.

### Deployment Geography for Use:

US, UK, Singapore, Malaysia, Philippines, Thailand, Vietnam, and Indonesia (availability varies by endpoint; product search is US-only)

## Known Risks and Mitigations:

Risk: API keys and submitted queries or URLs are sent to Scavio.

Mitigation: Use an authorized API key and avoid sharing sensitive private text in queries or URLs unless acceptable to the user.

Risk: Each API request consumes credits, including product-detail requests that return 404.

Mitigation: Confirm the expected cost before bulk pagination or detail lookups, and avoid retrying known unavailable product details.

## Reference(s):

- [Scavio TikTok Shop API documentation](https://scavio.dev/docs/tiktok-shop-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=tiktok-shop-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=tiktok-shop-api)
- [ClawHub skill release](https://clawhub.ai/scavio-ai/skills/tiktok-shop-api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Text]

**Output Format:** [Markdown with API request examples and structured JSON response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Scavio API key; each endpoint call consumes one credit.]

## Skill Version(s):

1.0.4 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
