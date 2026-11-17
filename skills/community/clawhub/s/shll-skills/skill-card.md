## Description:

Execute DeFi transactions on BSC via SHLL AgentNFA. The AI handles all commands and users only need to chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kledx](https://clawhub.ai/user/kledx)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent run SHLL CLI or MCP workflows for BSC DeFi operations, including setup checks, portfolio reads, swaps, lending, transfers, and raw calldata execution through PolicyGuard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an operator private key for DeFi execution.

Mitigation: Use only a fresh dedicated operator wallet with minimal BNB for gas, and never reuse a main wallet, owner wallet, or wallet holding significant funds.

Risk: The server security review flags unpinned npm execution as a supply-chain risk.

Mitigation: Pin and verify the npm package before execution, and avoid unpinned npx MCP setup.

Risk: Raw calldata, transfers, and configuration changes can authorize high-impact transactions.

Mitigation: Require explicit confirmation before these actions and review the token ID, action type, amount, target, and risk note before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kledx/skills/shll-skills)
- [SHLL website](https://shll.run)
- [npm package](https://www.npmjs.com/package/shll-skills)
- [PolicyGuard contract on BscScan](https://bscscan.com/address/0x25d17eA0e3Bcb8CA08a2BFE917E817AFc05dbBB3)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and machine-friendly JSON runtime responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a dedicated RUNNER_PRIVATE_KEY operator wallet for write operations; write operations require explicit user confirmation.]

## Skill Version(s):

6.0.5 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
