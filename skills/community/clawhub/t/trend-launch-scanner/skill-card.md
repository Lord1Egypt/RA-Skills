## Description:

基于历史技术指栌验证，实时扫描筛选处于上升趋势初期的潜力股票，评分≥60分为重点关注标的。

This skill is for research and development only.

## Publisher:

[jayden-zhong](https://clawhub.ai/user/jayden-zhong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market researchers use this skill to run a trend-following A-share stock scanner, inspect technical scores, confirmation signals, sentiment indicators, and optional backtest outputs. Financial outputs should be treated as research signals only, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Included stock-pool fetch and rebuild utilities can overwrite importable Python files with unvalidated market data.

Mitigation: Review these utilities before running them, avoid fetch/rebuild scripts by default, and execute only in an isolated workspace.

Risk: Some scripts load code from paths outside the skill package and use hard-coded .qclaw paths.

Mitigation: Inspect path configuration before execution and run in an environment where those paths cannot overwrite important user files.

Risk: The scanner produces financial research signals that may be incomplete or misleading.

Mitigation: Treat all outputs as research only and verify decisions with independent financial analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jayden-zhong/skills/trend-launch-scanner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance, Files]

**Output Format:** [Markdown or plain-text guidance with Python command examples and optional CSV/TXT scan outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stock-scanning results depend on live market-data endpoints and local data files.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
