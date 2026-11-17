## Description:

Query alternative financial data from Quiver Quantitative (Congress trading, Lobbying, Government Contracts, Insider transactions). Use this to track politician stock trades or unconventional market signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stuhorsman](https://clawhub.ai/user/stuhorsman)

### License/Terms of Use:


## Use Case:

External users, developers, and analysts use this skill to query Quiver Quantitative alternative financial datasets, including congressional trading, lobbying, government contracts, and insider transactions, as JSON for market-signal analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an authenticated Quiver Quantitative API key to query financial-data records.

Mitigation: Provide only a Quiver Quantitative API key intended for this skill, preferably scoped or revocable if Quiver supports that.

Risk: Returned records may be used as market signals but are not investment advice.

Mitigation: Review the JSON results and corroborate them with other sources before using them for financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stuhorsman/skills/quiver)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON]

**Output Format:** [JSON array of records emitted by command-line queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QUIVER_API_KEY; commands may return an empty JSON array when no matching records are available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
