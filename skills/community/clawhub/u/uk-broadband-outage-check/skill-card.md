## Description:

Check whether a UK broadband provider is down right now, where, what the provider has said and how the last 30 days have gone. Use for "is my internet down", "is BT down" or UK broadband outage questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[findbroadband](https://clawhub.ai/user/findbroadband)

### License/Terms of Use:

MIT-0

## Use Case:

UK broadband customers use this skill to check current provider outage reports and recent outage history. It helps them understand what is being reported and directs anyone who remains offline to their provider for confirmation and support.

### Deployment Geography for Use:

United Kingdom

## Known Risks and Mitigations:

Risk: Public reports can be mistaken for a provider-confirmed outage or all-clear.

Mitigation: Preserve provider wording and distinguish public reports from provider-confirmed status, as indicated by the result.

Risk: A provider-level result may be mistaken for a diagnosis of an individual broadband line.

Mitigation: State that the data does not identify whether an individual address is affected, and direct users who remain offline to their provider's status page or support.

Risk: The outage server's data is not licensed for commercial use.

Mitigation: Use the server and its data only for personal broadband checks, consistent with FindBroadband's terms.

## Reference(s):

- [FindBroadband broadband outage information](https://www.findbroadbanddeals.com/is-my-broadband-down)
- [FindBroadband outage MCP server](https://www.findbroadbanddeals.com/api/mcp/outages)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Natural language outage status and history summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports provider status and public outage reports; data covers the last 30 days and does not identify issues at individual addresses.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
