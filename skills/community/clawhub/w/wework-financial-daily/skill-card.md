## Description:

Generates a daily financial analysis teaching report, saves an HTML version locally, uploads it for sharing, and sends a WeCom message with charts and technical-analysis summaries for BTC and AAPL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leozhang1431](https://clawhub.ai/user/leozhang1431)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to schedule daily finance teaching material that combines simulated BTC and AAPL data, charts, trend commentary, and WeCom delivery. It is suited for education and reporting workflows, not for investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded WeCom and MinIO credentials are exposed in the release artifact.

Mitigation: Revoke or rotate those values before use, then provide secrets through environment variables or a managed secret store.

Risk: Generated reports may be uploaded to a hard-coded public MinIO path.

Mitigation: Use private storage by default and share reports through short-lived, access-controlled links.

Risk: The scheduling guidance recommends elevated Windows task execution.

Mitigation: Run the scheduled task with the least-privileged account that can generate reports and send messages.

Risk: The generated BTC and AAPL values are simulated but could be mistaken for live market data.

Mitigation: Label reports as simulated unless the data source is replaced with a validated real market-data provider.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leozhang1431/skills/wework-financial-daily)
- [Cron setup guide](references/cron-setup.md)
- [Scheduled task configuration guide](README-定时任务配置.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, scheduled-task configuration, WeCom message content, and generated HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report content uses simulated market data unless the script is changed to use a real market-data source.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
