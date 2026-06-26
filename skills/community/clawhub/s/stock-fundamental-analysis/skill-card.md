## Description: <br>
Analyzes listed companies' fundamentals, including financial health, valuation, growth, industry comparison, financial report interpretation, and structured investment research reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuritu](https://clawhub.ai/user/wuritu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate structured stock fundamental analysis reports for listed companies, including valuation, financial health, growth, industry comparison, and shareholder signals. Outputs are research support and must be reviewed before any investment decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python code and requires a stock-data API key. <br>
Mitigation: Install only in environments where local code execution and API-key use are acceptable; review dependencies and data-source configuration before running. <br>
Risk: The skill can overstate the completeness of its analysis workflow. <br>
Mitigation: Treat results as partial research support, verify source data and missing tool coverage, and do not rely on outputs as investment advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuritu/stock-fundamental-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Structured Markdown report with tables, data sources, timestamps, confidence labels, and an investment disclaimer; helper scripts may emit JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and STOCK_DATA_API_KEY; outputs should be treated as research support, not investment advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and openclaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
