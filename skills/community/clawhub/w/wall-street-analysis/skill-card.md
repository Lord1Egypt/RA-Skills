## Description:

提供基于实时数据的华尔街风格十维度深度股票分析，覆盖公司概览、财务健康、估值、风险及投资建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[horizoncove](https://clawhub.ai/user/horizoncove)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and finance-focused users use this skill to request live stock data checks and structured ten-dimension Wall Street-style equity analysis for a supplied ticker. The output is suited for research support and should not be treated as personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External finance data may be unavailable, stale, or provider-dependent.

Mitigation: Check network connectivity and data-provider availability, and clearly state when live data cannot be fetched.

Risk: Investment-style conclusions may be mistaken for personalized financial advice.

Mitigation: Frame outputs as research support, avoid certainty claims, and encourage independent verification before acting.

Risk: Ambiguous stock codes can lead to analysis of the wrong security.

Mitigation: Ask the user to clarify the ticker, market, or exchange before fetching data when the code is ambiguous.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/horizoncove/skills/wall-street-analysis)
- [Tencent Finance market data endpoint](https://qt.gtimg.cn/q={code})

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown stock analysis report with structured sections and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live market figures when external finance data is available; important numbers should be verified independently.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
