## Description:

Provides a localhost collaboration server for agents to coordinate through chat, task management, presence, team health, and a web dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryancampbell](https://clawhub.ai/user/ryancampbell)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developer teams use this skill to coordinate local multi-agent work by exchanging messages, creating and updating tasks, tracking presence, and viewing team health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Anyone can create tasks, so agents may receive untrusted task descriptions or messages.

Mitigation: Treat chat messages and task descriptions as untrusted input, and require human approval before acting on tasks that read files, run commands, modify data, or contact external systems.

Risk: The collaboration service is intended for local or trusted team use and lacks documented authentication or approval checks.

Mitigation: Install only in a trusted local or team environment and avoid placing secrets or credentials into the service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryancampbell/skills/reflectt-node)
- [Publisher profile](https://clawhub.ai/user/ryancampbell)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown guidance with inline curl commands and endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coordinates through a localhost service at 127.0.0.1:4445 and references local data storage under ~/.reflectt/data/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
