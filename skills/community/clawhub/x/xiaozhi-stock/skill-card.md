## Description:

小智A股分析引擎 provides multi-source Chinese A-share market quotes, individual stock analysis, market sentiment checks, sector scanning, quantitative screening, watchlist management, and monitoring alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[badboy2021123](https://clawhub.ai/user/badboy2021123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query Chinese A-share quotes, analyze individual stocks, assess market sentiment and sectors, generate stock-screening candidates, manage a watchlist, and create monitoring alerts. Its outputs are informational and should not be treated as personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Investment-oriented signals may be mistaken for personalized financial advice.

Mitigation: Use outputs only for informational stock analysis and retain clear risk disclaimers in user-facing responses.

Risk: Watchlists, cost basis, alert state, logs, and saved reports may be written locally.

Mitigation: Run the skill in a workspace where local persistence is expected, and review locally saved files before sharing or publishing the workspace.

Risk: Stock identifiers may be sent to market-data providers over plaintext HTTP.

Mitigation: Avoid sensitive watchlists where plaintext market-data requests are unacceptable, and review provider requests before enabling monitoring.

Risk: Optional package installs and automated alerting can increase operational exposure.

Mitigation: Verify and pin optional packages before installation, and enable cron, WeChat, or DingTalk-style alerts only with explicit destinations you control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/badboy2021123/skills/xiaozhi-stock)
- [Analysis methods reference](references/analysis-methods.md)
- [Data sources API reference](references/data-sources.md)
- [Technical timing score reference](references/technical-timing.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, formatted text cards, JSON from scripts, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local watchlist, alert state, logs, and saved reports when monitoring or report features are used; uses public market-data HTTP endpoints.]

## Skill Version(s):

1.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
