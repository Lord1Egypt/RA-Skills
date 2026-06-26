## Description: <br>
Solanaprox provides pay-per-request AI model access via Solana/USDC using a Phantom wallet address for wallet-native authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use Solanaprox to make paid AI model calls through a Solana wallet address, check balances, and route requests to Claude or GPT models without managing provider API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, responses, and the public wallet address are sent through the Solanaprox third-party proxy and upstream model providers. <br>
Mitigation: Use the skill only when that routing is acceptable for the data being sent, and avoid submitting sensitive prompts. <br>
Risk: Paid model calls can spend the wallet balance. <br>
Mitigation: Keep only a limited funded balance, check balance before calls, warn when funds are low, and do not make requests that would exceed the remaining balance. <br>
Risk: The optional npm MCP package and AIProx registration workflow are separate components from the skill text. <br>
Mitigation: Review those components before running the optional commands or registering an agent. <br>


## Reference(s): <br>
- [Solanaprox MCP server](https://github.com/solanaprox/mcp-server) <br>
- [Solanaprox service](https://solanaprox.com/) <br>
- [Solanaprox MCP npm package](https://npmjs.com/package/solanaprox-mcp) <br>
- [AIProx registry](https://aiprox.dev) <br>
- [Autonomous agent demo](https://github.com/unixlamadev-spec/autonomous-agent-demo) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and clean text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SOLANA_WALLET as the wallet address input and instructs agents to return clean text output rather than raw JSON.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
