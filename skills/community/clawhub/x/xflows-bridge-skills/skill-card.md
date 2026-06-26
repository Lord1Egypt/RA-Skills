## Description: <br>
Helps an agent use the xflows CLI to manage EVM wallets, query bridge routes, estimate fees, send cross-chain or same-chain token transfers, check balances, and track transaction status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lolieatapple](https://clawhub.ai/user/lolieatapple) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and crypto operators use this skill to guide agent-driven xflows CLI workflows for EVM wallet management, route discovery, bridge quotes, cross-chain transfers, same-chain token transfers, balance checks, and transaction tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet private keys or recovery details can be exposed through wallet import or wallet show operations. <br>
Mitigation: Use fresh low-balance wallets, enable wallet encryption, avoid importing main private keys, and avoid wallet show unless recovery is required. <br>
Risk: Cross-chain and same-chain sends are irreversible blockchain transactions that can transfer funds to the wrong chain, token, or recipient. <br>
Mitigation: Run dry-runs first and manually confirm chain IDs, token contracts, recipient, amount, fees, slippage, and RPC before real transactions. <br>
Risk: The skill depends on the external xflows CLI and package source. <br>
Mitigation: Verify the xflows package source and version before use and keep transaction approvals scoped to the intended route. <br>


## Reference(s): <br>
- [XFlows CLI](https://github.com/wandevs/xflows-cli) <br>
- [XFlows CLI Complete Command Reference](references/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create wallet files, query balances, dry-run transfers, or broadcast blockchain transactions through the xflows CLI.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
