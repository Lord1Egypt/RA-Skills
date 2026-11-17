## Description:

Connect your agent to pre-computed market context that improves reasoning and reduces token usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tickerdb](https://clawhub.ai/user/tickerdb)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and market-monitoring agents use this skill to retrieve categorical market snapshots, search assets by derived state, manage TickerDB watchlists, configure webhooks, and set up scheduled market checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a TickerDB API key and can help users create or access an account during setup.

Mitigation: Install only if users are comfortable storing a TickerDB API key, and keep the key in the configured secret store rather than pasting it into unrelated prompts.

Risk: The skill can manage persistent watchlists, webhooks, and scheduled market checks through authenticated API calls.

Mitigation: Review requested watchlist, webhook, and schedule changes before relying on them, especially when slash commands are used for direct execution.

Risk: Market context can be misread as investment advice even though the artifact says the data is factual and not predictive.

Mitigation: Treat outputs as categorical market context and verify important decisions with appropriate financial analysis or advice.

## Reference(s):

- [TickerDB homepage](https://tickerdb.com)
- [TickerDB ClawHub skill page](https://clawhub.ai/tickerdb/skills/tickerdb)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with JSON examples, API request guidance, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TICKERDB_KEY for authenticated API access; may guide account setup, watchlist changes, webhook registration, and scheduled checks.]

## Skill Version(s):

0.1.97 (source: server release metadata; artifact frontmatter lists 0.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
