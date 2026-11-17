## Description:

Create, read, update, and delete memos on a Memos instance (usememos/memos), including requests such as saving, listing, updating, or deleting memos through openclaw-memos-mcp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sinhong2011](https://clawhub.ai/user/sinhong2011)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to let an agent manage notes in a self-hosted Memos instance, including creating private memos, searching existing memos, changing memo content or visibility, and deleting memos after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned npm MCP server that receives a Memos access token.

Mitigation: Install only after trusting the openclaw-memos-mcp package and publisher, and pin an exact reviewed package version where possible.

Risk: The MCP server can read, update, and delete memos using the configured token.

Mitigation: Use a least-privilege Memos token, store it through the MCP client's secret mechanism when available, and confirm destructive memo operations manually.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sinhong2011/skills/usememos)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with MCP tool calls and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Memos MCP tools that create, read, update, or delete memo records.]

## Skill Version(s):

0.1.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
