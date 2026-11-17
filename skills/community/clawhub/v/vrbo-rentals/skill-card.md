## Description:

Search Vrbo vacation rentals by location, dates, and occupancy in one unified schema.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to discover Vrbo vacation rentals that match a destination, date range, occupancy, and rental filters through StayingAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow may persist a live StayingAPI key in a shell profile, plaintext config, logs, command history, shared environment, or source control.

Mitigation: Use a sandbox key for evaluation, prefer MCP OAuth/PKCE or a proper secret store for live use, and avoid exposing the key outside the agent runtime.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stayingapi/skills/vrbo-rentals)
- [StayingAPI homepage](https://stayingapi.com)
- [StayingAPI docs](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [Auth setup](references/auth-setup.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with API request guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct the agent to call StayingAPI REST or MCP endpoints and to handle asynchronous polling, rate limits, partial failures, and empty results.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
