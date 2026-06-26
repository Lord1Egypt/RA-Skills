## Description: <br>
Use this skill to safely create a wallet the agent can use for transfers, swaps, and any EVM chain transaction, with support for raw signing and Polymarket betting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[piperwallet](https://clawhub.ai/user/piperwallet) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to create agent-controlled wallets, check balances, transfer or swap tokens, send EVM transactions, sign raw messages, and use Polymarket wallets under owner-defined policies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent may gain broad ongoing authority to move funds, sign messages, and place bets. <br>
Mitigation: Use a dedicated low-balance wallet, claim it immediately, and configure spending limits, allowlists, and require-approval policies before funding it. <br>
Risk: API keys and re-link tokens can authorize wallet access. <br>
Mitigation: Treat API keys and re-link tokens as financial credentials, store them securely, and avoid sharing them outside the intended agent workflow. <br>
Risk: Raw signing and arbitrary contract calls can produce irreversible or unintended blockchain actions. <br>
Mitigation: Avoid raw signing or arbitrary contract calls unless the wallet owner verifies the target, chain, amount, calldata, and expected effect. <br>


## Reference(s): <br>
- [Vincent Wallet Service](https://heyvincent.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/piperwallet/vincent-agent-wallet) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API request patterns, credential handling guidance, wallet policy guidance, and transaction workflow instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
