## Description:

Persistent, consensus-validated memory for AI agents via the SAGE MCP server, supporting durable recall, reflection, and continuity across conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[l33tdawg](https://clawhub.ai/user/l33tdawg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect an MCP-capable agent to a local SAGE server for persistent memory, contextual recall, task reflection, and deletion or review of stored memories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists agent-written observations and memories across sessions.

Mitigation: Avoid storing secrets or sensitive personal data, review stored memories in the dashboard, use deletion controls when needed, and enable at-rest encryption if appropriate.

Risk: The local SAGE server can return operating instructions that influence agent behavior.

Mitigation: Treat the local server and dashboard as trusted components, review their configuration before use, and restrict use to environments where that local service is controlled.

Risk: Server-resolved provenance for this release is unavailable.

Mitigation: Verify the installed SAGE binary and release source before using the skill with confidential work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/l33tdawg/skills/sage-memory)
- [SAGE documentation](https://l33tdawg.github.io/sage/)
- [SAGE repository](https://github.com/l33tdawg/sage)
- [SAGE releases](https://github.com/l33tdawg/sage/releases)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline tool names and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a locally installed SAGE server and MCP configuration.]

## Skill Version(s):

5.0.2 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
