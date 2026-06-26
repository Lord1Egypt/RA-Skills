## Description: <br>
Automated financial indicator analysis for S&P 500 and NASDAQ stocks, with weighted financial health scoring, red-flag detection, and sector-level rankings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, developers, and finance teams use this skill to analyze user-provided CSV or JSON stock data, rank S&P 500 and NASDAQ stocks, identify financial red flags, and produce screening reports. It also provides manual Feishu/Lark permission guidance for sharing financial reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial scores and rankings may be misleading if the input data is stale, incomplete, incorrect, or if the scoring assumptions do not fit the user's investment context. <br>
Mitigation: Verify the source data and review the scoring thresholds before relying on the output; treat the analysis as screening support rather than financial advice. <br>
Risk: The skill reads local CSV or JSON files selected by the user for analysis. <br>
Mitigation: Provide only financial data that the agent is intended to read, and avoid including unrelated confidential information in input files. <br>
Risk: Feishu/Lark sharing guidance may not match an organization's current access-control policy. <br>
Mitigation: Confirm permissions with the organization's policy owner before sharing reports, and default to named-user, least-privilege access. <br>


## Reference(s): <br>
- [Financial Indicators Reference](references/indicators.md) <br>
- [SEC EDGAR](https://www.sec.gov/cgi-bin/browse-edgar) <br>
- [Financial Modeling Prep](https://financialmodelingprep.com/) <br>
- [Alpha Vantage](https://www.alphavantage.co/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON analysis output, Python commands, and permission guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local financial-health scores, sector rankings, red-flag summaries, and manual Feishu/Lark sharing recommendations from user-provided stock data.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
