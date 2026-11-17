## Description:

Vantage is an autonomous trading agent for Hyperliquid perpetual futures that runs a signal-to-execution loop with funding, momentum, THORChain volume signals, Kelly sizing, paper mode, setup validation, and signed live order execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morebetterclaw](https://clawhub.ai/user/morebetterclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure and run a local Hyperliquid perpetual futures trading agent, first in paper mode and then, after review, in live mode with user-provided wallet credentials and trading limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live risk checks can use a wallet address that is not proven to match the private key signing real orders.

Mitigation: Do not run live mode until the wallet address used for balance and position checks is enforced to match the signing key; run the setup validator and confirm the match before any funded use.

Risk: Live mode can place real perpetual futures orders using a private key.

Mitigation: Use paper mode first, keep only limited funds under the signing key, set conservative trading limits, and protect the .env file containing credentials.

Risk: OpenAI fallback can send trading context to an external cloud API when enabled.

Mitigation: Disable the OpenAI fallback when trading context should stay local, and prefer local Ollama or rule-based decisions for private workflows.

Risk: Dependency issues may affect a live trading environment.

Mitigation: Review and update flagged dependencies before live deployment.

## Reference(s):

- [Vantage ClawHub listing](https://clawhub.ai/morebetterclaw/skills/vantage)
- [MoreBetter Studios products](https://morebetterstudios.com/products)
- [Hyperliquid Info API documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)
- [THORChain THORNode endpoint](https://thornode.ninerealms.com)
- [THORChain Midgard endpoint](https://midgard.ninerealms.com/v2)
- [Ollama](https://ollama.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may lead to paper or live trading workflows; live mode requires a private key, wallet address, and explicit trading limits.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
