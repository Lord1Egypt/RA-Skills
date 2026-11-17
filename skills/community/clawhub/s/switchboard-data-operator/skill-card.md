## Description:

Autonomous operator for Switchboard on-demand feeds, Surge streaming, and randomness. Designs jobs, simulates via Crossbar, and deploys/updates/reads feeds across Solana/SVM, EVM, Sui, and other Switchboard-supported chains-with user-controlled security, spend limits, and allow/deny lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oakencore](https://clawhub.ai/user/oakencore)

### License/Terms of Use:


## Use Case:

Developers, protocol teams, feed creators, DeFi teams, and automation operators use this skill to plan, simulate, deploy, update, read, and integrate Switchboard oracle feeds, signed streams, and randomness across supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server security evidence flags the release as suspicious because it may route sensitive credentials, including reusable private keys, through remote oracle workflows without enough scoping or disclosure.

Mitigation: Keep the skill in read-only or plan-only mode unless explicit spend limits, allowlists, isolated environments, and short-lived scoped credentials are in place.

Risk: The skill can guide transaction signing, fee payment, feed deployment, and on-chain state changes across multiple chains.

Mitigation: Require per-transaction approval for execution modes, confirm mainnet signing explicitly, and enforce allowlists for programs, contracts, RPC endpoints, and Crossbar URLs.

Risk: API keys, wallet keys, JWTs, and other secrets may be needed for examples or live operation.

Mitigation: Do not print secrets or full environment files; prefer keystores, local signing, secret managers, and pinned package versions in an isolated environment without production wallet secrets.

## Reference(s):

- [Switchboard Skill Page](https://clawhub.ai/oakencore/skills/switchboard-data-operator)
- [Switchboard Documentation](https://docs.switchboard.xyz/)
- [Switchboard Docs by Chain](https://docs.switchboard.xyz/docs-by-chain)
- [Crossbar Documentation](https://docs.switchboard.xyz/tooling/crossbar)
- [Switchboard SDKs](https://docs.switchboard.xyz/tooling/sdks)
- [Switchboard Feed Builder](https://explorer.switchboardlabs.xyz/feed-builder)
- [Switchboard Task Types Reference](https://explorer.switchboardlabs.xyz/task-docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks, command snippets, configuration examples, and structured plans.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include operator policies, feed plans, deployment steps, readiness reports, integration code, rollback guidance, and risk notes.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
