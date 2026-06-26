## Description: <br>
Deploy, import, interact with, and monitor smart contracts using Circle Smart Contract Platform APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mscandlen3](https://clawhub.ai/user/mscandlen3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and implement Circle Smart Contract Platform workflows for contract deployment, import, ABI-based reads and writes, template contracts, and event monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Circle API keys, entity secrets, or wallet credentials could be exposed if copied into frontend code, logs, committed files, or plain-text command flags. <br>
Mitigation: Keep secrets server-side in environment variables or a secrets manager, avoid logging them, and add ignore rules for local secret material. <br>
Risk: Deploy, mint, or write transactions can move funds or create irreversible on-chain effects on the wrong network, token, contract, or amount. <br>
Mitigation: Default to testnet and require manual confirmation of wallet, network, fee, contract address, function, token, and amount before any write transaction. <br>
Risk: Custom bytecode or unknown contracts may contain unaudited behavior or fail because of chain, constructor, gas, or EVM-version mismatches. <br>
Mitigation: Prefer audited templates when available, warn before deploying custom bytecode or interacting with unknown contracts, validate inputs, and poll deployment or transaction status for failures. <br>


## Reference(s): <br>
- [Circle Developer Docs](https://developers.circle.com/llms.txt) <br>
- [Deploy Smart Contract with Bytecode](references/deploy-bytecode.md) <br>
- [Deploy ERC-1155 Template](references/deploy-erc-1155.md) <br>
- [Interact with a Deployed Contract](references/interact.md) <br>
- [Monitor Smart Contract Events](references/monitor-events.md) <br>
- [Contract Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request patterns, environment variable guidance, transaction confirmation checklists, and polling steps.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
