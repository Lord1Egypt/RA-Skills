## Description: <br>
Connect to Robinhood's Agentic Trading MCP server and act on the user's behalf to list account and position tools, analyze a portfolio, and place trades via the official MCP with persistent OAuth authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmtucker](https://clawhub.ai/user/zmtucker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to a Robinhood account for account-aware portfolio review and user-authorized trading workflows. It is appropriate when the user intentionally wants the agent to authenticate to Robinhood and interact with the Agentic Trading MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent OAuth credentials grant ongoing access to a Robinhood trading account. <br>
Mitigation: Keep ROBINHOOD_MCP_HOME in protected persistent storage, treat credentials.json as a trading credential, and use logout or Robinhood revocation when access is no longer needed. <br>
Risk: The generic MCP tool-call path can place real orders without enforcement inside the script. <br>
Mitigation: Require separate explicit human confirmation before every order, including symbol, side, quantity, order type, and estimated cost. <br>
Risk: Robinhood MCP tools may change as the beta evolves. <br>
Mitigation: Discover available tools and inspect each input schema before calling a tool; surface tool errors to the user and avoid blind retries. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zmtucker/robinhood-mcp) <br>
- [Robinhood Agentic Trading Overview](https://robinhood.com/us/en/support/articles/agentic-trading-overview/) <br>
- [OAuth & cross-session persistence](references/oauth_and_persistence.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [MCP tool calls can return account data and trading results; tool-level errors are surfaced as JSON.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
