## Description:

Processes uploaded Excel table-structure workbooks by replacing headers, adding default field data, applying table styling, and saving a processed copy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cztzb](https://clawhub.ai/user/cztzb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users can use this skill to standardize Excel table-structure files for housing provident fund data work. It is intended for uploaded .xlsx files that need consistent headers, default field rows, styling, and processed workbook output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may silently alter spreadsheet data that users expect to remain preserved.

Mitigation: Use disposable workbook copies, inspect the processed workbook before relying on it, and confirm that preserved columns still match expectations.

Risk: Path-like filenames or output names may access or write files outside the documented folders.

Mitigation: Avoid path-like filenames, run the skill in a constrained workspace, and review file paths before execution.

## Reference(s):

- [Housing Provident Fund Basic Data Standard reference](references/住房公积金基础数据标准（报批稿）1001.md)
- [ClawHub skill page](https://clawhub.ai/cztzb/skills/table-structure-handler)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [Processed XLSX workbook plus brief status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [By default, writes a _processed.xlsx copy to /workspace/skills_output.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
