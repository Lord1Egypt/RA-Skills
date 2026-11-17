## Description:

This skill reads Tonghuashun Investment Ledger portfolio, watchlist, and trade data, then generates portfolio analysis reports with sector distribution, risk alerts, and threshold monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qcrcherry](https://clawhub.ai/user/qcrcherry)

### License/Terms of Use:

MIT-0

## Use Case:

External users with Tonghuashun Investment Ledger accounts use this skill to collect holdings and trade records from an authenticated browser session and generate local Markdown and JSON portfolio reports plus risk-monitoring alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an authenticated browser session and may read Tonghuashun account holdings, trades, and relevant 10jqka cookies.

Mitigation: Run it only in a dedicated Chrome profile or session and review Chrome remote-debugging access before use.

Risk: The skill stores sensitive financial data locally under data/ and memory/.

Mitigation: Protect those directories, clean retained files when no longer needed, and avoid sharing generated reports without review.

Risk: Cron examples can repeatedly collect account data and retain reports.

Mitigation: Enable scheduled runs only after reviewing the data collection frequency, retention behavior, and account-session exposure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qcrcherry/skills/tzzb-analyzer)
- [qcrcherry publisher profile](https://clawhub.ai/user/qcrcherry)
- [Tonghuashun Investment Ledger](https://tzzb.10jqka.com.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON data files, shell command guidance, and local configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include portfolio holdings, trade records, risk alerts, daily reports, and optional Feishu-formatted JSON.]

## Skill Version(s):

2.4.0 (source: server release evidence; artifact frontmatter 2.0.0 and pyproject.toml 2.1.0 differ)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
