## Description: <br>
Alipay+ Voyager Travel Agent provides flight search, hotel recommendations, and multi-day itinerary planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[voyageragent](https://clawhub.ai/user/voyageragent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to plan trips, search live flight and hotel options, and assemble travel recommendations into a single markdown response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel search details such as cities, dates, and search terms are sent to Alipay+ servers. <br>
Mitigation: Use the skill only when users are comfortable sharing those details with Alipay+ and avoid entering sensitive personal information unless necessary. <br>
Risk: Hotel searches may apply default check-in and check-out dates when dates are missing. <br>
Mitigation: Confirm hotel dates before relying on recommendations or booking links. <br>
Risk: Returned booking links are recommendations from an external service. <br>
Mitigation: Review prices, dates, cancellation terms, and provider details directly before booking. <br>
Risk: Flight and hotel answers can become misleading if the agent invents unavailable options. <br>
Mitigation: Use only tool-returned flight and hotel data and clearly state when no matching results are returned. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/voyageragent/voyager-travel-agent) <br>
- [Publisher profile](https://clawhub.ai/user/voyageragent) <br>
- [Search Hotels](references/search-hotels.md) <br>
- [Search Flights](references/search-flights.md) <br>
- [Plan Itinerary](references/plan-itinerary.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown travel recommendations, comparison tables, and itinerary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight and hotel recommendations are expected to be grounded in Alipay+ service responses when those tools are used.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
