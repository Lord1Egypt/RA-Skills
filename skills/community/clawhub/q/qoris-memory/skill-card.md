## Description:

Legacy ClawHub listing that directs users to install qoris-memory-mcp for Qoris persistent MCP-based agent memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apps-debug](https://clawhub.ai/user/apps-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users with existing qoris-memory installs use this legacy listing for backward compatibility while migrating to qoris-memory-mcp. The underlying MCP integration supports explicit memory storage, retrieval, search, update, deletion, and document lookup through Qoris cloud services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This is a legacy listing and may not receive future feature updates.

Mitigation: Install the canonical qoris-memory-mcp listing for current releases and support.

Risk: Memory content and knowledge documents are stored in Qoris cloud services for the configured workspace.

Mitigation: Confirm Qoris cloud storage is approved for the workspace before saving sensitive, regulated, or confidential data.

Risk: Access depends on a user-provided QORIS_API_KEY.

Mitigation: Keep the API key out of saved memories and rotate it when access should be revoked.

## Reference(s):

- [Qoris homepage](https://qoris.ai)
- [Qoris Memory documentation](https://docs.qoris.ai/memory)
- [Canonical qoris-memory-mcp listing](https://clawhub.ai/qoris-memory-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QORIS_API_KEY and QORIS_WORKSPACE_ID; connects to the Qoris MCP server.]

## Skill Version(s):

1.0.5 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
