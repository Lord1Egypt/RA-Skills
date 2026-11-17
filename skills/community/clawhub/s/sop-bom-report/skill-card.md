## Description:

SOP and BOM comparison skill that extracts material information from one SOP spreadsheet and one or more BOM spreadsheets, compares differences by material code, and generates an independent review report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2656255594](https://clawhub.ai/user/2656255594)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing, quality, and engineering users can use this skill to compare SOP and BOM spreadsheets, identify differing materials, SOP-only materials, BOM-only materials, and repeated SOP material codes. It is intended for local report generation from supplied spreadsheet files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads supplied spreadsheets and extracts workbook archives locally, which can expose sensitive SOP or BOM contents or stress local resources with untrusted files.

Mitigation: Use trusted spreadsheet inputs where possible, run the skill in a sandbox or dedicated working directory, and review archive-size handling before broad deployment.

Risk: The skill automatically deletes matching temporary directories and old report files as part of cleanup.

Mitigation: Use a dedicated output directory, avoid sensitive shared temporary environments, and adjust or review cleanup behavior before use in shared systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2656255594/skills/sop-bom-report)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Guidance]

**Output Format:** [XLSX report file with console status text and command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a spreadsheet report containing differing materials, SOP-only materials, and BOM-only materials.]

## Skill Version(s):

1.4.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
