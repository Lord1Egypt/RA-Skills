## Description:

Polymarket prediction market trading for agents that can create a wallet, browse markets, place bets, manage positions, and withdraw funds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glitch003](https://clawhub.ai/user/glitch003)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to let an agent manage a Polymarket wallet, inspect prediction markets, trade within configured policies, monitor positions, redeem resolved markets, and withdraw USDC.e.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables autonomous prediction-market trading and withdrawals, which can give an agent high-impact financial authority.

Mitigation: Claim the wallet, configure strict spending and approval policies, keep balances limited, and monitor positions before allowing trading.

Risk: An unclaimed wallet may operate before human policy controls are configured.

Mitigation: Claim the wallet and set policies before funding it; avoid leaving funds in an unclaimed wallet.

Risk: The documented commands use `@vincentai/cli@latest`, so command behavior can change as the package changes.

Mitigation: Pin and review the CLI version before deployment.

Risk: Re-link tokens or scoped API keys may be exposed if pasted into ordinary chat.

Mitigation: Share re-link tokens only when that exposure is acceptable, consume them immediately, and revoke or rotate credentials from the Vincent frontend when needed.

## Reference(s):

- [Vincent homepage](https://heyvincent.ai)
- [ClawHub skill page](https://clawhub.ai/glitch003/skills/vincentpolymarket)
- [Publisher profile](https://clawhub.ai/user/glitch003)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use @vincentai/cli and return JSON for wallet, market, order, holding, trade, redemption, and withdrawal operations.]

## Skill Version(s):

1.0.70 (source: ClawHub release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
