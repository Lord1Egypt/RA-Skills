## Description: <br>
光伏电站巡检报告生成技能。支持创建标准化巡检报告、记录缺陷问题、统计汇总数据、导出 Word/PDF 格式。使用场景：(1) 生成每日/周/月巡检报告，(2) 记录电站缺陷和隐患，(3) 统计发电量数据，(4) 导出格式化报告文档。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shendingyi](https://clawhub.ai/user/shendingyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations and maintenance teams use this skill to generate photovoltaic station inspection reports, record equipment defects, and summarize generation and inspection coverage data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may contain sample, placeholder, or simulated inspection data. <br>
Mitigation: Verify and replace generated values with authoritative monitoring and inspection records before sharing or acting on a report. <br>
Risk: Reports and defect records may contain operational details about photovoltaic stations. <br>
Mitigation: Keep generated files local by default, review persisted defect records, and restrict access to report and data directories. <br>
Risk: Sending draft reports through Feishu, email, or another external channel may expose unverified information. <br>
Mitigation: Confirm recipients and review the final report contents before using any external delivery channel. <br>


## Reference(s): <br>
- [Report Templates](assets/templates/report_templates.md) <br>
- [Station Configuration](references/stations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, Word documents, local JSON defect records, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports and defect records are generated as local files; generated inspection data should be verified against authoritative monitoring records.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
