## Description:

Analyzes observed used-car listing price changes using Crawlora's stored vehicle histories and selected live listings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Vehicle shoppers and analysts use this skill to compare dated asking-price changes across matched used-car listings, with listing identity and crawl coverage kept visible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exposure of the Crawlora API key during vehicle research.

Mitigation: Treat CRAWLORA_API_KEY as sensitive and do not include it in reports or shared commands.

Risk: Unintended requests or credit use outside the intended vehicle-history scope.

Mitigation: Limit requests to the intended listings, search area, and credit budget.

Risk: Incomplete or stale listing coverage may make an asking-price change seem more conclusive than it is.

Mitigation: Show observation and crawl dates, distinguish first-observed prices from original prices, and flag missing histories or unmatched listings.

Risk: Live listings may include seller or dealer details.

Mitigation: Share only details needed for the price comparison and handle listing data with care.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/used-car-price-history-analysis)
- [Crawlora endpoint reference](artifact/reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown with price-event ledger and comparable-listing table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes observation dates, coverage and freshness notes, and seller-verification questions.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
