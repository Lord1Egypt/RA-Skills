## Description:

A 股大师 Pro helps agents monitor A-share holdings, generate market reviews, issue alerts, and screen trend candidates using QVeris AI market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seedew](https://clawhub.ai/user/seedew)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to track A-share portfolios, review intraday and closing market conditions, receive holding alerts, and generate trend-based stock screening output. The skill is financial-analysis support only and does not replace professional investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential exposure and sensitive financial data handling

Mitigation: Remove any exposed API key material, rotate affected credentials, and keep QVERIS_API_KEY and holdings data in user-controlled environment or secret storage.

Risk: Unpinned remote installation commands

Mitigation: Use pinned, verified releases or checksummed downloads instead of raw curl-based installation steps.

Risk: Shell command construction in scripts

Mitigation: Replace shell-interpolated command strings with argument-vector execution and strict parameter validation before running QVeris commands.

Risk: Dashboard escaping and rendered market data

Mitigation: Sanitize or encode dashboard content before insertion into HTML to reduce script-injection risk from local or API-derived data.

Risk: Scheduled monitoring may run API calls automatically

Mitigation: Make cron-style monitoring opt-in, document disable steps, and clearly explain API usage and logging behavior before enabling automation.

Risk: Financial analysis may be mistaken for investment advice

Mitigation: Keep the investment-risk disclaimer visible and require users to verify market data and decisions against authoritative sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seedew/skills/stock-master-pro)
- [QVeris AI data source](https://qveris.ai/?ref=y9d7PKgdPcPC-A)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, text alerts, JSON configuration examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may depend on QVERIS_API_KEY, local holdings configuration, scheduled runs, and QVeris market-data availability.]

## Skill Version(s):

0.0.1 (source: server release metadata and changelog, released 2026-03-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
