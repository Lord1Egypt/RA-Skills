## Description:

Toolbelt helps agents ingest documents, query structured and unstructured data, and share findings through a persistent MCP workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toolbeltai](https://clawhub.ai/user/toolbeltai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Toolbelt to ingest user-approved documents, query structured and unstructured workspace data, and carry findings across sessions. It is suited to tasks that benefit from persistent shared context and MCP-based retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags possible MCP configuration access and a reported mismatch involving account details in a web request; the scan is incomplete.

Mitigation: Review the onboarding request and proposed configuration changes before approving them, and protect or revoke any issued access token.

Risk: Workspace uploads and recorded findings persist, and a share URL can grant access to a namespace.

Mitigation: Upload only task-approved content, avoid sensitive data unless needed, and share namespace links only with intended recipients.

## Reference(s):

- [Toolbelt skill release](https://clawhub.ai/toolbeltai/skills/toolbelt)
- [Toolbelt documentation](https://toolbelt.ai/docs)
- [Toolbelt homepage](https://toolbelt.ai)
- [Toolbelt workspace app](https://app.toolbelt.ai)
- [Toolbelt MCP endpoint](https://mcp.toolbelt.ai/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, API calls, JSON, Text]

**Output Format:** [Markdown guidance with shell and JSON examples; workspace query results and connection status as text or structured data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create an MCP client configuration after user confirmation; workspace operations depend on the user's connected Toolbelt account.]

## Skill Version(s):

1.1.11 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
