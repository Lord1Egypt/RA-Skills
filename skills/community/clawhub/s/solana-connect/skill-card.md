## Description: <br>
Solana Connect helps agents generate or connect Solana wallets, inspect balances and token accounts, read transaction history, and simulate or send SOL transfers with configurable limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Seenfinity](https://clawhub.ai/user/Seenfinity) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agent builders use this skill to add Solana wallet queries and guarded SOL transfer workflows to agents. It is intended for blockchain interactions where dry-run simulation, transaction limits, and human confirmation controls are part of the operating procedure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move real SOL using a raw private key and is classified suspicious by the security evidence because it may affect real funds. <br>
Mitigation: Use testnet or a dedicated low-value wallet, keep dry-run enabled by default, and verify network, recipient, and amount before any real transaction. <br>
Risk: The release overstates private key protection while transfer functions still require a raw private key input. <br>
Mitigation: Do not provide a primary wallet private key to an agent; isolate secrets and review signing paths before deployment. <br>
Risk: Documented options can bypass human confirmation for real transfers. <br>
Mitigation: Avoid skipConfirmation for real funds and require a human approval step for transactions at or above the configured threshold. <br>


## Reference(s): <br>
- [ClawHub listing for Solana Connect](https://clawhub.ai/Seenfinity/solana-connect) <br>
- [README.md](README.md) <br>
- [scripts/solana.js](scripts/solana.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples and JSON-like wallet, balance, transaction, simulation, or signature results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Solana RPC configuration and transaction limit environment variables; dry-run mode is documented as the default for transfers.] <br>

## Skill Version(s): <br>
3.0.0 (source: evidence release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
