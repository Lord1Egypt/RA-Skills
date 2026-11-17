## Description:

从工程报价单和 Excel/CSV 表格中提取、清洗、标准化硬件设备 BOM 数据，并按项目交付时间生成物料需求预测汇总表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[git-surellc](https://clawhub.ai/user/git-surellc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, procurement analysts, and supply-chain teams use this skill to analyze Chinese-language BOM and supplier quote tables, exclude non-material service lines, standardize equivalent hardware items, and produce time-based demand summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplier quotes and project delivery timelines may contain sensitive commercial information.

Mitigation: Only provide files you are comfortable having the agent analyze in the current workspace.

Risk: Incorrect item standardization, quantity extraction, or time mapping could distort the generated demand summary.

Mitigation: Review ambiguous names, missing quantities, unit conversions, and project delivery mappings against the source tables before using the summary for procurement decisions.

## Reference(s):

- [数据提取规则详解](references/extraction-rules.md)
- [物料标准化映射表](references/material-mapping.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown tables and concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on hardware BOM extraction, standardized material mapping, quantity aggregation, and timeline-based demand summaries.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
