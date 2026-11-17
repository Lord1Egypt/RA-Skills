## Description:

Helps agents retrieve and explain TickDB market prices, historical data, company financials, and API key subscription status across supported markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tickdb](https://clawhub.ai/user/tickdb)

### License/Terms of Use:

MIT-0

## Use Case:

Traders, analysts, and developers use this skill to query supported market quotes, historical prices, financial fundamentals, and their own API key subscription details through TickDB.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API requests use credentials and may expose a formal key if pasted into a shared transcript.

Mitigation: Provide a formal key only when needed, preferably through a configured secret, and do not include it in shared transcripts or saved output.

Risk: The skill checks ClawHub for updates on first use and suggests an unpinned latest-version installation command.

Mitigation: Expect the version-check request and review the suggested update command before running it.

## Reference(s):

- [TickDB API documentation](https://docs.tickdb.ai)
- [API key subscription reference](references/apikeys.md)
- [API errors reference](references/errors.md)
- [Financial fundamentals reference](references/fundamentals.md)
- [ClawHub skill listing](https://clawhub.ai/tickdb/skills/tickdb-market-data)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown market-data summaries and optional API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on API key permissions, quotas, and data availability.]

## Skill Version(s):

1.1.1 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
