## Description:

基于A股行情数据计算SAR抛物线指标，并用机构资金流向近似替代ZJTJ庄家抬轿指标，实现四维选股策略。

This skill is ready for commercial/non-commercial use.

## Publisher:

[haohanyang92](https://clawhub.ai/user/haohanyang92)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and market-analysis practitioners can use this skill to generate Python helpers for SAR calculation, approximate ZJTJ-style fund-flow signals, and batch stock-screening analysis. Outputs should be treated as educational analysis and independently verified before any financial decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated buy signals or stock-screening recommendations may be mistaken for trading instructions.

Mitigation: Treat the output as rough educational analysis and verify results independently before making financial decisions.

Risk: The strategy uses a simplified ZJTJ approximation and the scoring description is partly inconsistent.

Mitigation: Review the underlying SAR, fund-flow, volume, and scoring logic before relying on any recommendation.

Risk: Runtime behavior depends on external Python packages and market-data availability.

Mitigation: Install in an isolated Python environment, prefer pinned dependencies, and handle unavailable or unstable AkShare data.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/haohanyang92/skills/zjtj-sar-calculator)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stock-analysis signals and screening recommendations that require independent financial review.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
