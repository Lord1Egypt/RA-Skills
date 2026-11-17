## Description:

Read, write, and analyze tabular data with schema memory, format preservation, and multi-platform support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to inspect, update, analyze, and report on spreadsheet data across Google Sheets, Excel, and CSV files while preserving schema and formatting expectations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Google service account or spreadsheet authorization could grant broader sheet access than intended.

Mitigation: Limit service account sharing to the specific spreadsheets required for the task and review access before installation or use.

Risk: Write or append operations could change unintended ranges or overwrite important formulas or values.

Mitigation: Confirm target sheets and cell ranges before writes, and preserve formulas unless the user explicitly requests changes.

Risk: Local schema memory under ~/spreadsheet/ could accidentally include sensitive credentials or financial data.

Mitigation: Store only non-secret schemas and preferences in memory files, and keep passwords, API keys, and sensitive financial data out of ~/spreadsheet/.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/spreadsheet)
- [Spreadsheet skill definition](artifact/SKILL.md)
- [CSV handling](artifact/csv.md)
- [Excel operations](artifact/excel.md)
- [Google Sheets](artifact/google-sheets.md)
- [Memory setup](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update user-requested spreadsheet files and local schema memory under ~/spreadsheet/.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
