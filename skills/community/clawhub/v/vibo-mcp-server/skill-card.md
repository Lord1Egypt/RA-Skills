## Description:

ViBo MCP helps AI agents retain and retrieve user-approved facts and thread context through locally stored memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vnbochkarev-netizen](https://clawhub.ai/user/vnbochkarev-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other MCP-client users can give AI agents persistent local recall of facts and conversations with the user's explicit consent. A ViBo license key is required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unverified external package or following a lookalike documentation account could introduce untrusted code or instructions.

Mitigation: Verify the npm package name, pinned version, registry integrity, and GitHub documentation account before installing; review the version change before upgrading.

Risk: Stored facts and thread history persist locally and may contain sensitive information.

Mitigation: Ask for explicit consent before storing memory, limit the server to a dedicated storage location, and delete files or use forget/wipe when data is no longer needed.

Risk: The release version differs from the versions shown in the skill and installation examples.

Mitigation: Confirm the intended audited npm version and its integrity before installation rather than assuming the ClawHub release version matches the npm package.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/vnbochkarev-netizen/skills/vibo-mcp-server)
- [ViBo documentation (verify account before use)](https://github.com/КГ-netizen/ViBo-memory)
- [ViBo website](https://wwwvibo.com)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration instructions, Shell commands]

**Output Format:** [Markdown with installation commands, MCP configuration examples, and memory-tool guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Memory search and thread tools may return locally stored facts and conversation context.]

## Skill Version(s):

0.2.7 (source: server-resolved ClawHub release; artifact frontmatter lists 0.2.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
