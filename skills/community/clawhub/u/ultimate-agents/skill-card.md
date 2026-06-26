## Description: <br>
Automates blockchain transactions, DEX swaps, wallet selection, RPC selection, and simple adaptive tracking for DeFi and dApp interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ariesbalweell](https://clawhub.ai/user/ariesbalweell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill as a DeFi automation agent for testnet or low-value wallet experiments involving wallet transactions, API checks, and DEX swap attempts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private keys can be used to sign irreversible blockchain transactions and swaps. <br>
Mitigation: Use a fresh testnet or low-value wallet, never use a funded mainnet private key, and stop the process when testing is complete. <br>
Risk: Automated DEX swaps may execute with unsafe router or token addresses and without sufficient user control. <br>
Mitigation: Review router and token addresses before use, add manual confirmation, and configure slippage limits before any swap. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ariesbalweell/ultimate-agents) <br>
- [Publisher profile](https://clawhub.ai/user/ariesbalweell) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires wallet private keys, RPC URLs, DEX router and token addresses, and transaction timing limits supplied through environment configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
