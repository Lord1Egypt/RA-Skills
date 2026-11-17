## Description:

Autonomous Hyperliquid trading agent for smart-money signals, market analysis, backtesting, and creation or operation of automated trading agents with optional human-in-the-loop trade approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phutt-bwai](https://clawhub.ai/user/phutt-bwai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze Hyperliquid and Polymarket signals, configure trading agents, review HITL trade plans, and execute or manage trading actions through the bundled CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent trading agents, enable automated execution, open or close positions, withdraw funds, and run trading backtests.

Mitigation: Use human-in-the-loop mode first, require fresh user approval before financial commands, verify agent IDs and wallet addresses from current command output, and execute one consequential action at a time.

Risk: Telegram setup can transmit bot credentials to ZoneIn and the artifact documentation under-discloses sensitive data sharing.

Mitigation: Avoid pasting bot tokens into logged shells when possible, rotate exposed tokens, and review Telegram configuration before enabling notifications or approvals.

Risk: Trading signals, leverage, and automated execution can produce financial losses.

Mitigation: Use conservative sizing, validate stop-loss and take-profit settings, review leverage-specific stop-loss guidance, and do not rely on signals as guaranteed outcomes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phutt-bwai/skills/zonein)
- [ZoneIn Homepage](https://zonein.xyz)
- [ZoneIn App](https://app.zonein.xyz)
- [ZoneIn API Docs](https://mcp.zonein.xyz/docs)
- [OpenClaw](https://openclaw.io)
- [Commands Reference](references/COMMANDS.md)
- [Data Sources Reference](references/DATA_SOURCES.md)
- [Agent Configuration Reference](references/AGENT_CONFIG.md)
- [Trigger Conditions Reference](references/TRIGGER_CONDITIONS.md)
- [Operational Workflows Reference](references/WORKFLOWS.md)
- [Zonein Data Schema Reference](references/schema.md)
- [Zonein Trading Strategy Reference](references/strategy.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with CLI commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and ZONEIN_API_KEY; financial actions require explicit confirmation before gated commands execute.]

## Skill Version(s):

2.3.8 (source: ClawHub release metadata; artifact frontmatter reports 2.3.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
