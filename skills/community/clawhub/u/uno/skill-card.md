## Description:

Call 2000+ tools via curl, zero installation. Supports tool-level semantic search; get the full inputSchema in one step and invoke tools directly across search, development, documentation, finance, maps, travel, AI media, social, productivity, enterprise, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxyd-ai](https://clawhub.ai/user/lxyd-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover MCPMarket tools, inspect their input schemas, and call selected remote tools through curl-based API requests. It is useful when an agent needs broad third-party tool access without installing local packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad MCPMarket authorization can expose tool searches, arguments, and downstream delegated actions to remote services.

Mitigation: Use the skill only when users are comfortable sending the selected query and arguments to MCPMarket and the downstream tool provider; avoid secrets, private documents, credentials, source code, and regulated data unless the destination has been reviewed.

Risk: The bearer token is stored persistently at ~/.uno/token and can be reused if exposed.

Mitigation: Protect the token file with restrictive permissions, treat it as a sensitive credential, and revoke or rotate the token if disclosure is suspected.

Risk: Some downstream tools can require additional account linking, such as GitHub or Notion OAuth.

Mitigation: Review each downstream authorization request and service destination before linking accounts or retrying the tool call.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lxyd-ai/skills/uno)
- [MCPMarket homepage](https://mcpmarket.cn)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance, Text]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces curl-based workflows for authentication, tool search, tool invocation, ratings, credits, and skill lookup.]

## Skill Version(s):

3.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
