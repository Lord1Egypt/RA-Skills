## Description:

Connects an agent to Robinhood's Agentic Trading MCP server to read account tools and positions, analyze a portfolio, and place trades when the user explicitly requests it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmtucker](https://clawhub.ai/user/zmtucker)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to connect to a Robinhood account, discover available trading MCP tools, review portfolio information, and invoke account actions after explicit user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep ongoing access to a Robinhood account and that access can include trading.

Mitigation: Use it only when the user is comfortable granting this authority, prefer read-only actions by default, and require explicit human approval for every order.

Risk: Stored OAuth credentials can grant trading access if the credential directory is exposed.

Mitigation: Keep ROBINHOOD_MCP_HOME on private local storage, avoid shared or synced folders, and revoke access or run logout immediately if exposure is suspected.

Risk: Changing the MCP server URL could send account actions or authentication flow to an untrusted endpoint.

Mitigation: Do not set ROBINHOOD_MCP_URL except to a trusted Robinhood endpoint.

## Reference(s):

- [Robinhood Agentic Trading overview](https://robinhood.com/us/en/support/articles/agentic-trading-overview/)
- [OAuth and cross-session persistence](references/oauth_and_persistence.md)
- [ClawHub skill page](https://clawhub.ai/zmtucker/skills/robinhood-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and mcp>=1.9.0; commands may read, refresh, or delete local OAuth credential files.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
