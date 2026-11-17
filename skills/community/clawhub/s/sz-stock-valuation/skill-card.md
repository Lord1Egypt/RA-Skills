## Description:

A stock valuation lookup for A-share and Hong Kong equities that returns valuation metrics, fair-price estimates, margin of safety, and under/fair/overvaluation labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenfei619](https://clawhub.ai/user/chenfei619)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query supported A-share and Hong Kong stock codes and generate informational valuation summaries. The output is useful for financial research workflows, but it is not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried stock codes are sent to tz.smxqx.tech with either a user-provided token or the bundled shared public token.

Mitigation: Use a scoped STOCK_VALUATION_AUTH token when available and avoid querying sensitive watchlists through the shared public token.

Risk: Valuation output may be mistaken for investment advice.

Mitigation: Present results as informational research, keep the disclaimer visible, and require human judgment before any financial decision.

Risk: Broad finance triggers may activate the skill for ambiguous valuation or investment prompts.

Mitigation: Confirm the intended stock code and market suffix before running the valuation query.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenfei619/skills/sz-stock-valuation)
- [API returned fields](references/api_fields.md)
- [Stock code format](references/stock_code_format.md)
- [Valuation API endpoint](https://tz.smxqx.tech/api/stock/valuation/detail)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Structured Markdown report with valuation tables and a disclaimer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a supported stock code and may use STOCK_VALUATION_AUTH or a bundled shared public token.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
