## Description: <br>
Helps agents retrieve China-focused financial market data through Tushare Pro, including equities, Hong Kong and US stocks, funds, futures, bonds, financial statements, and macroeconomic indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bingze00000](https://clawhub.ai/user/bingze00000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users can use this skill to select Tushare interfaces, configure a Tushare token, and generate Python calls for market, fundamentals, and macroeconomic data retrieval. It is suited for data lookup, financial analysis workflows, and batch export tasks that rely on Tushare Pro access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tushare access requires a user token, which may be exposed if placed in committed configuration files or shared command history. <br>
Mitigation: Prefer the TUSHARE_TOKEN environment variable, do not commit tokens, and restrict permissions on any local secret files. <br>
Risk: Some broad reference endpoints may expose policy documents, media transcripts, management biographies, or other privacy-sensitive fields. <br>
Mitigation: Review the selected endpoint documentation before use and treat personal data fields as privacy-sensitive. <br>
Risk: Financial market and macroeconomic data can be incomplete, delayed, permission-limited, or unsuitable as sole investment advice. <br>
Mitigation: Validate returned data against the Tushare documentation and use independent review before relying on outputs for financial decisions. <br>


## Reference(s): <br>
- [Tushare Official Documentation](https://tushare.pro/document/2) <br>
- [Tushare API Test Tool](https://tushare.pro/document/1) <br>
- [Tushare API Interface Index](reference/README.md) <br>
- [Tushare API Quick Reference](QUICK_REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include pandas DataFrame-oriented examples, Tushare API method selections, token setup guidance, and file export suggestions.] <br>

## Skill Version(s): <br>
2.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
