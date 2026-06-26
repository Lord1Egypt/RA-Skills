## Description: <br>
A股/港股实时行情查询、基本面分析、深度报告生成与邮件发送一体化工具。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hitjcl](https://clawhub.ai/user/hitjcl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query A-share and Hong Kong stock prices, collect valuation and fundamentals data, generate Markdown stock analysis reports, and optionally send those reports by email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial-data output can be incomplete, delayed, or unsuitable as personal investment advice. <br>
Mitigation: Review generated reports, verify market and fundamentals data with trusted sources, and treat the output as analysis support rather than a trading instruction. <br>
Risk: The skill can use JQData and SMTP credentials for fundamentals data and email delivery. <br>
Mitigation: Provide credentials through environment variables where possible, use app-specific email passwords, run in a virtual environment, and avoid placing passwords or authorization codes in code, documents, or reports. <br>
Risk: Interactive JQData setup may store the account phone identifier locally. <br>
Mitigation: Use environment variables for credentials when practical, limit local config-file access, and clear the local configuration when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hitjcl/stock-analyzer-v2) <br>
- [JoinQuant](https://www.joinquant.com) <br>
- [Report template](references/report_template.md) <br>
- [Stock code reference](references/stock_codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, terminal text, Python command examples, and email message content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces financial-data summaries from AkShare and optional JQData inputs; users should review generated reports before sending or relying on them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
