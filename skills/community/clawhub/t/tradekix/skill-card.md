## Description:

Query financial market data via the Tradekix API for stock prices, crypto, forex, indices, market news, earnings, economic events, Congressional trades, and social sentiment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamesjohnfox](https://clawhub.ai/user/jamesjohnfox)

### License/Terms of Use:


## Use Case:

External users and agent developers use this skill to retrieve market data, financial news, economic and earnings calendars, social sentiment, and Congressional trade data through Tradekix API commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a Tradekix account and store an API key locally.

Mitigation: Require explicit human approval before signup, and install only in environments where storing the API key under the user's home directory is acceptable.

Risk: The skill includes account-changing commands for paid upgrade and API-key revocation.

Mitigation: Use read-only market data commands by default and require explicit human approval before running upgrade or revoke actions.

Risk: The security guidance warns against use where HOME or command arguments may be attacker-controlled.

Mitigation: Run the skill in a controlled agent environment with trusted HOME and command arguments.

## Reference(s):

- [Tradekix API Reference](references/api-docs.md)
- [Tradekix API Base URL](https://www.tradekix.ai/api/v1)
- [Tradekix API Docs](https://tradekix.ai/docs/api)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands read and write a local Tradekix API key config and return API response payloads.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
