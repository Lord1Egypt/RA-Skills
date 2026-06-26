## Description: <br>
Execute DeFi transactions on BSC via SHLL AgentNFA. The AI handles all commands and users only need to chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kledx](https://clawhub.ai/user/kledx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent run BSC DeFi setup, portfolio, swap, lending, transfer, and raw calldata workflows through SHLL's CLI or MCP tools. The skill is intended for AI-assisted execution with a dedicated operator hot wallet and on-chain PolicyGuard limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates BSC transaction-signing authority to an AI-controlled operator hot wallet. <br>
Mitigation: Use a newly generated operator wallet with minimal BNB for gas only; never use the owner wallet, Agent NFT wallet, vault wallet, or any wallet holding significant funds. <br>
Risk: Trade, transfer, lending, and raw calldata actions can move assets if the user approves an unsafe request. <br>
Mitigation: Require clear approval before each write operation and verify token ID, action type, token or amount, target, and risk note before execution. <br>
Risk: Raw calldata and package or policy configuration mistakes may bypass user expectations even when on-chain checks exist. <br>
Mitigation: Verify the npm package and on-chain policy settings independently, prefer built-in command flows, and block undecodable calldata recipients. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kledx/shll-run) <br>
- [SHLL website](https://shll.run) <br>
- [npm package: shll-skills](https://www.npmjs.com/package/shll-skills) <br>
- [PolicyGuard contract on BscScan](https://bscscan.com/address/0x25d17eA0e3Bcb8CA08a2BFE917E817AFc05dbBB3) <br>
- [Project repository](https://github.com/kledx/shll-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and machine-friendly JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write operations require explicit user confirmation; runtime command responses should remain machine-friendly JSON.] <br>

## Skill Version(s): <br>
6.0.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
