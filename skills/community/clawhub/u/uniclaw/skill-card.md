## Description:

Trade on UniClaw prediction markets, browse markets, place orders, and manage positions with UCT tokens on the Unicity network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvsteiner](https://clawhub.ai/user/jvsteiner)

### License/Terms of Use:


## Use Case:

External agents and developers use this skill to interact with UniClaw prediction markets, including account registration, market discovery, order placement, portfolio review, deposits, and withdrawals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move UCT tokens through deposit and withdrawal commands and can place prediction-market orders.

Mitigation: Use only funds you are willing to risk, preferably on testnet, and personally verify amounts, markets, prices, quantities, and withdrawal destinations before executing commands.

Risk: The skill reads wallet secrets from the configured Unicity wallet and signs API requests.

Mitigation: Review wallet and private-key handling before installation, keep wallet files protected, and avoid running the skill with production wallet material unless the deployment has been approved.

Risk: Changing the server endpoint can direct signed requests or token transfers to a custom service.

Mitigation: Confirm the `UNICLAW_SERVER` endpoint before use and avoid custom or plaintext endpoints unless they are explicitly trusted.

## Reference(s):

- [UniClaw API Reference](references/api.md)
- [UniClaw skill page](https://clawhub.ai/jvsteiner/skills/uniclaw)
- [Default UniClaw API endpoint](https://api.uniclaw.app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npx, tsx, and a configured Unicity wallet.]

## Skill Version(s):

0.2.1 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
