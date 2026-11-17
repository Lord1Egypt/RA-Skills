## Description:

Monitors custom A-share and Hong Kong stock pools, retrieves market quotes, analyzes technical indicators, prepares trend and signal alerts, and supports scheduled market reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xsqorange](https://clawhub.ai/user/xsqorange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor A-share and Hong Kong stock watchlists, manage holdings and trade records, run technical analysis, and generate market reports. Outputs should be treated as informational stock-monitoring support, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores watchlists, holdings, trades, and alert settings in local JSON files under ~/.openclaw.

Mitigation: Keep the ~/.openclaw stock JSON files private and review local file permissions before use.

Risk: Scheduled cron workflows can automatically post reports containing financial records and analysis to a Feishu group.

Mitigation: Use a local-only or preview workflow unless group delivery is intentional, and review the Feishu target before enabling scheduled announcements.

Risk: Some market data is fetched over unauthenticated HTTP, which can affect trust in generated reports.

Mitigation: Treat outputs as informational and verify important market data against trusted sources before acting on it.

Risk: The troubleshooting documentation includes a pip install command for json, which is part of Python's standard library.

Mitigation: Avoid installing json with pip; use the Python standard-library module.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xsqorange/skills/xsqorange-stock-monitor)
- [Commands Reference](artifact/references/commands.md)
- [Configuration Reference](artifact/references/config.md)
- [Reference Index](artifact/references/index.md)
- [Scheduled Tasks Reference](artifact/references/scheduled-tasks.md)
- [Troubleshooting Reference](artifact/references/troubleshooting.md)
- [Report Templates](artifact/reports/templates.md)
- [Cron Prompt Templates](artifact/reports/prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON configuration examples, and inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include watchlists, holdings, trades, technical indicators, news summaries, alerts, and operational recommendations.]

## Skill Version(s):

1.2.2 (source: server release metadata and SKILL.md body)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
