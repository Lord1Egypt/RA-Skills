## Description:

Get a real Vrbo price quote for a listing and dates, then compare that property against the offers StayingAPI can resolve for it to find the cheapest rate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to quote a specific Vrbo listing for requested dates and occupancy, then compare the resolved property against available cross-OTA offers. It is suited to price-checking a known property, not searching for a list of alternatives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guide asks agents to persist STAYINGAPI_KEY across future sessions, which could expose a live API key if stored in plaintext or accessible to unrelated processes or backups.

Mitigation: Use a sandbox key for testing, and store live keys in an agent/runtime secret store or inject them only for the active session instead of saving them broadly in shell profiles.

## Reference(s):

- [StayingAPI homepage](https://stayingapi.com)
- [StayingAPI documentation](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [StayingAPI pricing](https://stayingapi.com/pricing)
- [Auth setup](references/auth-setup.md)
- [ClawHub skill page](https://clawhub.ai/stayingapi/skills/vrbo-prices)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request details, shell snippets, and price-comparison summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STAYINGAPI_KEY and internet access to api.stayingapi.com; live results depend on upstream property and OTA coverage.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
