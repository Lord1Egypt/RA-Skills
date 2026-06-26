## Description: <br>
Execute DeFi transactions on BSC via SHLL AgentNFA. The AI handles all commands and users only need to chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kledx](https://clawhub.ai/user/kledx) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an AI agent operate SHLL CLI and MCP flows for BSC DeFi vault readiness checks, portfolio review, swaps, lending, transfers, and guarded calldata execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an AI agent and an external npm package transaction authority through a private operator key on BSC mainnet. <br>
Mitigation: Use a fresh operator wallet with minimal gas only, never use an owner or main wallet, and pin and review the npm package before providing a key. <br>
Risk: AI-assisted DeFi execution can submit trades or configuration changes that move funds or alter risk exposure. <br>
Mitigation: Require explicit confirmation for every transaction or configuration change and keep tight on-chain spending, receiver, cooldown, and protocol limits. <br>
Risk: Raw calldata execution can be difficult to inspect and may route funds unexpectedly if not decoded correctly. <br>
Mitigation: Avoid raw calldata unless independently verified and rely on strict recipient checks that block undecodable calldata. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kledx/upload-clawhub) <br>
- [SHLL website](https://shll.run) <br>
- [shll-skills npm package](https://www.npmjs.com/package/shll-skills) <br>
- [PolicyGuard contract on BscScan](https://bscscan.com/address/0x25d17eA0e3Bcb8CA08a2BFE917E817AFc05dbBB3) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and machine-friendly JSON runtime responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write operations require explicit user confirmation and use a dedicated operator wallet private key for transaction execution.] <br>

## Skill Version(s): <br>
6.0.5 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
