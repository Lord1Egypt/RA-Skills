## Description:

Provides agents with finance news search, stock screening, and market, company, financial, relationship, and operating data lookup based on East Money Miaoxiang data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jade-srgb](https://clawhub.ai/user/jade-srgb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask agents for current financial news, screen stocks by natural-language criteria, and retrieve market, company, financial, and relationship data for securities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a reusable default API key and instructs agents to use it when MX_APIKEY is not set.

Mitigation: Use a user-controlled, scoped MX_APIKEY and avoid relying on the bundled default key.

Risk: Queries are sent to external finance API endpoints.

Mitigation: Do not submit confidential trading strategies, client details, account data, or proprietary research terms unless approved for external processing.

Risk: Broad historical or large-range data requests can produce excessive output.

Mitigation: Constrain symbols, metrics, date ranges, and page sizes before requesting high-volume financial data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jade-srgb/skills/stock-mx)
- [Combined skill guide](artifact/SKILL.md)
- [mx_search documentation](artifact/mx_search.md)
- [mx_select_stock documentation](artifact/mx_select_stock.md)
- [mx_data documentation](artifact/mx_data.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and tables, optional CSV-style stock screening output, and curl examples for API calls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MX_APIKEY for API access. Large historical or broad-market queries can produce long responses.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
