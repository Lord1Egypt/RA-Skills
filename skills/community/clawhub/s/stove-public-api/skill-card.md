## Description:

Helps agents query Stove Protocol public market data, including platform statistics, ticker statistics, ticker heatmaps, and orderbook reference data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zschen211](https://clawhub.ai/user/zschen211)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve and summarize read-only Stove Protocol public market data through the bundled Python command-line helper and reference documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make network requests to a custom base URL.

Mitigation: Use the documented production or test Stove endpoints, and do not accept custom base URLs from untrusted prompts or point them at private/internal services.

Risk: Returned market data may be incomplete, unavailable, or misunderstood if API errors are not checked.

Mitigation: Check the Stove response code and error fields before summarizing data, and make clear when an API call failed or returned no usable data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zschen211/skills/stove-public-api)
- [Publisher profile](https://clawhub.ai/user/zschen211)
- [Public API](references/Public API.md)
- [Query Platform Statistics](references/Query Platform Statistics.md)
- [Query Ticker Heatmap](references/Query Ticker Heatmap.md)
- [Query Ticker Information and Statistics](references/Query Ticker Information and Statistics.md)
- [Query Ticker Orderbook](references/Query Ticker Orderbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled helper prints Stove API JSON responses to stdout for the agent to parse and summarize.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
