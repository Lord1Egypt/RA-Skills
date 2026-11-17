## Description:

Provides real-time Swiss public transport station search, departure boards, journey planning, and connection details using transport.opendata.ch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xenofex7](https://clawhub.ai/user/xenofex7)

### License/Terms of Use:


## Use Case:

External users, travelers, and developers use this skill to search Swiss transit stations, inspect live departures, and plan point-to-point journeys through an agent or the included command-line helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Station names, routes, dates, and times may be sent to the public transport.opendata.ch service.

Mitigation: Avoid using the skill for travel queries that require strict privacy, and review outbound query details before execution.

## Reference(s):

- [transport.opendata.ch API](https://transport.opendata.ch)
- [ClawHub skill release page](https://clawhub.ai/xenofex7/skills/swiss-transport)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline bash commands and plain-text journey results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use HTTPS requests to transport.opendata.ch; no API key is required.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
