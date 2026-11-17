## Description:

Analyze any Solana wallet's trading history for win rate, realized PnL, trader type, and copy-trade rating.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ultranumblol](https://clawhub.ai/user/ultranumblol)

### License/Terms of Use:

MIT

## Use Case:

Developers, copy traders, and smart money analysts use this skill to evaluate Solana wallet trading history before deciding whether to follow a wallet's trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The paid API path documents a mutable npx payment command and sends wallet analysis requests over network services.

Mitigation: Use a pinned and reviewed payment client, confirm each paid request before sending a wallet address, and avoid running the payment command in a privileged environment.

Risk: Self-hosted deployments depend on external Solana and Helius APIs and require a Helius API key.

Mitigation: Protect the API key, pin dependencies, validate or restrict FACILITATOR_URL, and review network endpoints before deployment.

Risk: The demo endpoint can perform wallet analysis without payment enforcement in the artifact behavior.

Mitigation: Add rate limits or payment checks to the demo endpoint if production access should be paid.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ultranumblol/skills/wallet-pnl)
- [Publisher profile](https://clawhub.ai/user/ultranumblol)
- [Project homepage](https://github.com/ultranumblol/wallet-pnl)
- [Project support](https://github.com/ultranumblol/wallet-pnl/issues)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON response examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces wallet analysis summaries including trader type, copy rating, trade counts, win rate, realized PnL in SOL, top traded tokens, and recent trades.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
