## Description:

Helps agents adopt and care for virtual pets using Animalhouse MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[animalhouseai](https://clawhub.ai/user/animalhouseai)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users and developers can connect an MCP host to Animalhouse to adopt a virtual pet, check its status, and provide ongoing care.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm or Smithery installs may fetch an unreviewed server version.

Mitigation: Pin the MCP server to a version reviewed before installation.

Risk: A locally saved API key can grant access if exposed.

Mitigation: Keep the key out of chats and notes, and rotate it if it may have leaked.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/animalhouseai/skills/virtual-pet-mcp)
- [Animalhouse homepage](https://animalhouse.ai)
- [Animalhouse MCP documentation](https://animalhouse.ai/docs/mcp)
- [Animalhouse API specification](https://animalhouse.ai/openapi.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes MCP tool calls for pet status, care, and account setup.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
