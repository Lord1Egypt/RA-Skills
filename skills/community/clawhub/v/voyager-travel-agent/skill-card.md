## Description:

Alipay+ Voyager Travel Agent provides travel assistance for flight search, hotel recommendations, and multi-day itinerary planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voyageragent](https://clawhub.ai/user/voyageragent)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to search travel options, compare flight and hotel results, and assemble practical day-by-day itineraries from stated destinations, dates, budgets, interests, and constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel search details such as dates, cities, and search terms are sent to Alipay+ travel service endpoints.

Mitigation: Use the skill only when sharing those details with Alipay+ services is acceptable, and avoid entering unnecessary sensitive personal information.

Risk: Hotel searches may silently default missing dates and infer nearby points of interest.

Mitigation: Confirm check-in and check-out dates, destination area, and hotel location assumptions before relying on recommendations or booking links.

Risk: Flight and hotel availability, price, currency, and booking links can change or be incomplete.

Mitigation: Verify dates, currency, destination, availability, and booking links directly before purchase or travel decisions.

Risk: The flight search script has JSON input handling that should be hardened.

Mitigation: Review and harden shell argument serialization before using the script with untrusted or complex input.

## Reference(s):

- [Plan Itinerary](references/plan-itinerary.md)
- [Search Flights](references/search-flights.md)
- [Search Hotels](references/search-hotels.md)
- [Voyager Travel Agent on ClawHub](https://clawhub.ai/voyageragent/skills/voyager-travel-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown travel recommendations, comparison tables, itinerary plans, and shell command invocations for travel search scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hotel results may include names, prices, ratings, images, and booking links when available; flight recommendations are limited to returned search data.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
