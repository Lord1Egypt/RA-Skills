## Description:

Fetch Chinese stock and futures market data via Tushare API, including stock quotes, futures data, company fundamentals, and macroeconomic indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wdblink](https://clawhub.ai/user/wdblink)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to retrieve Chinese equity, futures, company, and macroeconomic market data through Tushare-backed command-line helpers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A paid or sensitive Tushare token could be exposed if stored in a synced shell profile or shared configuration file.

Mitigation: Use a session export, a local environment file with restrictive permissions, or a secrets manager for TUSHARE_TOKEN.

Risk: Unpinned Python dependencies can change behavior across installations.

Mitigation: Install the skill dependencies in a virtual environment and pin package versions when deploying repeatable workflows.

Risk: Some Tushare endpoints may fail or return limited data when the token lacks the required account permissions.

Mitigation: Confirm Tushare account permissions before relying on a specific endpoint in production workflows.

## Reference(s):

- [Tushare Stock API Reference](references/stock_api.md)
- [Tushare Futures API Reference](references/futures_api.md)
- [Tushare Official Site](https://tushare.pro)
- [Tushare Stock Interface Documentation](https://tushare.pro/document/2?doc_id=14)
- [Tushare Futures Interface Documentation](https://tushare.pro/document/2?doc_id=134)
- [Tushare Registration](https://tushare.pro/register)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and command-line text or JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output depends on the selected Tushare endpoint, market symbol, date range, token permissions, and available Tushare data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
