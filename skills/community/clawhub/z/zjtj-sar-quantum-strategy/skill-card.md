## Description:

ZJTJ+SAR+成交量+市场情绪四维选股策略，结合主力动向、趋势判断、资金验证和环境分析，适合A股短线波段操作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[haohanyang92](https://clawhub.ai/user/haohanyang92)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask the skill to explain a four-factor A-share short-term stock screening workflow using ZJTJ, SAR, volume, and market sentiment. The skill provides entry, exit, position-sizing, no-trade, and daily review criteria as trading guidance that requires independent verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Speculative short-term trading guidance may be wrong or misapplied as financial advice.

Mitigation: Require independent signal verification and human financial judgment; do not connect outputs to automated order placement.

Risk: The SAR explanation appears inconsistent with the provided formula.

Mitigation: Review the intended SAR condition against the target trading platform before using the strategy.

Risk: Technical indicators can fail in sideways or abnormal markets.

Mitigation: Apply the stated position sizing, stop-loss, no-trade constraints, and market sentiment checks before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haohanyang92/skills/zjtj-sar-quantum-strategy)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with tables and formula snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Financial-risk caveats and strategy constraints are included; no code execution or external tool use is required.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
