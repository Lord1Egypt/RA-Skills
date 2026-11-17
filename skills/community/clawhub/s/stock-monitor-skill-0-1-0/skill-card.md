## Description:

Stock Monitor Skill provides a Chinese-market stock, ETF, and gold alert monitor with cost-percentage, price-change, volume, moving-average, RSI, gap, and trailing-stop rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiahl0910](https://clawhub.ai/user/jiahl0910)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to configure and run market alerts for watched Chinese equities, ETFs, and London gold. Its generated alerts and suggestions should be treated as informational signals, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hardcoded watchlist and cost values may not match the user's actual holdings.

Mitigation: Review and edit the watchlist, cost basis, and thresholds before starting the monitor.

Risk: The background monitor continues running after ./control.sh start until it is explicitly stopped.

Mitigation: Use ./control.sh status, ./control.sh log, and ./control.sh stop to inspect and terminate the daemon.

Risk: Financial alerts and generated suggestions may be inaccurate or unsuitable for a user's investment decisions.

Mitigation: Treat alerts as informational signals and verify them against independent analysis before trading.

Risk: Market-data and analysis output may be exposed to transport or text-handling risks if extended without care.

Mitigation: Prefer HTTPS-only data sources and escape notification text when relying on analysis output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiahl0910/skills/stock-monitor-skill-0-1-0)
- [Publisher profile](https://clawhub.ai/user/jiahl0910)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Python configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces alert text, configuration guidance, and local control commands for starting, stopping, checking, and logging a background monitor.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
