## Description:

小石金融数据平台 helps agents connect to Xiaoshi public financial-data APIs for authenticated market data, point-in-time macro and event research, financial statements, factors, backtests, and quantitative research without trade execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pilot1799](https://clawhub.ai/user/pilot1799)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and financial researchers use this skill to log in to Xiaoshi and retrieve market, macro, event, financial, factor, and historical data for reports, backtests, and API-driven quantitative research. It is not for investment advice, trading, order placement, or account actions beyond authorized authentication and credential recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Use sends the user's email and financial-data queries to Xiaoshi.

Mitigation: Confirm the user is comfortable sharing that information and send only query parameters needed for the requested task.

Risk: API keys, verification codes, and session tokens are sensitive credentials.

Mitigation: Store credentials only in a protected secret store, never echo or write them to ordinary files or reports, and keep them session-only when protected storage is unavailable.

Risk: Financial research outputs may be mistaken for investment advice or trade instructions.

Mitigation: Present outputs as data retrieval and research, distinguish verified data from model inference, and do not execute trades or place investment orders.

Risk: Rate-limit or bulk-download protections can be bypassed accidentally by repeated retries.

Mitigation: Honor Retry-After values, switch to declared bulk-download flows when required, and stop rather than cycling accounts, IPs, or repeated registrations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pilot1799/skills/xiaoshi-financial-data-platform)
- [Xiaoshi Homepage](https://www.shizixi.com/)
- [Full Capability Routing](references/capabilities.md)
- [Data, PIT, Download, and Error Contracts](references/data-and-safety-contracts.md)
- [Host Compatibility and Degradation](references/host-compatibility.md)
- [Registration and Login](references/registration-and-login.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown or structured JSON with optional code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve data provenance, time range, market, currency, unit, adjustment mode, as_of value, coverage, and revision metadata when relevant, and must not expose API keys, verification codes, session tokens, or full sensitive logs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
