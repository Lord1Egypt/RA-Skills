## Description: <br>
核心ROIC（投入资本回报率）深度分析助手，用于A股、港股、美股上市公司的ROIC计算与资本效率分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and finance-focused agents use this skill to calculate core ROIC, NOPAT, and invested capital from listed-company financial data, then produce a Markdown-style analysis that highlights items requiring manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package mixes ROIC financial-analysis material with unrelated QQ bot documentation. <br>
Mitigation: Review the artifact contents before installation and confirm the installed skill matches the intended ROIC use case. <br>
Risk: The skill can run scripts, fetch external financial data, and write local reports. <br>
Mitigation: Require explicit user approval before tool execution and review generated files and network-dependent results. <br>
Risk: ROIC outputs may be incomplete or misleading if financial data, hidden financial assets, acquisition intangibles, or long-term equity investment splits are not independently checked. <br>
Mitigation: Validate outputs against annual reports and other authoritative filings before using results for investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cgxxxxxxxxxxxx/roic-toolkit) <br>
- [finance-data API](https://www.codebuddy.cn/v2/tool/financedata) <br>
- [SEC EDGAR company search](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company={ticker}&type=10-K&dateb=&owner=include&count=1&output=atom) <br>
- [Eastmoney notices](https://data.eastmoney.com/notices/detail/{股票代码}/AN{公告日期}{序号}.html) <br>
- [Xueqiu annual report PDF pattern](https://stockmc.xueqiu.com/{YYYYMM}/{代码}_{YYYYMMDD}_CQ65.pdf) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Code, Files, Guidance] <br>
**Output Format:** [Markdown reports with tables, calculations, warning markers, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses external financial-data sources and flags selected balance-sheet items for manual verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
