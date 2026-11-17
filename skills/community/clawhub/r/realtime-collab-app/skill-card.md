## Description:

Build real-time collaborative applications with shared whiteboards, live code editing, chat, CRDT synchronization, and presence indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use this skill to create real-time collaboration apps for shared whiteboarding, pair programming, collaborative documents, and live dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a lightweight starter prompt and references helper scripts that are not included in the artifact.

Mitigation: Review or create the helper scripts before running any generated setup commands.

Risk: Implemented real-time collaboration apps may expose network services, Redis, shared document state, and user content.

Mitigation: Review service configuration, access controls, data handling, and deployment settings before using generated applications with real users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshine-del-ux/skills/realtime-collab-app)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides starter commands and requirements for Node.js 18+ and Redis.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
