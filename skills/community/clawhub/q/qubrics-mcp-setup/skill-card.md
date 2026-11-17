## Description:

Connect OpenClaw and other agent clients to hosted or local Qubrics MCP servers for mailbox, sending, and management tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roshanjonah](https://clawhub.ai/user/roshanjonah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect OpenClaw and other supported clients to Qubrics mailbox, sending, and management tools through hosted OAuth or a local MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence notes that the package-index installation route is unpinned and could install a release different from the one described.

Mitigation: Verify that the intended qubrics-mcp release is published before installing it; hosted OAuth is documented as an alternative.

Risk: The scanner evidence is incomplete because some local path references could not be resolved.

Mitigation: Review the relevant source and unresolved references before relying on the skill in a deployment.

## Reference(s):

- [Qubrics skills repository (release metadata homepage)](https://github.com/qubrics/skills)
- [Qubrics hosted MCP endpoint](https://mcp.qubrics.com/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and client-specific configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use secret-backed environment variables for credentials and vary by MCP client and server surface.]

## Skill Version(s):

2.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
