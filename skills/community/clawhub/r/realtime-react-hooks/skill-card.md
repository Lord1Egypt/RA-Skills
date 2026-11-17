## Description:

React hooks for real-time data with SSE, WebSocket, and SWR integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add live updates to React applications, including dashboards, chat interfaces, notifications, and other interfaces that should update without refresh.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented npx installation paths rely on mutable, unpinned remote execution.

Mitigation: Review or pin the installer before running the commands, especially in sensitive development environments.

Risk: Realtime hooks can connect to SSE or WebSocket endpoints and channels that may carry sensitive data.

Mitigation: Connect only to trusted authenticated endpoints and avoid placing sensitive payloads on channels you do not control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/realtime-react-hooks)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript, TSX, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides reusable hook and component patterns for SSE, WebSocket reconnection, SWR updates, subscriptions, installation, and operational cautions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
