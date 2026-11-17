## Description:

Researches hotels, flights, attractions, short-term rentals, and live events through Crawlora and returns structured travel data for comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to compare stays and flights, check public reviews and attractions, and research rentals or events before making plans. It does not book or pay for travel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel searches, dates, locations, listing IDs, review queries, and the API key are sent to Crawlora.

Mitigation: Use only necessary travel details, avoid sensitive personal information, and keep the API key in the environment rather than sharing or committing it.

Risk: The endpoint catalog includes additional travel and event providers beyond the short description.

Mitigation: Review the requested provider and endpoint before sending a query.

Risk: Expedia POST request-body fields are unconfirmed, so those searches may fail or return unexpected results.

Mitigation: Confirm the current body format in Crawlora documentation before relying on Expedia results.

## Reference(s):

- [Travel API endpoint reference](reference/endpoints.md)
- [Crawlora API documentation](https://crawlora.net/docs)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/travel-hotel-research)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON API results and human-readable travel comparisons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public travel-search results; rates and availability should be checked before booking.]

## Skill Version(s):

1.0.20 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
