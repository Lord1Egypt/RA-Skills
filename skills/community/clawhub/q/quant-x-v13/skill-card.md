## Description:

A-share quantitative analysis skill that combines four-dimensional OBI, enhanced OBV, Longhubang validation, main-force accumulation checks, and multi-factor scoring.

This skill is for research and development only.

## Publisher:

[43906351-debug](https://clawhub.ai/user/43906351-debug)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a China A-share market analysis workflow for sh600330, producing OBI, OBV, Longhubang, main-force, sector, and factor-score research outputs. The output should be reviewed as market research and not treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Tencent and Eastmoney market-data endpoints during execution.

Mitigation: Run it only where outbound market-data requests are allowed and review provider access requirements before use.

Risk: The skill writes results to /workspace/v13/analysis_result.json.

Mitigation: Ensure the output path is expected and review the generated file before sharing or retaining it.

Risk: The stock analysis output is research-oriented and may include inconsistent model labeling.

Mitigation: Treat results as research support, verify calculations and labels, and do not use the output as investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/43906351-debug/skills/quant-x-v13)
- [Tencent quote endpoint](https://qt.gtimg.cn/q={self.code})
- [Tencent minute endpoint](https://web.ifzq.gtimg.cn/appstock/app/minute/query?code={self.code})
- [Eastmoney push2 endpoint](https://push2.eastmoney.com/api/qt/stock/get)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Files]

**Output Format:** [Console markdown-style analysis plus a JSON results file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes analysis results to /workspace/v13/analysis_result.json when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 13.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
