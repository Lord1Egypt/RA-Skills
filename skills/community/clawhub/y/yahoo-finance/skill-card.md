## Description:

Get stock prices, quotes, fundamentals, earnings, options, dividends, and analyst ratings using Yahoo Finance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajanraj](https://clawhub.ai/user/ajanraj)

### License/Terms of Use:


## Use Case:

Developers, analysts, and external users can use this skill to retrieve market quotes, company fundamentals, earnings, dividends, options chains, historical prices, comparisons, and symbol search results from Yahoo Finance through a CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation asks users to run remote installer commands for uv.

Mitigation: Prefer installing uv through a trusted package manager or a verified release before using the skill.

Risk: The evidence security summary reports that the actual yf CLI script is not included for review.

Mitigation: Do not run global symlink or first-run dependency steps until the missing script and its exact dependencies are available for review.

Risk: Yahoo Finance may rate limit requests or return no data for some symbols or security types.

Mitigation: Retry later after rate limits, verify symbols with search, and treat unavailable fields as expected data-source limitations.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with CLI commands and tabular financial data output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses yfinance and uv; no API key is described as required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
