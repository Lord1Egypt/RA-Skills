## Description:

Searches and compares live travel options across flights, hotels, Airbnb-style stays, car rentals, ferries, and destination information so agents can recommend best-value itineraries with prices and booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adrianetti](https://clawhub.ai/user/adrianetti)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to find, compare, and present travel options across providers, including flights, lodging, cars, ferries, multi-city routes, and destination intel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel searches are sent to named third-party travel providers.

Mitigation: Share only trip details needed for the search and avoid unnecessary sensitive personal information.

Risk: Optional local integrations may require npm or pip packages.

Mitigation: Pin package versions and run optional integrations in a sandboxed environment before using them with real travel queries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adrianetti/skills/travel-search)
- [Kiwi.com Flight Search](references/flights.md)
- [Skiplagged Flights, Hotels, and Car Rentals](references/skiplagged.md)
- [Trivago Hotel and Accommodation Search](references/hotels.md)
- [Ferryhopper Ferry Search](references/ferries.md)
- [Google Flights via fli](references/google-flights.md)
- [Airbnb Short-Stay and Apartment Search](references/airbnb.md)
- [Smart Price Deal Comparison](references/price-tools.md)
- [Trip Planner Itinerary Generator](references/trip-planner.md)
- [Multi-City Route Optimizer](references/multi-city.md)
- [Travel Intel Destination Intelligence](references/travel-intel.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with travel recommendations, inline shell commands, JSON examples, prices, and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live results depend on third-party travel-provider availability and user-provided trip details.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
