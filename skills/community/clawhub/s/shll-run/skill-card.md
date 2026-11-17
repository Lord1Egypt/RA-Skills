## Description:

Execute DeFi transactions on BSC via SHLL AgentNFA. The AI handles all commands and users only need to chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kledx](https://clawhub.ai/user/kledx)

### License/Terms of Use:

MIT

## Use Case:

Developers, agent operators, and external users use this skill to let AI agents inspect BSC vault state and execute policy-limited DeFi operations through SHLL CLI or MCP tools. It supports setup, portfolio checks, swaps, lending, transfers, and other BSC actions with confirmation requirements for write operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-operated DeFi transactions can move funds within the authority granted to the skill.

Mitigation: Install only if that operating model is acceptable, use a dedicated low-balance operator wallet, and review each write-operation confirmation carefully.

Risk: Private-key handling creates hot-wallet exposure.

Mitigation: Never provide an owner wallet or main-wallet key; use only a purpose-built operator wallet funded with minimal BNB for gas.

Risk: Unpinned remote npm execution can change the installed code unexpectedly.

Mitigation: Pin and verify the npm package before use and avoid latest-version npx execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kledx/skills/shll-run)
- [SHLL Website](https://shll.run)
- [shll-skills npm Package](https://www.npmjs.com/package/shll-skills)
- [PolicyGuard Contract on BscScan](https://bscscan.com/address/0x25d17eA0e3Bcb8CA08a2BFE917E817AFc05dbBB3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and machine-friendly JSON response expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write operations require explicit user confirmation; runtime responses are expected to use structured JSON success or error objects.]

## Skill Version(s):

6.0.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
