## Description:

Search one-way flight lists from the Variflight ticket API by departure IATA city code, arrival IATA city code, and departure date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arisefx](https://clawhub.ai/user/arisefx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up one-way flight options for a route and date, then summarize direct and transfer flights with airports, times, duration, price, and tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill sends the requested route and departure date to Variflight's ticket API.

Mitigation: Use only route and date details that are appropriate to share with the Variflight service.

Risk: Formatted script output is primarily Chinese.

Mitigation: Ask the agent to translate or summarize the returned flight details when a different output language is needed.

Risk: Flight availability and prices may change after the API response is returned.

Mitigation: Verify important itinerary, fare, and booking details directly with the provider before making travel decisions.

## Reference(s):

- [Variflight ticket homepage](https://ticket.variflight.com/)
- [ClawHub skill page](https://clawhub.ai/arisefx/skills/variflight-flight-search)
- [Publisher profile](https://clawhub.ai/user/arisefx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown summaries with optional raw JSON payloads from the flight query script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Formatted script output is primarily Chinese; raw JSON is returned only when requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
