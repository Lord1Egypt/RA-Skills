## Description:

TikTok Shop influencer analytics, product selection, and content strategy toolkit. Fetches creator data via EchoTik API, optionally fetches product trending data via TikTok Shop Partner API, then generates multi-region analysis reports, influencer collaboration plans, prioritized product selection lists, and video hook strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skovely](https://clawhub.ai/user/skovely)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and analysts use this skill to fetch TikTok Shop creator and product data, compare markets, plan influencer collaborations, prioritize product selections, and draft video hook strategies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses user-provided EchoTik credentials and optional TikTok Shop credentials to call external APIs.

Mitigation: Install only when those credentials are appropriate for the intended TikTok Shop analytics task, scope credentials to the minimum needed, and rotate or revoke them if no longer needed.

Risk: Generated reports may save business-relevant creator, product, sales, and market data locally.

Mitigation: Review output files before sharing, store them in approved locations, and avoid including confidential data in generic recommendation workflows.

Risk: Analytics and recommendations depend on external API responses and may be incomplete, stale, or unavailable by region or permission level.

Mitigation: Review generated reports before business use and validate important decisions against current marketplace data and platform policy.

## Reference(s):

- [Workflow Guides](references/workflows.md)
- [API Reference](references/api_docs.md)
- [Output Format Examples](references/output_example.md)
- [EchoTik](https://www.echotik.com/)
- [EchoTik Influencer API Endpoint](https://open.echotik.live/api/v3/echotik/influencer/list)
- [TikTok Shop Product Search Endpoint](https://api.tiktokshop.com/v2/products/search)
- [TikTok Shop OAuth Endpoint](https://auth.tiktokshop.com/api/v2/oauth/token)
- [TikTok Shop Seller Center](https://seller.tiktokglobalshop.com/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, API calls, Analysis, Markdown, JSON, Code]

**Output Format:** [Markdown guidance with shell commands, plus generated JSON or Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local reports for influencer data, product data, regional comparisons, collaboration plans, product selection lists, and video hook strategies.]

## Skill Version(s):

1.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
