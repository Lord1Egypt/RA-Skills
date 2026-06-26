## Description: <br>
Risk Art Agent is a Bankr integration skill that guides agents through natural-language crypto trading, DeFi wallet actions, portfolio checks, token deployment, automation, and LLM gateway usage across Base, Ethereum, Polygon, Solana, and Unichain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[riskiagung-prog](https://clawhub.ai/user/riskiagung-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Bankr through CLI commands or REST API calls for portfolio research, trading, transfers, NFT operations, Polymarket activity, token deployment, automation, and LLM gateway access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live wallet actions can move assets or create financial exposure. <br>
Mitigation: Use a dedicated low-balance wallet, prefer read-only keys for research, and verify chain, asset, amount, and recipient before write operations. <br>
Risk: Raw signing or submit flows can execute transactions that are difficult to inspect after submission. <br>
Mitigation: Avoid raw sign/submit unless the transaction can be decoded and reviewed; use confirmation-aware flows when available. <br>
Risk: Persistent automations and LLM auto top-up settings can continue spending after setup. <br>
Mitigation: Review active automations and auto top-up settings regularly, and cancel or disable anything no longer intended. <br>
Risk: API key exposure can allow unauthorized wallet or gateway use. <br>
Mitigation: Avoid storing live keys in shell profiles, enable IP restrictions where possible, and rotate or revoke keys when access is no longer needed. <br>


## Reference(s): <br>
- [Bankr homepage](https://bankr.bot) <br>
- [Bankr API Workflow Reference](references/api-workflow.md) <br>
- [Safety & Access Control Reference](references/safety.md) <br>
- [Sign and Submit API Reference](references/sign-submit-api.md) <br>
- [LLM Gateway Reference](references/llm-gateway.md) <br>
- [Token Trading Reference](references/token-trading.md) <br>
- [Portfolio Reference](references/portfolio.md) <br>
- [Market Research Reference](references/market-research.md) <br>
- [Transfers Reference](references/transfers.md) <br>
- [NFT Operations Reference](references/nft-operations.md) <br>
- [Polymarket Reference](references/polymarket.md) <br>
- [Leverage Trading Reference](references/leverage-trading.md) <br>
- [Token Deployment Reference](references/token-deployment.md) <br>
- [Automation Reference](references/automation.md) <br>
- [Arbitrary Transaction Reference](references/arbitrary-transaction.md) <br>
- [Error Handling Reference](references/error-handling.md) <br>
- [Agent Profiles Reference](references/agent-profiles.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and REST API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Bankr CLI commands, curl examples, configuration values, and safety checks for user review before live operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
