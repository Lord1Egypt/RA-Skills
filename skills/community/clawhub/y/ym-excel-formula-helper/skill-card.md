## Description:

Turns Chinese spreadsheet requests into ready-to-use Excel or WPS formulas with plain-language explanations, edge-case notes, and common error diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

Spreadsheet users and agents use this skill to convert Chinese natural-language requirements into Excel/WPS formulas, explanations, compatibility notes, and troubleshooting guidance. It is intended for formula text generation, not direct editing of spreadsheet files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may trigger on broad spreadsheet or function wording, including non-spreadsheet programming-function requests.

Mitigation: Confirm the user is asking for Excel or WPS formula help; route programming or unrelated function questions to a more appropriate skill.

Risk: Generated formulas may not work without adjustment when the user's real workbook structure, version, or data cleanliness differs from the described inputs.

Mitigation: Review formulas before use, update placeholder ranges to match the workbook, and verify compatibility notes and dirty-data assumptions against the actual sheet.

## Reference(s):

- [formula-dict.md](references/formula-dict.md)
- [Server-resolved GitHub source](https://github.com/liuyuming0823/ym-excel-formula-helper)
- [ClawHub skill page](https://clawhub.ai/liuyuming0823/skills/ym-excel-formula-helper)
- [ClawHub publisher profile](https://clawhub.ai/user/liuyuming0823)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with Excel formulas, explanations, edge-case notes, and common error diagnostics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plain-text formula guidance only; does not execute code, access the network, persist data, modify files, or operate Excel/WPS files directly.]

## Skill Version(s):

0.1.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
