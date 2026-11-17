## Description:

Stock Daily Analysis helps agents analyze A-share, Hong Kong, and U.S. stocks with technical indicators, trend signals, and optional LLM-generated decision reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robottk](https://clawhub.ai/user/robottk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to build daily stock watchlist workflows that fetch market data, calculate technical indicators, and produce decision-oriented reports. The artifact states that the analysis is not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and update scripts can pull and run changing GitHub code.

Mitigation: Review scripts before execution, avoid privileged accounts, and pin the upstream repository and Python dependencies for controlled deployments.

Risk: AI integrations can send stock symbols and technical-analysis data to external services.

Mitigation: Configure only approved AI providers or proxies, and avoid sending data that policy or users consider sensitive.

Risk: API keys and environment backups can be exposed through shared directories or unmanaged .env copies.

Mitigation: Keep API keys outside shared directories, restrict file permissions, and remove stale .env backups.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robottk/skills/stock-daily-analysis)
- [AkShare market data library](https://github.com/akfamily/akshare)
- [OpenClaw market-data skill](https://github.com/chjm-ai/openclaw-market-data)
- [Daily stock analysis project cited by artifact](https://github.com/ZhuLinsen/daily_stock_analysis)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and text reports with JSON-like stock analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include technical indicators, trend status, signal scores, LLM commentary, target prices, stop-loss values, and risk warnings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
