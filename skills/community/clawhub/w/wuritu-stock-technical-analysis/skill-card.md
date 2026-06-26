## Description: <br>
对A股、美股和港股进行技术分析，包括K线形态识别、技术指标计算、趋势判断和量价分析，并生成结构化分析报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuritu](https://clawhub.ai/user/wuritu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and developers use this skill to ask an agent for technical analysis of A-share, US, and Hong Kong stocks. The skill fetches market data, calculates common indicators, recognizes candlestick patterns, analyzes trends and volume, and returns a report for reference rather than investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a stock-data API key and runs local Python scripts that can write output files. <br>
Mitigation: Use a revocable, low-privilege API key, review the external stock-data adapter dependency before use, and keep generated files in temporary or project-specific paths. <br>
Risk: Technical analysis reports can be mistaken for investment advice. <br>
Mitigation: Treat outputs as reference material only, retain the required risk warning, and review results against independent financial information before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuritu/wuritu-stock-technical-analysis) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Files] <br>
**Output Format:** [Structured Markdown report with tables, narrative interpretation, command-driven analysis steps, and optional chart image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and STOCK_DATA_API_KEY; generated reports must include a warning that technical analysis is for reference only and is not investment advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and openclaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
