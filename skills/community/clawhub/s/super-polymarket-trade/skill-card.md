## Description:

Access public Polymarket prediction market data for market search, odds monitoring, trend analysis, watchlists, alerts, resolution calendars, category digests, and local paper-trading simulation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to query public Polymarket markets, compare odds and movement, maintain local watchlists, and simulate prediction positions without wallet access or real trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market odds and movement summaries can be mistaken for financial advice or a complete view of market conditions.

Mitigation: Treat outputs as informational, verify important details against Polymarket or other sources, and do not use the skill to make real-money trades.

Risk: Watchlists, alerts, and paper-trading history are stored locally in ~/.polymarket/.

Mitigation: Review or remove local JSON files before sharing machines, logs, backups, or workspace snapshots.

Risk: Cron examples can repeatedly query the public Polymarket API.

Mitigation: Run scheduled checks only when user-directed, keep polling frequency reasonable, and monitor command failures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-polymarket-trade)
- [Polymarket](https://polymarket.com)
- [Polymarket API documentation](https://docs.polymarket.com)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [Step-by-Step Guide](https://telegra.ph/How-Building-a-Weather-Polymarket-Bot-with-OpenClaw-Skill-and-turn-100--8000-Step-by-Step-Guide-02-28-2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style terminal text with command examples and local JSON state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs market summaries, odds, volume, price movement, alerts, calendar entries, category digests, and simulated portfolio results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
