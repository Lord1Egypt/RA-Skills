## Description: <br>
A Yahoo Finance (yfinance) powered financial analysis tool that gets real-time quotes, generates high-resolution charts with moving averages and indicators, summarizes fundamentals, and runs one-shot reports with text summaries and Pro charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bingze00000](https://clawhub.ai/user/bingze00000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to fetch ticker data from Yahoo Finance, inspect fundamentals, view terminal trend output, and generate PNG charts with locally computed technical indicators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python code and may fetch Python packages through uv. <br>
Mitigation: Review the artifact and run it in an environment where local code execution and package installation are acceptable. <br>
Risk: The skill contacts Yahoo Finance/yfinance for ticker data, so availability and data quality can vary by ticker or market. <br>
Mitigation: Treat generated quotes, fundamentals, indicators, and charts as informational and verify important financial decisions against authoritative sources. <br>
Risk: Generated chart files are left in /tmp. <br>
Mitigation: Clear temporary chart files when they are no longer needed, especially on shared systems. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Analysis] <br>
**Output Format:** [Terminal text and tables, ASCII charts, and PNG chart files with CHART_PATH output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated charts are written to /tmp; outputs depend on Yahoo Finance/yfinance data availability and quality.] <br>

## Skill Version(s): <br>
1.2.11 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
