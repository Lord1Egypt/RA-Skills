## Description:

Compares movie, show, season, and episode viewing offers across countries and providers using Crawlora JustWatch, distinguishing offer types and noting missing availability details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

People comparing where to watch specific titles use this skill to assemble country-by-provider offer matrices and shortlists that distinguish subscription, rental, purchase, free, and ad-supported options.

### Deployment Geography for Use:

Global; available viewing offers vary by country.

## Known Risks and Mitigations:

Risk: Title and search parameters, together with a Crawlora API key, are sent to Crawlora's API.

Mitigation: Use a key scoped to Crawlora and avoid submitting sensitive search terms.

Risk: Queries can consume API credits, and results may omit offers or specific plan conditions.

Mitigation: Set country, language, provider, and call limits; check credit usage and label unknown conditions rather than claiming complete availability.

## Reference(s):

- [Streaming availability endpoint reference](reference/endpoints.md)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/streaming-availability-comparison)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown comparison matrix and practical shortlist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes offer basis, country, provider, price and currency when available, source and observation time, and missing-condition notes.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
