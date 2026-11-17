## Description:

Runrelay helps agents search and book flights and hotels through the RunRelay API, including low-cost carrier coverage, travel planning tasks, and MCP-compatible integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runrelay](https://clawhub.ai/user/runrelay)

### License/Terms of Use:


## Use Case:

External travel agents, concierge workflows, and developers use this skill to search flights and hotels, compare travel options, and prepare bookings through RunRelay-backed services. It is suited to travel planning workflows that need airline, hotel, and MCP tool coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send passenger personal data to external travel services.

Mitigation: Before transmitting personal data, require the agent to show passenger fields, itinerary, price, provider, and destination service, then obtain explicit user confirmation.

Risk: The skill can initiate flight booking workflows without clear consent safeguards in the artifact.

Mitigation: Require explicit user confirmation before any reservation or booking request is sent.

## Reference(s):

- [ClawHub Runrelay Skill](https://clawhub.ai/runrelay/skills/runrelay)
- [RunRelay App](https://app.runrelay.io)
- [RunRelay API](https://api.runrelay.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API endpoint examples, environment variable setup, and user-confirmation guidance before booking actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
