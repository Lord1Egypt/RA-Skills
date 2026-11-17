## Description:

Fetches Superinvestors' 13F portfolio holdings and buy/sell activity from ValueSider.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laimiaohua](https://clawhub.ai/user/laimiaohua)

### License/Terms of Use:


## Use Case:

External users and finance-focused agents use this skill to retrieve ValueSider superinvestor 13F holdings and buy/sell activity, then summarize parsed portfolio and activity JSON for research-oriented questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime dependency versions may change behavior over time.

Mitigation: Install the skill in a locked virtual environment and pin requests and beautifulsoup4 versions before deployment.

Risk: Fetched public ValueSider pages can be unavailable, blocked, stale, or parsed incompletely.

Mitigation: Use the documented web-fetch-then-parse flow, show source URLs and filing period or update date when presenting results, and inspect parser output for missing fields.

Risk: Portfolio holdings and trading activity may be mistaken for investment advice.

Mitigation: Present results as sourced 13F portfolio data from ValueSider and avoid recommending buy or sell decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laimiaohua/skills/valuesider-superinvestor-data)
- [ValueSider](https://valuesider.com)
- [ValueSider Value Investors](https://valuesider.com/value-investors)
- [ValueSider Portfolio URL Pattern](https://valuesider.com/guru/{guru_slug}/portfolio)
- [ValueSider Activity URL Pattern](https://valuesider.com/guru/{guru_slug}/portfolio-activity)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown summaries with JSON parser output and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Parsed portfolio output includes summary and holdings; activity output includes recent buy/sell activity. Results depend on ValueSider page availability and parser coverage.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
