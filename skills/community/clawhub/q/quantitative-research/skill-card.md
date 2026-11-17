## Description:

Provides quantitative trading research guidance for backtesting, alpha generation, factor models, and statistical arbitrage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengxinjipai](https://clawhub.ai/user/zhengxinjipai)

### License/Terms of Use:


## Use Case:

External users and developers use this skill for quantitative finance research support, including strategy backtesting, alpha-signal validation, factor modeling, statistical arbitrage analysis, and regime-aware portfolio research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quantitative finance outputs may be mistaken for trading advice or relied on without independent review.

Mitigation: Treat strategy logic, thresholds, market data assumptions, and conclusions as research assistance only; require user-controlled review before any trading decision.

Risk: Backtests and alpha signals can be misleading because of overfitting, look-ahead bias, transaction costs, survivorship bias, or weak statistical significance.

Mitigation: Use the artifact's validation guidance for train/test splits, out-of-sample testing, transaction-cost modeling, sample-size checks, and significance testing.

## Reference(s):

- [Quantitative Research Skill Page](https://clawhub.ai/zhengxinjipai/skills/quantitative-research)
- [Publisher Profile](https://clawhub.ai/user/zhengxinjipai)
- [Quantitative Research Patterns](references/patterns.md)
- [Quantitative Research Sharp Edges](references/sharp_edges.md)
- [Quantitative Research Validations](references/validations.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Code, Shell commands, Markdown]

**Output Format:** [Markdown with optional code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Finance research guidance only; users should independently verify market data, assumptions, and any proposed strategy before trading.]

## Skill Version(s):

1.0.0 (source: release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
