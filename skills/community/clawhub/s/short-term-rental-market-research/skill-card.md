## Description:

Compare short-term rental market supply, listing density, room mix, price distributions, and review signals using Crawlora Airbnb aggregates and selected live listings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and researchers compare short-term rental markets using aggregate supply, density, prices, and review signals, with separately labeled examples of live listings. Results support further research rather than occupancy, revenue, or investment forecasts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market queries and the Crawlora API key are sent to Crawlora.

Mitigation: Use only when this data sharing is acceptable; keep the key in the environment and bound queries to the intended markets and credit budget.

Risk: Sparse, suppressed, or sampled data could be mistaken for complete market evidence or used to infer occupancy or revenue.

Mitigation: Preserve freshness, coverage and suppression notes; label live examples as samples and avoid inferring bookings, revenue, or suppressed listing details.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/short-term-rental-market-research)
- [Crawlora publisher profile](https://clawhub.ai/user/crawlora-org)
- [Crawlora](https://crawlora.net)
- [Endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown market comparison]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports geography, filters, collection dates, coverage and suppression limits; presents sampled live listings separately.]

## Skill Version(s):

1.0.10 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
