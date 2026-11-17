## Description:

Analyze Venus Protocol lending/borrowing positions on BNB Chain with risk-first guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zed-venus](https://clawhub.ai/user/zed-venus)

### License/Terms of Use:


## Use Case:

External users, DeFi operators, and developers use this skill to inspect Venus Protocol markets, wallet exposure, health factor, liquidation risk, and what-if borrow or supply scenarios before taking action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live fund-moving commands can move funds or change liquidation risk when run in broadcast mode.

Mitigation: Use simulation mode first, inspect the proposed action and health-factor impact, and require explicit human confirmation before any broadcast.

Risk: Commands support raw private-key input.

Mitigation: Do not paste real private keys into commands or AI chats; prefer external wallet signing or another controlled signing flow.

Risk: Flux/Fluid transaction tooling is included alongside Venus workflows.

Mitigation: Use Flux commands only when the user explicitly intends to operate on Flux/Fluid as well as Venus.

## Reference(s):

- [Protocol overview](references/protocol-overview.md)
- [Risk thresholds and formulas](references/risk-rules.md)
- [Contract and address notes](references/bnbchain-contracts.md)
- [Venus CLI cookbook](references/quick-commands.md)
- [Flux CLI cookbook](references/flux-quick-commands.md)
- [Flux BNB addresses](references/flux-bnb-addresses.json)
- [Glossary](references/glossary.md)
- [Skill summary](references/skill-summary.md)
- [Venus API](https://api.venus.io)
- [Instadapp Fluid BNB deployments](https://github.com/Instadapp/fluid-contracts-public/tree/main/deployments/bnb)
- [ClawHub skill page](https://clawhub.ai/zed-venus/skills/venus-agent-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise bullets, optional JSON from helper scripts, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Risk-first DeFi analysis; execution-capable commands should be simulated and reviewed before broadcast.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
