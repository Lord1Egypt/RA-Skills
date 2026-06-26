## Description: <br>
Search flights via Aviasales, tours via Travelata + Level.Travel, and excursions via Sputnik8 with real prices and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[missial](https://clawhub.ai/user/missial) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent search Russian-market travel options, compare flights, package tours, and excursions, and present compact options with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel searches and booking-link details are sent to external travel providers and the api.botclaw.ru proxy/shortener. <br>
Mitigation: Install only when the user accepts sharing travel-search details with those services, and avoid including unnecessary sensitive personal details in queries. <br>
Risk: Family travel searches may include children's ages, which can be sensitive personal information. <br>
Mitigation: Ask only for ages needed to search room layouts and fares, and avoid storing or repeating unnecessary child-related details. <br>
Risk: The skill produces shortened booking links that may lead to third-party booking flows. <br>
Mitigation: Inspect shortened links and final booking terms before purchase; the skill should present options, not complete bookings. <br>
Risk: Some travel prices are cached snapshots and may differ from final booking prices. <br>
Mitigation: Label cached or snapshot results clearly and tell users to verify current price, availability, baggage, and refund terms on the booking site. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/missial/travel-search-ru) <br>
- [Aviasales Data API reference](references/aviasales-data-api.md) <br>
- [Aviasales booking links](references/aviasales-links.md) <br>
- [Travelata API reference](references/travelata-api.md) <br>
- [Travelata directories](references/travelata-directories.md) <br>
- [Level.Travel API reference](references/leveltravel-api.md) <br>
- [Sputnik8 API reference](references/sputnik8-api.md) <br>
- [Tour selection playbook](references/tour-selection-playbook.md) <br>
- [Travelpayouts utilities](references/travelpayouts-utils.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown travel shortlists with prices, dates, notes, and booking links; may include shell commands for API calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access; flight and Level.Travel data may be cached while Travelata tour search is live.] <br>

## Skill Version(s): <br>
1.2.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
