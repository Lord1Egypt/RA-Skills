## Description:

tushare turns Chinese natural-language financial data requests into Tushare workflows for data retrieval, cleaning, comparison, filtering, export, and brief analysis across equities, indexes, ETFs, funds, financials, valuation, capital flows, disclosures, news, sectors, themes, and macro data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lidayan](https://clawhub.ai/user/lidayan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn Chinese-language financial research requests into Tushare data pulls, concise market summaries, comparison tables, and CSV or parquet exports. It is intended for research workflows over market, company, fund, news, sector, capital-flow, and macroeconomic data, not for trading execution or personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Tushare token and makes network calls to Tushare.

Mitigation: Install and run it only when sharing that token with the agent and allowing Tushare network access is acceptable.

Risk: Broad data pulls or exports can write large local CSV or parquet files.

Mitigation: Review requested ranges and output locations before running broad exports, and require explicit instructions before writing local data files.

Risk: Financial summaries can be mistaken for investment advice.

Mitigation: Use the skill for data research and summaries, and keep trading decisions or advisory conclusions outside the skill's scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lidayan/skills/tushare-data)
- [Tushare token registration](https://tushare.pro/register)
- [Tushare API interface list](references/数据接口.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with optional tables, Python snippets, shell commands, and CSV or parquet file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local data exports and retrieval metadata such as interface name, request parameters, pull time, row count, field list, and failed segments.]

## Skill Version(s):

1.1.19 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
