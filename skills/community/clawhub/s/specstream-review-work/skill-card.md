## Description:

Get the real price for the exact request. Nothing runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[specstream](https://clawhub.ai/user/specstream)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users with a configured SpecStream MCP connection use this skill to quote the cost of a specific data request and check available balance before deciding whether to authorize spending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Request identifiers and quote parameters are sent to the configured SpecStream provider, whose remote implementation, authentication, and retention practices are outside this review.

Mitigation: Use a SpecStream MCP connection you trust and expect those values to reach the provider.

Risk: A quoted maximum price or displayed account balance could be mistaken for spending approval.

Mitigation: Keep quoting separate from spending authorization; use a quoted maximum only when explicitly authorized or already allowed by a bounded task.

## Reference(s):

- [SpecStream MCP endpoint](https://api.specstream.ai/mcp)
- [ClawHub release page](https://clawhub.ai/specstream/skills/specstream-review-work)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Text describing request scope, conditions, maximum price, and quote expiry]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quote requests and balance checks do not start a job or authorize spending.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
