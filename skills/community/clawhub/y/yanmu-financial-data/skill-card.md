## Description:

Yanmu Financial Data collects core financial metrics for a selected stock and comparable companies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoling7878-arch](https://clawhub.ai/user/caoling7878-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and financial analysts use this skill to collect stock quote data from Sina Finance and format built-in historical, forecast, valuation, and comparable-company metrics for supported A-share, Hong Kong, and U.S. tickers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock symbols are queried against Sina Finance for live prices.

Mitigation: Use the skill only when sending requested ticker symbols to Sina Finance is acceptable.

Risk: Bundled historical and estimate data may be incomplete, stale, or unsuitable for investment decisions.

Mitigation: Treat bundled data as demonstration or reference material and verify financial data against authoritative sources before relying on it.

Risk: The skill interface and output are Chinese-language only.

Mitigation: Use it in workflows where Chinese-language prompts and financial summaries are appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caoling7878-arch/skills/yanmu-financial-data)
- [Publisher profile](https://clawhub.ai/user/caoling7878-arch)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown summary or JSON financial data from a command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output; live quote lookups fall back to bundled static data when unavailable.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
