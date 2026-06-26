## Description: <br>
Stock Monitor helps an agent monitor custom A-share and Hong Kong stock watchlists, fetch market quotes, compute technical indicators, track positions and trades, and draft recurring analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xsqorange](https://clawhub.ai/user/xsqorange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to configure stock watchlists, local portfolio records, scheduled monitoring jobs, and Markdown-style market reports for A-share and Hong Kong holdings. It is intended for monitoring and analysis support, not as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores watchlists, positions, costs, and trade history under ~/.openclaw, which can expose sensitive portfolio data on shared or poorly protected machines. <br>
Mitigation: Use appropriate local file permissions, avoid entering sensitive holdings on shared systems, and back up or delete local JSON files according to the user's data-handling requirements. <br>
Risk: Scheduled report prompts can send generated reports to a Feishu or group-chat recipient without a clear confirmation step. <br>
Mitigation: Verify the configured recipient before enabling cron jobs, and disable automatic sending when reports should remain local. <br>
Risk: Market data, technical indicators, and generated analysis can be incomplete, delayed, or misleading if used as trading advice. <br>
Mitigation: Treat outputs as informational monitoring aids and verify price, position, and trade decisions against authoritative market or brokerage sources. <br>


## Reference(s): <br>
- [Skill Overview](artifact/SKILL.md) <br>
- [Command Reference](artifact/references/commands.md) <br>
- [Configuration Reference](artifact/references/config.md) <br>
- [Reference Index](artifact/references/index.md) <br>
- [Scheduled Tasks](artifact/references/scheduled-tasks.md) <br>
- [Troubleshooting](artifact/references/troubleshooting.md) <br>
- [Report Prompt Templates](artifact/reports/prompts.md) <br>
- [Report Templates](artifact/reports/templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xsqorange/xsqorange-stock-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, CLI command output, and JSON configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include stock quotes, technical indicator summaries, position and trade summaries, alerts, and scheduled report text.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata and SKILL.md body) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
