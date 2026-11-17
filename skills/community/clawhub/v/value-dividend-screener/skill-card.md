## Description:

Screen US equities for value and dividend quality using multi-factor scoring across P/E, P/B, dividend yield, and payout sustainability via the Finskills API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finskills](https://clawhub.ai/user/finskills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to screen US equities for undervalued dividend-paying stocks, compare dividend sustainability, and build income or dividend growth watchlists. It retrieves Finskills market data, applies value, income, and financial-health criteria, and returns ranked candidates with rationale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README install command is unpinned, which can make the installed contents depend on the current state of the remote source.

Mitigation: Install from a reviewed commit or release when possible and review the skill before deployment.

Risk: The skill sends stock symbols and screening requests to Finskills using the configured API key.

Mitigation: Use an intended Finskills API key, limit shared portfolio details to what is necessary, and confirm this data sharing is acceptable for the user's workflow.

Risk: The skill produces financial screening analysis that can be incomplete or stale if market data is delayed, unavailable, or plan-limited.

Mitigation: Treat results as screening output, confirm key metrics against authoritative sources, and avoid presenting the output as personalized investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/finskills/skills/value-dividend-screener)
- [Publisher profile](https://clawhub.ai/user/finskills)
- [Project homepage](https://github.com/finskills/value-dividend-screener)
- [Finskills API](https://finskills.net)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Markdown, Guidance]

**Output Format:** [Markdown report with ranked tables, score breakdowns, screening summaries, and concise rationale]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a Finskills API key and may require a Pro plan for financials, dividends, quotes, and recommendations.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
