## Description:

Queries Questrade brokerage accounts and Canadian/US market data via the Questrade REST API for balances, positions, orders, executions, activities, Level 1 quotes, historical candles, and symbol search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josemiguelherrera](https://clawhub.ai/user/josemiguelherrera)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to inspect Questrade portfolios, orders, executions, account activity, and Canadian/US market data. With Questrade partner API access, the skill can also place or cancel orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: With Questrade partner API credentials, the skill can submit or cancel real brokerage orders.

Mitigation: Keep QUESTRADE_READ_ONLY=true unless trading access is intentionally required, review order summaries before confirming, and avoid --force for live accounts.

Risk: The skill handles sensitive brokerage account data and rotating OAuth refresh tokens.

Mitigation: Protect the ~/.openclaw credential files, do not share refresh tokens, and prefer practice mode when testing workflows.

Risk: Dependency versions are not fully pinned.

Mitigation: Use a pinned dependency set before deployment in controlled environments.

## Reference(s):

- [Questrade API Reference](references/api.md)
- [Questrade API Documentation](https://www.questrade.com/api/documentation/getting-started)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or table-formatted CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Questrade OAuth credentials and may write rotated tokens to local OpenClaw credential files.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
