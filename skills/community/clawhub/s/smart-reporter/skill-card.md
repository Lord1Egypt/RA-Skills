## Description: <br>
智能报告生成器自动分析数据并生成专业报告，支持日报、周报、月报和分析报告，并可输出到飞书文档或本地文件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LiJie298](https://clawhub.ai/user/LiJie298) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users, analysts, and operations teams use this skill to turn Feishu tables, files, JSON data, or database query results into daily, weekly, monthly, or analytic reports for review and sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process business data and create persistent reports in local files or Feishu documents. <br>
Mitigation: Review the data source, generated report, destination, recipients, and sharing scope before writing or sending any report. <br>
Risk: Automatic sending to Feishu can expose sensitive report contents if destination controls are not checked per use. <br>
Mitigation: Keep automatic sending disabled by default and use least-privilege Feishu and database access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LiJie298/smart-reporter) <br>
- [Daily report template](templates/daily.md) <br>
- [Weekly report template](templates/weekly.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration guidance] <br>
**Output Format:** [Generated reports as Markdown, HTML, PDF, or Feishu documents, with template-driven report sections.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report contents depend on the selected data source, report type, time range, and output destination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
