## Description:

Coordinate work across avatars and agents using the Tick protocol and Git-backed TICK.md task files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptoreumd](https://clawhub.ai/user/cryptoreumd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and multi-agent operators use this skill to create, claim, update, validate, and summarize coordinated tasks across humans and agents. It supports dependency tracking, handoffs, local Git-backed audit trails, and optional CLI or MCP workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional dashboard can expose project task data through a temporary web server.

Mitigation: Use local-only operation when possible, bind the dashboard to 127.0.0.1, run it only on trusted networks, and stop it after inspection.

Risk: Remote task syncing can transfer project task data outside the local repository.

Mitigation: Sync only to Convex deployments and keys you control, and avoid syncing sensitive task content unless remote visibility is required.

Risk: Agents maintaining TICK.md may make incorrect task, status, dependency, or handoff changes.

Mitigation: Review TICK.md diffs, run tick validate before syncing, and rely on Git history to audit or revert unwanted task-state changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cryptoreumd/skills/tick-coord)
- [Tick CLI npm Package](https://npmjs.com/package/tick-md)
- [Tick MCP Server npm Package](https://npmjs.com/package/tick-mcp-server)
- [Tick Project Reference](https://github.com/Purple-Horizons/tick-md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional MCP tool-call descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to create or update local TICK.md task state through the Tick CLI or configured MCP tools.]

## Skill Version(s):

1.0.0 (source: evidence release and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
