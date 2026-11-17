## Description:

对A股/美股/港股进行全面技术分析，包括K线形态识别、技术指标计算、趋势判断、量价分析，生成可操作的技术分析报告

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuritu](https://clawhub.ai/user/wuritu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run stock technical analysis workflows for A-share, US, and Hong Kong securities, including K-line data retrieval, indicator calculation, candlestick pattern review, trend analysis, volume-price analysis, and chart generation. Reports are for reference only and do not constitute investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Python execution and access to a stock-data API key.

Mitigation: Run it in a constrained workspace and provide only the credentials needed for the requested data source.

Risk: Command instructions and file-writing behavior are under-scoped, including tool outputs written to local paths.

Mitigation: Validate ticker, period, indicator, and output path inputs, avoid direct shell interpolation, and write outputs to a dedicated safe directory.

Risk: Technical analysis output can be mistaken for investment advice.

Mitigation: Keep the required report warning that technical analysis is for reference only and does not constitute investment advice.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wuritu/skills/wuritu-stock-technical-analysis)
- [Publisher profile](https://clawhub.ai/user/wuritu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Structured Markdown report with JSON tool outputs and optional PNG chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and STOCK_DATA_API_KEY; generated reports must include a risk notice that technical analysis is for reference only and not investment advice.]

## Skill Version(s):

1.0.0 (source: server release evidence and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
