## Description:

通用模版。用户上传多个独立文档（问句、指标维度说明书、业务知识说明书、数据字典、表结构数据），自动提取指标、维度和过滤条件并输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hht1ng](https://clawhub.ai/user/hht1ng)

### License/Terms of Use:

MIT-0

## Use Case:

Business intelligence analysts, data product teams, and requirements owners use this skill to process Chinese BI question workbooks and map each question to metrics, dimensions, and filters using optional reference documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill updates uploaded Excel workbooks by filling columns and adding a matrix sheet, so accidental changes to an important original workbook are possible.

Mitigation: Run it on a copy of important workbooks and compare the generated fields and matrix before replacing source files.

Risk: Metric, dimension, or filter extraction can be incomplete or incorrect when optional reference documents are missing or ambiguous.

Mitigation: Review rows marked as unrecognized or needing confirmation and validate results against the project's authoritative metric, dimension, dictionary, and table-structure references.

Risk: Uploaded BI question workbooks and reference documents may contain sensitive business definitions or schema details.

Mitigation: Use approved data-handling workflows and avoid uploading documents outside the intended trusted environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hht1ng/skills/questionnaire)
- [Publisher profile](https://clawhub.ai/user/hht1ng)
- [SKILL.md](artifact/SKILL.md)
- [skill-指标维度说明书.md](artifact/skill-指标维度说明书.md)
- [skill-业务知识说明书.md](artifact/skill-业务知识说明书.md)
- [skill-数据字典.md](artifact/skill-数据字典.md)
- [skill-表结构数据.md](artifact/skill-表结构数据.md)

## Skill Output:

**Output Type(s):** [Analysis, Files, Markdown, Guidance]

**Output Format:** [Updated spreadsheet/workbook content with filled metric, dimension, and filter fields plus a two-dimensional metric-dimension matrix sheet.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves the original workbook style when updating the question document.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
