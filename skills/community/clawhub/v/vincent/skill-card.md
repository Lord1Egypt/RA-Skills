## Description: <br>
Use this skill to safely create a wallet the agent can use for transfers, swaps, and any EVM chain transaction. Also supports raw signing and polymarket betting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glitch003](https://clawhub.ai/user/glitch003) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents, developers, and wallet owners use this skill to create dedicated agent wallets, set owner-controlled transaction policies, and perform transfers, swaps, EVM contract calls, raw signing, and Polymarket betting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can operate a real wallet with broad power over funds, swaps, EVM transactions, raw signatures, and betting. <br>
Mitigation: Install only for a dedicated agent wallet, claim the wallet before funding it, and configure strict address, token, function, spending-limit, and manual-approval policies. <br>
Risk: API keys and re-link tokens can grant control over wallet actions. <br>
Mitigation: Treat API keys and re-link tokens as wallet-control secrets, store them securely, and avoid exposing them in chat logs, shared files, or command history. <br>
Risk: Raw signing and arbitrary contract calls can authorize actions whose effects are hard to inspect after execution. <br>
Mitigation: Avoid raw signing and arbitrary calldata unless a human can review the exact message, transaction target, calldata, and value before authorization. <br>


## Reference(s): <br>
- [ClawHub Vincent skill page](https://clawhub.ai/glitch003/vincent) <br>
- [Vincent wallet frontend](https://heyvincent.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and JSON request and response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bearer API keys for wallet actions and returns wallet addresses, claim URLs, transaction status, balances, signatures, market data, orders, or policy-related rejection states.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
