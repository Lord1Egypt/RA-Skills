## Description:

A股和港股价值投资分析系统，基于《股市真规则》方法论提供护城河、财务健康、DCF估值、管理层、行业和投资决策分析框架。

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankski818](https://clawhub.ai/user/frankski818)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to structure value-investing research for A-share and Hong Kong-listed stocks, including financial health checks, moat review, DCF valuation, peer comparison, watchlist monitoring, and decision summaries. Its outputs should be treated as research aids, not personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Investment conclusions, target prices, and position guidance may be incomplete or misleading if treated as personalized financial advice.

Mitigation: Use the output as research support only, cross-check source data and assumptions, and require independent review before making investment decisions.

Risk: Financial reports processed through the dependent pdf-parser skill may expose sensitive documents or produce extraction errors.

Mitigation: Install in an isolated environment and verify the pdf-parser publisher and version before using it on financial reports.

Risk: Watchlist use writes local state to ~/.valuation_watchlist.json.

Mitigation: Review local storage expectations before use and avoid storing confidential portfolio notes in shared environments.

Risk: Unpinned dependencies and free market-data sources can affect reproducibility and data reliability.

Mitigation: Pin dependency versions for controlled deployments and cross-check important market data before relying on generated analyses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frankski818/skills/valuation-analysis)
- [Publisher profile](https://clawhub.ai/user/frankski818)
- [Usage guide](references/usage_guide.md)
- [README](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis reports with inline shell commands and optional JSON output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read market and financial data through AKShare; watchlist operations write a local ~/.valuation_watchlist.json file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
