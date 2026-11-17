## Description:

Use for deterministic ICT market scans, validated intraday order-plan tickets, structure reads, macro bias boards, the local Trading Universe dashboard, and automatic candle-replayed trade tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[illimitedenterprise](https://clawhub.ai/user/illimitedenterprise)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users and developers use this skill to produce deterministic trading-analysis order-plan cards, structure reads, macro bias summaries, watchlist scans, and local dashboard views. It supports educational market analysis and trade tracking, but does not place trades, connect to brokers, or provide position-sizing or leverage advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional reasoning providers can receive selected tickets or fundamentals grounding packs.

Mitigation: Enable only trusted providers, review provider terms, and leave reasoning disabled or use local CLI modes when trading context should remain local.

Risk: Saved reasoning API keys and runtime trading data are written under the local Trading Universe data directory.

Mitigation: Avoid Save key unless local file permissions are verified, protect the local data directory, and clear saved keys when they are not needed.

Risk: An untrusted launcher or shell environment could change the reasoning provider endpoint.

Mitigation: Launch the dashboard only from a trusted wrapper or shell and check the environment before enabling external reasoning providers.

Risk: Trading-analysis outputs could be mistaken for execution instructions or financial advice.

Mitigation: Review every generated order plan manually, confirm levels against the user's own data feed, and keep the documented no-broker, no-sizing, and not-financial-advice boundaries.

## Reference(s):

- [README](README.md)
- [ICT intraday playbook](references/playbook.md)
- [Trading Universe Dashboard reference](references/dashboard.md)
- [Asset map, watchlist, queries, sources](references/asset-map.md)
- [Wyckoff engine reference](references/wyckoff.md)
- [ClawHub skill page](https://clawhub.ai/illimitedenterprise/skills/trading-universe)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown cards and guidance, shell commands, configuration notes, and JSON from local CLI scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are informational order plans and dashboard guidance; the skill states that it does not place trades or provide position-sizing or leverage advice.]

## Skill Version(s):

1.8.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
