## Description:

光伏电站巡检报告生成技能。支持创建标准化巡检报告、记录缺陷问题、统计汇总数据、导出 Word/PDF 格式。使用场景：(1) 生成每日/周/月巡检报告，(2) 记录电站缺陷和隐患，(3) 统计发电量数据，(4) 导出格式化报告文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shendingyi](https://clawhub.ai/user/shendingyi)

### License/Terms of Use:

MIT-0

## Use Case:

Operations teams and external maintainers use this skill to generate daily, weekly, and monthly photovoltaic power-station inspection reports, record defects, summarize generation and equipment status, and export report documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided station names can influence local output paths and may create or overwrite files outside the intended report folder.

Mitigation: Run the skill in a restricted workspace, use trusted station names, and sanitize path characters before generating reports.

Risk: Generated inspection reports may be sent through external channels such as Feishu or email.

Mitigation: Require explicit confirmation before sending reports outside the local workspace.

Risk: The Word report path depends on python-docx being available in the runtime environment.

Mitigation: Pin python-docx in an isolated environment before using Word export.

## Reference(s):

- [PV Inspection ClawHub Listing](https://clawhub.ai/shendingyi/skills/pv-inspection)
- [Station Configuration Reference](artifact/references/stations.md)
- [Report Templates](artifact/assets/templates/report_templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, Word documents, JSON defect records, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local report and defect files in configured workspace folders.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
