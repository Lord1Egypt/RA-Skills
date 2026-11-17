## Description:

Monitors custom stock pools with real-time quotes, technical indicator analysis, trend signals, position tracking, and report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xsqorange](https://clawhub.ai/user/xsqorange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to monitor A-share and Hong Kong watchlists or positions, run technical analysis, manage local portfolio records, and draft scheduled market reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive portfolio and trade records may be stored under ~/.openclaw or included in scheduled Feishu reports.

Mitigation: Review and redact local portfolio files before sharing reports, verify the Feishu destination, and disable automated delivery when it is not needed.

Risk: Automated signals and generated market reports may be mistaken for investment advice.

Mitigation: Treat outputs as informational analysis, keep a human review step, and confirm prices and trading decisions with authoritative sources.

Risk: The documented dependency workaround may weaken environment hygiene.

Mitigation: Avoid the pip install workaround noted by security guidance unless the publisher fixes it and dependencies have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xsqorange/skills/stock-monitor-xsq)
- [Command reference](references/commands.md)
- [Configuration reference](references/config.md)
- [Indicator and workflow reference](references/index.md)
- [Scheduled task reference](references/scheduled-tasks.md)
- [Troubleshooting reference](references/troubleshooting.md)
- [Report templates](reports/templates.md)
- [Scheduled report prompts](reports/prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, CLI text or JSON output, and local JSON configuration files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include market data, technical indicators, watchlist status, position summaries, alerts, and scheduled report content.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
