## Description:

Researches and compares public accommodation, flight, and activity listings across travel platforms using Crawlora without making bookings or payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Travel researchers and travelers compare public hotel and rental listings, check reviews and availability, and gather evidence for itineraries across supported platforms. The skill does not book travel or process payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel-search inputs and the Crawlora API key are sent to Crawlora.

Mitigation: Keep the key secret and avoid submitting payment data or unrelated personal information.

Risk: Prices, availability, reviews, and cancellation details may be incomplete or change after retrieval.

Mitigation: Preserve source, retrieval time, dates, occupancy, and currency; verify material booking decisions on the originating platform.

## Reference(s):

- [Travel accommodation endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/travel-accommodation-research)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Source-aware JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retains platform, dates, occupancy, currency, and retrieval time with comparisons.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
