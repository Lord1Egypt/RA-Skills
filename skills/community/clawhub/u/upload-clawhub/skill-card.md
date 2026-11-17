## Description:

Execute DeFi transactions on BSC via SHLL AgentNFA. The AI handles all commands and users only need to chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kledx](https://clawhub.ai/user/kledx)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to guide AI-assisted DeFi operations on BSC mainnet through SHLL CLI and MCP tooling. It supports onboarding, portfolio checks, policy-aware swaps, lending, transfers, and transaction confirmation flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate with an operator wallet private key and initiate financial transactions.

Mitigation: Use only a dedicated operator wallet with minimal BNB for gas, never use a main or owner wallet, and require explicit confirmation before every transaction.

Risk: Latest-version npm or npx commands can introduce unreviewed package changes into wallet-handling workflows.

Mitigation: Pin or preinstall a reviewed shll-skills version, verify package integrity before use, and rotate the operator key if package integrity is uncertain.

Risk: Raw calldata and undecoded recipients are high-risk transaction paths.

Mitigation: Prefer built-in command flows, use strict recipient checks, and block execution when calldata recipients cannot be decoded safely.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kledx/skills/upload-clawhub)
- [SHLL Website](https://shll.run)
- [SHLL Skills npm Package](https://www.npmjs.com/package/shll-skills)
- [PolicyGuard Contract on BscScan](https://bscscan.com/address/0x25d17eA0e3Bcb8CA08a2BFE917E817AFc05dbBB3)
- [Artifact-Declared Repository](https://github.com/kledx/shll-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and machine-friendly JSON response expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent runtime responses are expected to use structured JSON success or error objects.]

## Skill Version(s):

6.0.5 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
