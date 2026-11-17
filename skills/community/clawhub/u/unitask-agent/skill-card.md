## Description:

Start finishing tasks instead of just organizing them: connect your OpenClaw agent to Unitask (unitask.app) to manage and do your tasks with secure prioritization, tags, time blocks and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mfaiz-007](https://clawhub.ai/user/mfaiz-007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an AI agent to Unitask through a hosted MCP endpoint, then read, create, update, tag, merge, move, delete, and time-block tasks using scoped API tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and modify a user's own Unitask tasks when granted write or delete scopes.

Mitigation: Start with read-only scope, add write or delete only when needed, and store UNITASK_API_KEY in a secret store.

Risk: Delete, merge, move, or schedule changes may alter task organization or remove tasks from active views.

Mitigation: Confirm before applying deletes, merges, moves, or schedule changes, and use dry-run previews for compound actions where supported.

## Reference(s):

- [Unitask](https://unitask.app)
- [Unitask Hosted MCP Endpoint](https://unitask.app/api/mcp)
- [Unitask Agent on ClawHub](https://clawhub.ai/mfaiz-007/skills/unitask-agent)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Code, Markdown]

**Output Format:** [Markdown with configuration examples, tool guidance, and inline command or code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a UNITASK_API_KEY secret for authenticated MCP use.]

## Skill Version(s):

0.18.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
