## Description:

Flight search and pricing via the RollingGo Flight MCP for searching and comparing flights by origin, destination, date, passenger count, cabin class, city code, or airport code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yorkluai-lab](https://clawhub.ai/user/yorkluai-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to resolve city or airport names, search one-way or round-trip flights, and compare flight options by price, timing, directness, and value score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flight-search details are sent to RollingGo's remote service.

Mitigation: Install only when sending origin, destination, dates, passenger counts, and cabin preferences to RollingGo is acceptable.

Risk: Returned prices and availability may change and the skill has no booking or payment authority.

Mitigation: Treat results as informational and confirm final availability, fare rules, and purchase details with the airline or booking provider.

## Reference(s):

- [RollingGo MCP Reference](references/rollinggo-mcp.md)
- [RollingGo Homepage](https://rollinggo.store)
- [RollingGo Flight MCP endpoint](https://mcp.rollinggo.cn/mcp/flight)
- [ClawHub Skill Page](https://clawhub.ai/yorkluai-lab/skills/rollinggo-searchflight-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown flight-option summaries with structured MCP request and response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Presents 3-5 flight options when available and reminds users that prices and inventory require final confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence, released 2026-04-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
