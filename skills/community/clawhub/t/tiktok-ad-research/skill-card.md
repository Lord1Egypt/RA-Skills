## Description:

Research TikTok Creative Center Top Ads by brand, market, industry, and objective through Crawlora.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and agencies use this skill to compare public TikTok Top Ads across brands and markets, identify creative patterns, and develop testable advertising briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ad-research queries and the API key are sent to Crawlora; shared logs could expose requests or responses.

Mitigation: Use a secret store or environment variable for CRAWLORA_API_KEY and avoid sharing request and response logs.

Risk: Selected public Top Ads and performance charts can be mistaken for complete campaign coverage or proof of spend and causation.

Mitigation: State the filters and sample limits, verify advertiser matches, and frame creative recommendations as hypotheses rather than performance claims.

## Reference(s):

- [TikTok Top Ads endpoint reference](reference/endpoints.md)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/tiktok-ad-research)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown comparison with linked ad examples and creative-test hypotheses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source links, material IDs, comparison filters, reported metrics, and retrieval time when available.]

## Skill Version(s):

1.0.11 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
