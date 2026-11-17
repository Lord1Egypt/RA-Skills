## Description:

Real-time BTC Orderbook Imbalance tracking for professional traders to detect high-conviction whale activity before it hits the tape.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmstudio667-commits](https://clawhub.ai/user/tmstudio667-commits)

### License/Terms of Use:


## Use Case:

External traders and market-monitoring agents use this skill to run a BTC order book imbalance monitor for OKX and Binance and surface high-conviction whale activity alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented run command uses an unpinned npx package.

Mitigation: Verify that openclaw is the expected official package and run a pinned audited version in a least-privileged environment before installation or execution.

Risk: Trading signals and whale-activity claims may be incorrect, incomplete, or unsuitable for a user's trading strategy.

Mitigation: Treat outputs as informational market-monitoring signals and review them with independent risk controls before making trading decisions.

Risk: The skill charges 0.25 USDC via x402 per use.

Mitigation: Confirm the fee, currency, and Base network payment details before running the skill.

## Reference(s):

- [Whale Pulse Monitor ClawHub listing](https://clawhub.ai/tmstudio667-commits/skills/whale-pulse-monitor)
- [System Architect Zero ClawHub profile](https://clawhub.ai/user/tmstudio667-commits)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market-monitoring alerts and informational trading signals; access costs 0.25 USDC per use via x402.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
