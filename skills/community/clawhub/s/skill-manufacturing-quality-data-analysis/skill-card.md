## Description:

制造业质量现场数据分析；当用户需要分析车间巡检、制程不良、成品检验台账数据或处理现场不合格记录时使用；覆盖数据清洗、统计分析、图表可视化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing quality engineers and operations teams use this skill to parse Excel, CSV, Word, or PDF shop-floor inspection and defect records, clean and map key fields, summarize defect patterns, and generate Markdown tables plus HTML visual reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may include untrusted values from uploaded manufacturing records.

Mitigation: Process only trusted files, keep generated reports isolated, and use a fixed version that escapes HTML before reports are shared.

Risk: Generated reports may make an undisclosed external font request.

Mitigation: Remove or disclose external font loading before using reports with confidential manufacturing data.

Risk: Generated reports and parsed JSON can contain confidential manufacturing records.

Mitigation: Treat outputs as confidential records and avoid broad sharing outside the intended review group.

Risk: Report generation can overwrite the specified output file.

Mitigation: Choose a unique report path or confirm overwrite behavior before running report generation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/duding-engicool/skills/skill-manufacturing-quality-data-analysis)
- [Publisher Profile](https://clawhub.ai/user/duding-engicool)
- [Server-Resolved Source Repository](https://github.com/duding-engicool/skill-manufacturing-quality-data-analysis)
- [Field Mapping Reference](references/field_mapping.md)
- [Cleaning Rules Reference](references/cleaning_rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, HTML, JSON, shell commands, guidance]

**Output Format:** [Markdown tables, JSON script results, and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill asks for user confirmation when field meaning, data sufficiency, or report outline is ambiguous.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
