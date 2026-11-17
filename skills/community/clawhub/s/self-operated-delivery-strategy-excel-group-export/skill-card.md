## Description:

读取 Excel 文件，按照指定列分组，并将每个分组导出为用分组字段组合命名的新 Excel 文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoming](https://clawhub.ai/user/guoming)

### License/Terms of Use:

MIT-0

## Use Case:

Operations and logistics users can split self-operated delivery strategy spreadsheets into grouped zone-configuration workbooks. The skill is intended for Excel inputs with the configured grouping columns and a postal-code column.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workbooks may retain unexpected source spreadsheet columns despite documentation saying only the new zone fields are kept.

Mitigation: Run the skill only on reviewed copies of business spreadsheets and inspect generated workbooks before sharing or importing them.

Risk: The country code in generated rows is hard-coded as US.

Mitigation: Confirm that US is correct for the workflow before using the exported files operationally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoming/skills/self-operated-delivery-strategy-excel-group-export)
- [Publisher profile](https://clawhub.ai/user/guoming)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Excel workbooks with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates one .xlsx file per group and prints export progress to the terminal.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
