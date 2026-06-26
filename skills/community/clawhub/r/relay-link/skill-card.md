## Description: <br>
Professional Bridge & Swap skill using Relay.link. Supports automated execution and smart tracking for 70+ networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flipz3ro](https://clawhub.ai/user/flipz3ro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and crypto operators use this skill to quote, confirm, execute, and monitor Relay.link token bridge transactions across supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a raw EVM private key to sign and broadcast live bridge transactions. <br>
Mitigation: Use a dedicated low-balance wallet and avoid primary wallets or long-lived high-value keys. <br>
Risk: Bridge execution can move funds if the recipient, chain, amount, fees, or transaction target is wrong. <br>
Mitigation: Independently verify the recipient, chain, amount, fees, and transaction target before confirming the quote. <br>
Risk: The security verdict indicates the safeguards are not sufficient for the level of financial authority requested. <br>
Mitigation: Treat generated actions as proposals, require explicit user confirmation, and review the transaction details before signing. <br>


## Reference(s): <br>
- [Relay Link Bridge ClawHub page](https://clawhub.ai/flipz3ro/relay-link) <br>
- [Relay chains API](https://api.relay.link/chains) <br>
- [Relay currencies API](https://api.relay.link/currencies/v1) <br>
- [Relay status API](https://api.relay.link/intents/status/v3) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text, JSON] <br>
**Output Format:** [Markdown/text guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, cast, and bc; uses EVM_PRIVATE_KEY, EVM_ADDRESS, and SOLANA_ADDRESS when configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
