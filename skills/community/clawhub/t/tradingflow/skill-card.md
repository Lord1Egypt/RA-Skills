## Description: <br>
Create and manage crypto trading strategies, deploy automated trading bots, and control on-chain vaults on BSC, Aptos, and Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheCleopatra](https://clawhub.ai/user/TheCleopatra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and developers use this skill to create, deploy, monitor, and revise automated TradingFlow strategies while managing supported on-chain vault operations. It is intended for agent-assisted crypto strategy workflows that may require user approval for fund movement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent create and deploy crypto trading bots and prepare vault operations with financial impact. <br>
Mitigation: Use least-privilege API keys, start with tiny spending limits, and require explicit confirmation before deployments, vault permission changes, or fund-related actions. <br>
Risk: The skill handles trading credentials and secrets. <br>
Mitigation: Store credentials only as secret entries, avoid exposing secret values in conversation, and rotate keys if they may have been shared. <br>
Risk: Unauthenticated or weakly protected webhooks can trigger automated trading behavior. <br>
Mitigation: Avoid unauthenticated webhooks for processes that can trade and use webhook secrets or other validation before acting on external signals. <br>
Risk: A misconfigured API endpoint or untrusted base URL could send trading commands or credentials to the wrong service. <br>
Mitigation: Confirm the API base URL uses HTTPS and points to the trusted TradingFlow service before running commands. <br>


## Reference(s): <br>
- [TradingFlow Homepage](https://tradingflow.fun) <br>
- [ClawHub Skill Page](https://clawhub.ai/TheCleopatra/tradingflow) <br>
- [TradingFlow API Reference](artifact/references/api-reference.md) <br>
- [Strategy Format Reference](artifact/references/strategy-format.md) <br>
- [Vault Operations Guide](artifact/references/vault-operations.md) <br>
- [Webhooks & Triggers](artifact/references/webhook-triggers.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with JSON, code, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce strategy files, deployment commands, API request payloads, approval links, and operational status summaries.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
