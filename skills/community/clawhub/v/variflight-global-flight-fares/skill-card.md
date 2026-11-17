## Description:

Variflight Global Flight Fares searches one-way flight fares from the Variflight ticket API by departure IATA city code, arrival IATA city code, and departure date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arisefx](https://clawhub.ai/user/arisefx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up one-way flight fare options for a specific route and departure date, then summarize airports, times, duration, price, transfers, and fare tag text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the route and departure date supplied by the user to Variflight's ticket API.

Mitigation: Use only the route and date needed for the fare lookup and avoid adding sensitive personal details.

Risk: Default formatted results are Chinese text, which may be unclear for users who expect English output.

Mitigation: Ask the agent to translate or summarize the output, or request raw JSON when exact payload data is needed.

## Reference(s):

- [Variflight Ticket Homepage](https://ticket.variflight.com/)
- [Variflight Flight List API Endpoint](https://ticket.variflight.com/ticket-api-gateway/open/search/flightListAI)
- [ClawHub Skill Page](https://clawhub.ai/arisefx/skills/variflight-global-flight-fares)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown summary with optional raw JSON payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Formatted text output is Chinese by default; raw JSON is available when requested.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
