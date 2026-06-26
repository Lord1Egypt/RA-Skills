## Description: <br>
Variflight Global Flight Fares searches one-way flight fares from the Variflight ticket API by departure IATA city code, arrival IATA city code, and departure date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AriseFX](https://clawhub.ai/user/AriseFX) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel assistants, operations teams, and end users use this skill to look up one-way flight fare options for a single route and date from Variflight using IATA city codes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries send the departure code, arrival code, and departure date to Variflight's ticket API. <br>
Mitigation: Inform users before lookup and avoid submitting sensitive itinerary details beyond the route and date needed for the fare search. <br>
Risk: Fare and flight availability data can change or the external API can return errors or no results. <br>
Mitigation: Surface API error messages and empty-result responses clearly, and advise users to verify important fare decisions before booking. <br>


## Reference(s): <br>
- [Variflight Ticket Homepage](https://ticket.variflight.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/AriseFX/variflight-global-flight-fares) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Markdown summary or raw JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries include airports, times, duration, price, transfer status, and flight tag text; result count can be limited.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
