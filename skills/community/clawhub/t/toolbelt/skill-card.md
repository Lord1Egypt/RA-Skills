## Description:

Toolbelt helps agents ingest documents, query structured and unstructured data through an MCP workspace, and share persistent findings across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toolbeltai](https://clawhub.ai/user/toolbeltai)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agents use this skill to connect to Toolbelt when they need document extraction, hybrid search across structured and unstructured data, or a shared workspace for findings across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can provision an account, send network requests, and change an MCP client configuration.

Mitigation: Follow the skill's confirmation steps and review the service destination and proposed client configuration before enabling the connection.

Risk: Uploaded content persists in a shared workspace, and a share URL can grant access to that namespace.

Mitigation: Upload only user-approved, task-relevant content and treat share URLs as credentials that should go only to intended recipients.

## Reference(s):

- [Toolbelt documentation](https://toolbelt.ai/docs)
- [Toolbelt service](https://toolbelt.ai)
- [Toolbelt workspace UI](https://app.toolbelt.ai)
- [Toolbelt MCP endpoint](https://mcp.toolbelt.ai/mcp)

## Skill Output:

**Output Type(s):** [Guidance, MCP tool calls, Configuration instructions, YAML status]

**Output Format:** [Natural-language guidance, MCP tool calls, and YAML connection status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Account provisioning and MCP configuration are performed only after user confirmation.]

## Skill Version(s):

1.1.8 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
