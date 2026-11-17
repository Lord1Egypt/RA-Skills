## Description:

Fetch real-time stock quotes from Yahoo Finance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noypearl](https://clawhub.ai/user/noypearl)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to fetch current quote data for one or more stock symbols from Yahoo Finance and return normalized JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticker symbols requested through the skill are sent to Yahoo Finance.

Mitigation: Use only ticker symbols appropriate for third-party processing and restrict outbound traffic to the Yahoo quote endpoint when required.

Risk: Quote fields can be null when Yahoo Finance does not return data for a requested symbol.

Mitigation: Check for null price, change, currency, and market state fields before using the returned JSON in downstream decisions.

## Reference(s):

- [Yahoo Finance quote endpoint](https://query1.finance.yahoo.com/v7/finance/quote)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Normalized JSON array of quote objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes null fields for symbols Yahoo Finance does not return.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata; package.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
