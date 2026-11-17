## Description:

Trade on UniClaw prediction markets. Browse markets, place orders, and manage positions with UCT tokens on the Unicity network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvsteiner](https://clawhub.ai/user/jvsteiner)

### License/Terms of Use:


## Use Case:

External agents and developers use this skill to interact with UniClaw prediction markets, including market discovery, registration, deposits, order placement, order cancellation, portfolio review, and withdrawals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a Unicity wallet to trade and request withdrawals.

Mitigation: Use a testnet or limited-balance wallet and review trade amounts, market IDs, and withdrawal recipients before execution.

Risk: Custom UNICLAW_SERVER values can route signed requests to an untrusted endpoint.

Mitigation: Use only the default server or a trusted endpoint controlled by the user.

Risk: The security evidence flags wallet secret handling, hardcoded credentials, and weak request signing as concerns.

Mitigation: Prefer a release that removes raw private-key export, removes hardcoded credentials, and strengthens request signing before higher-value use.

## Reference(s):

- [UniClaw API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/jvsteiner/skills/uniclaw-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npx, tsx, and an existing Unicity wallet configured outside this skill.]

## Skill Version(s):

0.1.19 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
