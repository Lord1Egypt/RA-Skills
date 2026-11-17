## Description:

筛选测试用例Excel文件，提取P0/P1优先级用例，删除项目/产品列，重新编号并保持原格式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yontlly](https://clawhub.ai/user/yontlly)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers and test teams use this skill to prepare release or regression test workbooks by extracting P0/P1 cases, dropping project/product columns, and preserving workbook formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workbook transformations remove project/product columns, split merged cells, filter rows, and rewrite case IDs.

Mitigation: Keep the original workbook backed up, use a distinct output filename, and review the generated workbook before relying on it.

Risk: The batch helper processes every .xlsx file in its configured temporary folder.

Mitigation: Use single-file processing by default, or run the batch helper only after confirming the folder contains only intended inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yontlly/skills/testcase-filter)
- [Publisher profile](https://clawhub.ai/user/yontlly)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Code, Guidance]

**Output Format:** [Excel .xlsx workbook plus text processing summary and optional command or Python invocation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a modified workbook with P0/P1 rows, removed project/product columns, split merged cells, preserved formatting, and per-sheet TC001-style renumbering.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
