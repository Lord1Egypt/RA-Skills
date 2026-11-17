## Description:

Generates stock investment analysis reports, financial charts, investment journal content, alerts, and natural-language investment assistant responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuritu](https://clawhub.ai/user/wuritu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate pre-market, post-market, weekly, and individual-stock reports, render supporting market charts, maintain investment logs, configure alerts, and answer follow-up investment questions. Outputs are informational and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill may store sensitive investment records in persistent memory without enough scoping or cleanup controls.

Mitigation: Require explicit confirmation before memory writes, define retention and cleanup expectations, and avoid storing account credentials or unnecessary personal financial details.

Risk: The security review says the skill may modify agent-level instructions, create recurring scheduled jobs, and send reports through channels.

Mitigation: Require explicit confirmation for cron jobs, instruction changes, and channel delivery; review schedules and recipients before enabling them.

Risk: The security review calls for verifying the external stock_data_adapter source.

Mitigation: Confirm the adapter package or local source before use and restrict access to the required STOCK_DATA_API_KEY.

Risk: The security review identifies dashboard HTML injection as an issue before use in shared or untrusted environments.

Mitigation: Sanitize dashboard data before rendering and avoid injecting untrusted strings into HTML.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuritu/skills/stock-reporting-interaction)
- [Publisher profile](https://clawhub.ai/user/wuritu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, generated chart files, dashboard HTML, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and STOCK_DATA_API_KEY for stock data access.]

## Skill Version(s):

1.0.0 (source: server release metadata and openclaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
