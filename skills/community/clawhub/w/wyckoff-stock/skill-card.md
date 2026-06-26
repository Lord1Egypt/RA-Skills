## Description: <br>
A股诊股工具，基于Wyckoff 2.0方法论分析股票。支持获取实时K线数据、技术指标计算、趋势分析、支撑阻力识别、Wyckoff结构判断、风险收益评估。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxarch1980](https://clawhub.ai/user/dxarch1980) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate informational technical-analysis reports for A-share stock codes, including Wyckoff structure, trend, volume, support/resistance, and risk-reward signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on efinance as a third-party market-data dependency that makes network requests. <br>
Mitigation: Install only in environments where that dependency and outbound market-data requests are acceptable. <br>
Risk: The generated diagnosis may be mistaken for investment advice. <br>
Mitigation: Treat the report as informational technical analysis and require human financial judgment before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dxarch1980/wyckoff-stock) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text diagnosis report with structured report object fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an A-share stock code; the optional lookback window defaults to 250 days.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
