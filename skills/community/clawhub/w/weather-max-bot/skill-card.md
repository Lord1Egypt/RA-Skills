## Description:

Weather Max Bot is a Simmer-based prediction-market skill package that queries weather markets and includes guidance and code for trading through Simmer, including a Polymarket BTC Up/Down strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pasichnuk969](https://clawhub.ai/user/pasichnuk969)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to orient agents to Simmer prediction-market workflows, query weather markets, and configure or run prediction-market trading behavior. The package should be reviewed carefully before live trading because server evidence flags inconsistent identities and bundled real-money Polymarket automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes an automated real-money Polymarket BTC trading strategy.

Mitigation: Start in dry-run mode, review the strategy output and configuration, and enable live trading only with explicit limits and monitoring.

Risk: The package handles trading credentials and may use wallet credentials for live external-wallet trading.

Mitigation: Use managed or dedicated low-balance wallets, keep credentials in environment variables, and review SDK version pinning before exposing keys.

Risk: Cron or quiet mode can make repeated trading harder to observe.

Mitigation: Avoid unattended quiet cron until dry-run behavior, budgets, exits, and external monitoring are verified.

Risk: Server evidence reports inconsistent identities across the target metadata, artifact metadata, and bundled strategy files.

Mitigation: Confirm the installed package identity, publisher profile, and intended skill behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pasichnuk969/skills/weather-max-bot)
- [Publisher profile](https://clawhub.ai/user/pasichnuk969)
- [Simmer homepage](https://simmer.markets)
- [Simmer documentation](https://docs.simmer.markets)
- [Simmer full reference for agents](https://docs.simmer.markets/llms-full.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration examples, and executable code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market lists, dry-run output, position summaries, trade status, and configuration guidance when executed.]

## Skill Version(s):

1.0.1 (source: server evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
