## Description:

How to create, retrieve, list, and delete Zoom meetings using the Zoom REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neuyazvimyi](https://clawhub.ai/user/neuyazvimyi)

### License/Terms of Use:


## Use Case:

Employees, external users, developers, and agents use this skill to schedule Zoom meetings, retrieve meeting access details, list upcoming meetings, and delete meetings through Zoom Server-to-Server OAuth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Zoom Server-to-Server OAuth credentials and can create, read, list, and delete meetings.

Mitigation: Use least-privileged Zoom scopes and avoid broad admin credentials.

Risk: Meeting deletion has no clear confirmation safeguard.

Mitigation: Verify meeting IDs before deletion and require operator confirmation in workflows that call delete actions.

Risk: Created meetings disable the waiting room and allow participants to join before the host.

Mitigation: Review meeting defaults before use and adjust Zoom settings when stricter participant controls are required.

Risk: Meeting access details such as join URLs and passwords may be returned in human-readable output.

Mitigation: Share skill output only in appropriate channels and avoid exposing meeting details to unauthorized users.

## Reference(s):

- [Zoom API Reference](references/zoom_api_reference.md)
- [Zoom API base endpoint](https://api.zoom.us/v2)
- [Zoom OAuth token endpoint](https://zoom.us/oauth/token)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Human-readable Markdown/text responses with meeting details, links, passwords, status, errors, and command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No JSON output is intended for users; the skill may call Zoom API actions for create, retrieve, list, and delete operations.]

## Skill Version(s):

1.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
