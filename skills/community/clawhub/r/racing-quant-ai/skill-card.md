## Description:

Racing Quant AI helps agents match A-share quantitative strategies to holdings and produce structured stock-analysis reports for investment reference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenxyzcyxpp](https://clawhub.ai/user/chenxyzcyxpp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query quantitative strategy holdings, analyze A-share stocks with market, fundamental, fund-flow, and news signals, and generate investment-reference reports. The skill also includes workflows for portfolio review, strategy drawdown analysis, position sizing, and optional trading-instruction generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live database credentials are exposed in the skill artifact.

Mitigation: Remove credentials from the skill, rotate the exposed password, and require environment-managed secrets with least-privilege read access.

Risk: Stock analysis workflows are mixed with live trading and order-execution instructions.

Mitigation: Separate analysis from trading workflows and keep trading dry-run by default with explicit account selection, order preview, and user confirmation before any execution.

Risk: Production-server administration and scheduler-state guidance broadens the operational impact of installing the skill.

Mitigation: Restrict operational guidance to authorized maintainers, remove scheduler prompt-recovery guidance, and avoid bundling production administration steps with general stock-analysis workflows.

Risk: Financial analysis can mislead users if market, fundamental, or fund-flow data is stale, unavailable, or fabricated.

Mitigation: Require current data-source calls, label the source used, state when data retrieval fails, and keep the investment-risk disclaimer in every report.

Risk: Unpinned dependencies can make execution non-reproducible or introduce unexpected package changes.

Mitigation: Pin Node.js and Python dependencies and review dependency updates before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenxyzcyxpp/skills/racing-quant-ai)
- [Signal-asset matching framework](artifact/references/signal-asset-matching-framework.md)
- [Portfolio deep analysis workflow](artifact/references/portfolio-analysis-workflow.md)
- [Trading execution pipeline](artifact/references/trading-execution-pipeline.md)
- [Position sizing optimization](artifact/references/position-sizing-optimization.md)
- [Strategy drawdown analysis](artifact/references/strategy-drawdown-analysis.md)
- [Eastmoney Push API](https://push2.eastmoney.com/api/qt/stock/get?secid=0.300308&fields=f43,f44,f45,f46,f47,f48,f50,f51,f52,f55,f57,f58,f60,f116,f117,f162,f167,f170,f171)
- [Eastmoney historical K-line API](https://push2his.eastmoney.com/api/qt/stock/kline/get)
- [Racing AI strategy page pattern](http://racingai.top/strategy/{id})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON trading instructions, shell commands, and code or configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include strategy lists, holdings tables, stock-analysis narratives, data-source notes, disclaimers, and dry-run or order-execution instructions depending on the request.]

## Skill Version(s):

1.10.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
