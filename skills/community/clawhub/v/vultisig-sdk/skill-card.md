## Description: <br>
Use this skill when an agent needs to create crypto wallets, send transactions, swap tokens, check balances, or perform any on-chain operation across 36+ blockchains using threshold signatures (TSS). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realpaaao](https://clawhub.ai/user/realpaaao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to guide agents through Vultisig SDK wallet setup, balance checks, transaction signing, broadcasts, swaps, and vault backup workflows. It is intended for on-chain cryptocurrency operations where the operator has explicitly accepted the custody and transaction risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can create wallets and move or swap real cryptocurrency without mandatory human approval. <br>
Mitigation: Use the skill only for intentional crypto-management workflows; start with a new low-value vault, prefer Secure Vault or explicit approval for sends and swaps, and apply spend limits and recipient allowlists where possible. <br>
Risk: Vault backups, passwords, and imported seedphrases can expose funds if mishandled. <br>
Mitigation: Avoid importing existing seedphrases, never log or store seed material in plaintext, protect .vult backups and passwords, and use secure storage for persistent agents. <br>
Risk: Incorrect recipient addresses, token decimals, gas settings, or swap assumptions can cause irreversible loss or failed transactions. <br>
Mitigation: Validate receiver addresses, use small test transactions, confirm token decimals and amount units, check gas estimates, and review swap quote warnings before broadcasting. <br>
Risk: The SDK package becomes part of the wallet transaction path. <br>
Mitigation: Pin or verify the SDK package before using it with real funds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/realpaaao/vultisig-sdk) <br>
- [Publisher profile](https://clawhub.ai/user/realpaaao) <br>
- [Vultisig SDK source](https://github.com/vultisig/vultisig-sdk) <br>
- [Vultisig SDK users guide](https://github.com/vultisig/vultisig-sdk/blob/main/docs/SDK-USERS-GUIDE.md) <br>
- [Vultisig agent integration guide](https://github.com/vultisig/vultisig-sdk/blob/main/docs/agent.md) <br>
- [Vultisig security and technology](https://docs.vultisig.com/security-and-technology/security-technology) <br>
- [VultiServer Fast Vault documentation](https://docs.vultisig.com/infrastructure/what-is-vultisigner/how-does-vultisigner-work) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with TypeScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational steps for wallet creation, transaction preparation, signing, broadcasting, swaps, balances, vault import/export, and security posture selection.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
