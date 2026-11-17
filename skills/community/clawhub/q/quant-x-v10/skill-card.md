## Description:

QUANT-X v10 量化策略仪表盘 helps agents generate and operate an A-share stock dashboard for 600330 with live Tencent quote data, multi-factor scoring, OBI analysis, strategy signals, sector comparison, and large-order panels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43906351-debug](https://clawhub.ai/user/43906351-debug)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and finance-focused agents use this skill to create or deploy a live A-share stock dashboard with heuristic trading scores, order-book imbalance views, and strategy summaries. Outputs should support market analysis workflows and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard presents trading scores and large-order panels that may overstate the precision of the underlying analytics.

Mitigation: Treat the scores, OBI values, and large-order panels as heuristics and review them against independent market data before making decisions.

Risk: Deployment instructions include an unpinned npx mdeploy path.

Mitigation: Pin and verify deployment tooling before use, or deploy the HTML through a reviewed internal hosting path.

Risk: The dashboard loads Chart.js from a public CDN.

Mitigation: Self-host Chart.js or apply integrity controls before using the dashboard in decision-support environments.

## Reference(s):

- [QUANT-X v10 ClawHub Skill Page](https://clawhub.ai/43906351-debug/skills/quant-x-v10)
- [Tencent quote data endpoint](https://qt.gtimg.cn/q=sh600330)
- [Tencent ifzq K-line endpoint](https://web.ifzq.gtimg.cn/appstock/app/fqkline/get)
- [Tencent ifzq minute endpoint](https://web.ifzq.gtimg.cn/appstock/app/minute/query)
- [多因子评分公式详细说明](references/scoring-formula.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration notes, and deployable HTML code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference live market-data endpoints and browser-side dashboard behavior.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
