## Description:

Look up a local service business (plumber, HVAC, electrician, roofer, contractor) on ServiceFront and answer from its owner-verified facts: hours, service area, contact and owner-confirmed prices. Use when someone asks about a business on ServiceFront or a <name>.servicefront.ai address, wants a confirmed price from one, or is a service business owner asking what ServiceFront is, what it costs or how to set it up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[servicefront](https://clawhub.ai/user/servicefront)

### License/Terms of Use:

MIT-0

## Use Case:

External users can find local service businesses and get hours, service areas, contact details, or owner-confirmed prices. Service business owners can also learn about ServiceFront, its pricing, and setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts ServiceFront's external MCP service, and the security summary notes some uncertainty about data transmission.

Mitigation: Use business search details only, and consider whether contacting the external service is appropriate before use.

## Reference(s):

- [ServiceFront read-only MCP endpoint](https://servicefront.ai/api/mcp/read)
- [ServiceFront pricing](https://servicefront.ai/pricing.md)
- [ServiceFront](https://servicefront.ai)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Natural-language text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers rely on owner-verified details and identify when information or a confirmed price is unavailable; the skill does not book appointments or take requests.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
