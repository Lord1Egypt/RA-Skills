## Description:

Researches public rental communities, NYC housing listings, and market series through Crawlora's StreetEasy and Greystar data to build rental shortlists and compare advertised offers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Renters and housing researchers use this skill to shortlist public rental listings and communities, compare advertised prices and terms, and place NYC asking prices in dated market context.

### Deployment Geography for Use:

Global use; listing coverage is NYC-area StreetEasy results and published Greystar markets.

## Known Risks and Mitigations:

Risk: Housing search terms, budgets, locations, and the API key are sent to Crawlora.

Mitigation: Inform users before use and share only the search details needed for the request.

Risk: Advertised prices, fees, and availability may be incomplete or change after collection.

Mitigation: Show price bases, unknown costs, source links, and collection times; confirm current terms directly.

Risk: A research shortlist could be mistaken for a decision to apply, pay, or contact a landlord.

Mitigation: Keep rental decisions, applications, payments, and landlord contact under direct user control.

## Reference(s):

- [Rental housing research endpoint reference](reference/endpoints.md)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/rental-housing-research)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown rental shortlist and market comparison]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes price basis, source links, collection times, and unresolved costs or availability.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
