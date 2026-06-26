## Description: <br>
Analyzes stock CSV data with moving averages, MACD, RSI, and Bollinger Bands to generate trend assessments, trading-signal summaries, and optional visual charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wang-junjian](https://clawhub.ai/user/wang-junjian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run local technical analysis on selected stock CSV files, either one security at a time or in batch, and produce reports that summarize trend direction, indicator signals, and risk notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill outputs trading suggestions and trend signals that could be mistaken for financial advice. <br>
Mitigation: Treat outputs as informational technical analysis only and require human review before making investment decisions. <br>
Risk: Batch mode scans a user-provided directory and writes generated reports and indicator files. <br>
Mitigation: Run in a virtual environment, point batch mode only at intended folders, and review generated files before sharing or relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wang-junjian/super-trend-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, terminal summaries, optional PNG charts, and generated CSV indicator files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally on user-selected CSV files and writes generated reports and optional chart artifacts to an output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
