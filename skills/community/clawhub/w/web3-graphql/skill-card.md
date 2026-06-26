## Description: <br>
Use Ask GraphQL MCP to handle Web3 and on-chain questions through GraphQL endpoints, especially SubQuery and SubGraph endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subquery-network](https://clawhub.ai/user/subquery-network) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to answer Web3 and on-chain questions against user-provided GraphQL endpoints. It routes endpoint analysis, schema debugging, and setup guidance through Ask GraphQL MCP and returns concise results with configuration help when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can forward GraphQL endpoint URLs, prompts, and optional authorization headers to the Hermes Ask GraphQL MCP gateway. <br>
Mitigation: Use public endpoints where possible, and only provide scoped temporary endpoint credentials that can be rotated. <br>
Risk: Paid mode asks users to provide an Ask API key in chat after free quota or rate limits are reached. <br>
Mitigation: Avoid long-lived production API keys; use scoped temporary credentials and rotate or revoke them after use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/subquery-network/web3-graphql) <br>
- [Ask GraphQL MCP Templates](references/config-templates.md) <br>
- [Ask GraphQL MCP Tools And Prompts](references/tools-and-prompts.md) <br>
- [Ask GraphQL MCP Free Gateway](https://ask-api.hermes-subnet.ai/mcp/graphql-agent) <br>
- [Ask API Key Creation](https://ask.hermes-subnet.ai/billing/api-keys/) <br>
- [Ask Usage And Quota](https://ask.hermes-subnet.ai/billing/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with concise analysis sections and JSON configuration blocks when setup guidance is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include assumptions, MCP answer summaries, query details supplied by MCP, retry guidance, and free-to-paid quota handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
