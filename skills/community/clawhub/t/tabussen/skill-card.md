## Description:

Västerbotten & Umeå public transport trip planner (Tabussen/Ultra) that plans bus journeys using the ResRobot API and supports stops, addresses, coordinates, regional routes, and local routes throughout Västerbotten county.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simskii](https://clawhub.ai/user/simskii)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to search Swedish public transport stops and plan Tabussen, Ultra, and regional Västerbotten journeys using ResRobot-backed shell commands.

### Deployment Geography for Use:

Global use for Västerbotten, Sweden public transport planning

## Known Risks and Mitigations:

Risk: Trip-planning queries, stop identifiers, addresses, or coordinates are sent to ResRobot/Trafiklab when the shell scripts run.

Mitigation: Use the skill only when sharing trip-planning queries with ResRobot/Trafiklab is acceptable, and avoid including sensitive location details beyond what the journey search requires.

Risk: The ResRobot API key may be exposed through local shell tracing, process logging, or command-line handling.

Mitigation: Use a dedicated low-privilege ResRobot API key, avoid shell tracing and process logging when running the scripts, and rotate the key if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/simskii/skills/tabussen)
- [ResRobot API v2.1](https://api.resrobot.se/v2.1/)
- [ResRobot Trip Endpoint](https://api.resrobot.se/v2.1/trip)
- [ResRobot Location Lookup Endpoint](https://api.resrobot.se/v2.1/location.name)
- [Trafiklab Developer Portal](https://developer.trafiklab.se)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain-text journey results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and RESROBOT_API_KEY for live API-backed searches.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
