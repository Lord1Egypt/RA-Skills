## Description:

Store and recall persistent memories via FlightBox (Quack Network).

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpaulgrayson](https://clawhub.ai/user/jpaulgrayson)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to store, recall, search, review, and delete persistent agent memories through FlightBox across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored memories are sent to and retrieved from the external FlightBox service.

Mitigation: Do not store passwords, API keys, private client data, or sensitive personal details unless you trust FlightBox retention, access control, and deletion practices.

Risk: FlightBox may be temporarily offline, which can interrupt memory storage or recall.

Mitigation: Check the documented FlightBox endpoint status before relying on the skill for time-sensitive workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jpaulgrayson/skills/quack-memory)
- [FlightBox API](https://flightbox.replit.app/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call FlightBox API endpoints using local Quack credentials and print JSON or text results.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
