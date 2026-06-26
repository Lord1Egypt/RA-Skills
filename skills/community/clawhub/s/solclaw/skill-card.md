## Description: <br>
SolClaw enables agents to send and receive USDC on Solana devnet by human-readable agent name while signing transactions locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sterdam](https://clawhub.ai/user/Sterdam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use SolClaw to initialize or import a Solana devnet wallet, register a payable agent name, query balances, and execute USDC payments, invoices, allowances, and subscriptions from CLI guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through wallet setup, private-key import or export, and local transaction signing. <br>
Mitigation: Verify the solclaw CLI source or package before running npx, avoid pasting or exporting private keys unless necessary, and keep wallet files permission-restricted. <br>
Risk: Automated payments, allowances, subscriptions, and invoice execution can move funds without enough human review. <br>
Mitigation: Require explicit user approval for payment execution, set low spending caps, and prefer read-only heartbeat checks for routine automation. <br>
Risk: Heartbeat logs and command output may expose balances, agent names, or operational payment details. <br>
Mitigation: Restrict log file permissions and limit retained command output to what is needed for monitoring. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Sterdam/solclaw) <br>
- [SolClaw Skill](https://solclaw.xyz/skill.md) <br>
- [SolClaw Heartbeat](https://solclaw.xyz/heartbeat.md) <br>
- [SolClaw API Health](https://solclaw.xyz/api/health) <br>
- [Solana Devnet Explorer](https://explorer.solana.com/?cluster=devnet) <br>
- [Solana Faucet](https://faucet.solana.com) <br>
- [Circle Faucet](https://faucet.circle.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, API URLs, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may initialize wallets, sign Solana devnet transactions, query APIs, or configure recurring heartbeat checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
