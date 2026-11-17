## Description:

Stock Query helps agents retrieve and format real-time market quotes, historical K-line data, and portfolio watchlist views for stocks, ETFs, mutual funds, and indexes across A-share, Hong Kong, and U.S. markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asfamilybank](https://clawhub.ai/user/asfamilybank)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer stock, fund, index, historical price, and watchlist valuation requests. It is intended for market-data lookup and formatting, not for cryptocurrency, futures, options, or foreign-exchange workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe input handling in shell-based portfolio and history commands may enable local code execution.

Mitigation: Review before installing and use only with trusted prompts until the shell/Python injection paths are fixed.

Risk: Portfolio data is stored in portfolio.csv and may be modified during explicit portfolio-management requests.

Mitigation: Keep portfolio.csv limited to stock codes, names, quantities, and reference prices; do not store credentials, API keys, tokens, or account passwords in it.

Risk: Queried symbols are sent to external market-data services.

Mitigation: Avoid querying sensitive or confidential watchlists if disclosure of symbols to external providers is unacceptable.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/asfamilybank/skills/stock-query)
- [Source repository listed in metadata](https://github.com/asfamilybank/stock-query)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Shell commands, Configuration guidance]

**Output Format:** [Markdown tables, JSON arrays or objects, CSV, and concise error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, iconv, and python3 on macOS or Linux; queried symbols may be sent to external market-data services.]

## Skill Version(s):

2.6.0 (source: server release metadata, skill.yaml, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
