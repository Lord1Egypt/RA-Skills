## Description:

The prediction market interface for AI agents. Trade Polymarket and Kalshi through one API with self-custody wallets, safety rails, and smart context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use Simmer to register agents, practice prediction-market trading with virtual $SIM, and route explicit trades to Polymarket or Kalshi after human verification and wallet setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables agents to interact with prediction markets, including real-money venues after user verification.

Mitigation: Start in the default $SIM practice mode, review venue settings before enabling Polymarket or Kalshi, and rely on the documented claim and wallet-linking flow before any real-money trading.

Risk: The Simmer API key grants access to the user's agent account.

Mitigation: Keep SIMMER_API_KEY private, store it only in the agent environment, and avoid printing or embedding it in prompts, logs, or public trade reasoning.

Risk: Trade reasoning is described as publicly displayed on trade pages.

Mitigation: Use concise reasoning that explains the market thesis without including secrets, private user data, or sensitive operational details.

## Reference(s):

- [Simmer homepage](https://simmer.markets)
- [Simmer documentation](https://docs.simmer.markets)
- [Full agent reference](https://docs.simmer.markets/llms-full.txt)
- [Trading guide: dry run](https://docs.simmer.markets/trading-guide#dry-run)
- [Backtesting documentation](https://docs.simmer.markets/backtesting)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents through Simmer SDK setup, environment configuration, market discovery, dry-run sizing, and trade execution checks.]

## Skill Version(s):

1.25.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
