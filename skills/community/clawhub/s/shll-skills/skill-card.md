## Description: <br>
Execute DeFi transactions on BSC via SHLL AgentNFA. The AI handles all commands and users only need to chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kledx](https://clawhub.ai/user/kledx) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an AI agent operate SHLL CLI or MCP tools for BSC DeFi onboarding, portfolio checks, swaps, lending, and policy-limited vault actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an AI agent authority to perform BSC DeFi actions with an operator private key. <br>
Mitigation: Use a new dedicated operator wallet with minimal gas only, never a main or owner wallet. <br>
Risk: Write operations such as transfers, config changes, and raw calldata can move funds or alter risk settings. <br>
Mitigation: Require explicit user confirmation before every write action and verify token ID, action type, amount, target, and risk note. <br>
Risk: Raw calldata may be unsafe when the recipient cannot be decoded or verified. <br>
Mitigation: Block undecodable recipient calldata and prefer built-in SHLL command flows where possible. <br>
Risk: Package or version confusion could install software other than the reviewed release. <br>
Mitigation: Verify the npm package name, version 6.0.5, and release hashes before installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kledx/shll-skills) <br>
- [SHLL Website](https://shll.run) <br>
- [npm Package](https://www.npmjs.com/package/shll-skills) <br>
- [PolicyGuard Contract](https://bscscan.com/address/0x25d17eA0e3Bcb8CA08a2BFE917E817AFc05dbBB3) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented runtime responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RUNNER_PRIVATE_KEY for write operations and may use SHLL_RPC for BSC RPC configuration.] <br>

## Skill Version(s): <br>
6.0.5 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
