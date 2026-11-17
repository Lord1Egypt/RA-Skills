## Description:

Autonomous AI trading agent for Simul8or, a live market simulator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[day-trading-simulator](https://clawhub.ai/user/day-trading-simulator)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to run an autonomous agent that watches simulated market data, manages a watchlist, places simulated long or short trades, and reports performance in Simul8or.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent autonomous trading can run repeatedly through PM2 startup and OpenClaw cron.

Mitigation: Use an isolated account or environment and avoid enabling PM2 startup or recurring cron until the behavior is reviewed.

Risk: Global npm packages are installed without pinned versions.

Mitigation: Pin and verify package versions before installation.

Risk: The skill uses an API key and may publish an account-linked performance profile.

Mitigation: Treat the API key and public profile as account-linked information, scope access appropriately, and rotate credentials when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/day-trading-simulator/skills/simul8or-trader)
- [Simul8or](https://simul8or.com)
- [Simul8or Setup Guide](https://simul8or.com/OpenClawLanding.php)
- [Simul8or Leaderboard](https://simul8or.com/OpenClawTrading.php)
- [Yahoo Finance Market Gainers](https://finance.yahoo.com/markets/stocks/gainers/)
- [Yahoo Finance Crypto Markets](https://finance.yahoo.com/markets/crypto/all/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Text]

**Output Format:** [Markdown with bash, JSON, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SIMUL8OR_API_KEY and local market, command, and price-history files when activated.]

## Skill Version(s):

1.0.3 (source: artifact/SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
