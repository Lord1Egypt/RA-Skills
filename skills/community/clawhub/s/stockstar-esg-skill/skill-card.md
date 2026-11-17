## Description:

Queries StockStar ESG rating data for A-share and Hong Kong-listed companies, including company lookup, rating details, multi-stock comparison, and provider rating lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stockstar1996](https://clawhub.ai/user/stockstar1996)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to look up, compare, and summarize ESG ratings for A-share and Hong Kong-listed companies from StockStar-sourced rating data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock names, codes, and search terms are sent to public financial-data endpoints.

Mitigation: Use the skill for public market queries and avoid entering sensitive internal watchlists or confidential research terms.

Risk: Broad ESG-related triggers may activate during general ESG discussions.

Mitigation: Confirm that the user wants StockStar ESG data before running lookups in ambiguous conversations.

Risk: External ESG endpoints can return unavailable, incomplete, or dated rating fields.

Mitigation: Present ratings with their source and date fields, and leave missing provider fields unavailable rather than filling gaps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stockstar1996/skills/stockstar-esg-skill)
- [StockStar ESG data source](https://esg.stockstar.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [JSON from the CLI for agent parsing, with concise Chinese Markdown summaries for users]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-stock lookups, detail views, comparisons of up to five stocks, and paged provider lists of 20 records.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
