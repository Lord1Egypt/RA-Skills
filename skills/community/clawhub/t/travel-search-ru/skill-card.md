## Description:

Use while planning a trip when Russian-catalog search is needed: package tours, hotels, flights, trains, excursions, prices, and booking links. Trigger on Russian requests: «спланировать путешествие», «подобрать тур», «найти отель/авиабилеты/жд билеты/экскурсии», «маршрут с актуальными ценами». Not for general advice without live search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[missial](https://clawhub.ai/user/missial)

### License/Terms of Use:

MIT

## Use Case:

External travelers planning trips use the skill to search Russian-catalog tours, hotels, flights, trains, and activities, then compare prices and booking links. It supports travel planning but does not book trips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search criteria, including destinations, dates, traveler counts or ages, budgets, and preferences, are sent to mcp.botclaw.ru; server retention is unspecified.

Mitigation: Send only necessary search criteria and omit names, passport details, payment information, and credentials.

Risk: Prices and availability may change, and some flight and train results are cached.

Mitigation: Verify booking-link destinations, current availability, and final prices with the provider before purchasing.

## Reference(s):

- [Usage reference](references/usage.md)
- [Travel Search MCP service](https://mcp.botclaw.ru/travel)
- [ClawHub skill page](https://clawhub.ai/missial/skills/travel-search-ru)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured search results summarized as travel guidance with prices and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Searches do not make bookings; some flight and train results may be cached.]

## Skill Version(s):

2.6.0 (source: SKILL.md frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
