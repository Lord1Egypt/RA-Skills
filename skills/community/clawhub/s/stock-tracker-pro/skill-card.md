## Description:

Stock Tracker Pro lets an agent manage a stock watchlist and retrieve Yahoo Finance quote data with recent news for requested symbols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongbhuang](https://clawhub.ai/user/hongbhuang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to add, remove, list, and inspect stock symbols in a watchlist. It retrieves quote, valuation, volume, dividend, and recent-news information for requested symbols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock symbols and company names can be sent to external services for quote and news lookup.

Mitigation: Use the skill only where Yahoo Finance and Tavily-style external searches are acceptable for the watchlist data being queried.

Risk: The news lookup invokes a separate local Tavily search script outside this package.

Mitigation: Review and trust the referenced local search skill before enabling news lookup behavior, or restrict that behavior during deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hongbhuang/skills/stock-tracker-pro)
- [Yahoo Finance chart endpoint](https://query1.finance.yahoo.com/v8/finance/chart/)
- [Yahoo Finance quote endpoint](https://query1.finance.yahoo.com/v7/finance/quote)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Markdown guidance with inline bash commands and plain text script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains a JSON stock watchlist and returns up to three news results when available.]

## Skill Version(s):

1.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
