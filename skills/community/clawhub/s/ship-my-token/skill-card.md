## Description: <br>
Launch Solana tokens on Pumpfun, create memecoins, mint crypto tokens, manage creator fee sharing, claim trading earnings, and track a portfolio through chat with no code or config. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcoulaud](https://clawhub.ai/user/jcoulaud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and token creators use this skill to create Pumpfun/Solana tokens through an agent conversation, manage creator fee sharing, claim fees, and view portfolio recaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent authority to submit real Solana mainnet transactions for token launches, fee claims, and fee share changes. <br>
Mitigation: Use a dedicated low-balance wallet, require explicit user confirmation before transaction actions, and review the transaction intent before execution. <br>
Risk: The generated wallet private key controls funds and can be exported into chat if the user requests a backup. <br>
Mitigation: Avoid exporting the private key unless necessary, store any backup in a secure password manager or encrypted note, and never share it with others. <br>
Risk: Creator fee sharing reserves 20% of creator fees for Ship My Token. <br>
Mitigation: Confirm the fee split is understood before launches or fee-sharing updates and review the shareholder configuration. <br>
Risk: Daily recap setup can create persistent recurring portfolio activity through a heartbeat file or scheduled job. <br>
Mitigation: Check for and remove HEARTBEAT.md entries or scheduled recap jobs if recurring portfolio checks are not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jcoulaud/ship-my-token) <br>
- [Ship My Token docs](https://shipmytoken.com) <br>
- [Solana CLI install](https://docs.solanalabs.com/cli/install) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and parsed JSON script results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local wallet and token history files, submit Solana mainnet transactions, and configure recurring portfolio recaps.] <br>

## Skill Version(s): <br>
1.5.3 (source: SKILL.md metadata, CHANGELOG, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
