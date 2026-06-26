## Description: <br>
Search one-way flight lists from the Variflight ticket API by departure IATA city code, arrival IATA city code, and departure date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AriseFX](https://clawhub.ai/user/AriseFX) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve and summarize one-way flight options for a route and date using IATA city codes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight-search details are sent to Variflight. <br>
Mitigation: Use the skill only when sharing departure city code, arrival city code, and travel date with Variflight is acceptable. <br>
Risk: The returned flight data can be incomplete, unavailable, or time-sensitive. <br>
Mitigation: Treat results as search assistance and confirm important itinerary, fare, and availability details before booking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AriseFX/variflight-flight-search) <br>
- [Variflight ticket homepage](https://ticket.variflight.com/) <br>
- [Variflight flight list API endpoint](https://ticket.variflight.com/ticket-api-gateway/open/search/flightListAI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Markdown summary or raw JSON payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May limit displayed result count; includes route, date, times, airports, duration, price, transfer status, and flight tag text when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
