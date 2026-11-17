## Description:

A finance data research skill for A-shares, Hong Kong stocks, U.S. stocks, funds, futures, options, bonds, and macro data that maps user requests into Tushare-compatible data retrieval, cleaning, comparison, screening, and export workflows through the StockToday gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[usa2046](https://clawhub.ai/user/usa2046)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn Chinese natural-language financial research requests into StockToday/Tushare-compatible API calls, analysis summaries, tabular comparisons, and optional local exports. Typical tasks include market trend checks, financial statement snapshots, stock comparisons, sector and fund-flow reviews, announcement/news checks, macro data lookups, and reusable research scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tushare tokens and financial query history are routed through the StockToday gateway.

Mitigation: Use the skill only when this routing is acceptable, prefer a dedicated or limited token, and rotate any token previously used through the gateway.

Risk: The artifact documents HTTP backup gateways for financial API traffic.

Mitigation: Avoid the HTTP backup gateways and use HTTPS endpoints where possible.

Risk: The authoritative security verdict is suspicious and calls for careful review before installation.

Mitigation: Review the skill, gateway configuration, and token-handling posture before deploying it in a production agent.

## Reference(s):

- [StockToday Data Interface Reference](artifact/references/数据接口.md)
- [ClawHub Skill Page](https://clawhub.ai/usa2046/skills/stocktoday-py)
- [Publisher Profile](https://clawhub.ai/user/usa2046)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown summaries with concise tables, optional Python snippets, and optional CSV or parquet exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state the query interface, parameters, retrieval time, row count, fields, missing data, failed segments, and relevant data limitations.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata, artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
