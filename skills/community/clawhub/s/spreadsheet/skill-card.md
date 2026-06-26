## Description: <br>
Read, write, and analyze tabular data with schema memory, format preservation, and multi-platform support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to read, update, analyze, and report on spreadsheet data across Google Sheets, Excel, and CSV files while preserving schemas, formulas, formats, and user preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Sheets credentials could grant broader spreadsheet access than intended. <br>
Mitigation: Use a dedicated Google service account, share only the specific spreadsheets needed, and rotate credentials when access requirements change. <br>
Risk: Local spreadsheet memory may retain sheet IDs, file paths, schemas, and preferences. <br>
Mitigation: Periodically review and prune ~/spreadsheet/ and avoid storing passwords, API keys, or sensitive financial data there. <br>
Risk: Spreadsheet updates can overwrite formulas, formatting, or user data if applied without review. <br>
Mitigation: Limit writes to user-requested ranges, preserve existing formats and formulas, and review changes before applying them to important workbooks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/spreadsheet) <br>
- [Google Sheets guidance](artifact/google-sheets.md) <br>
- [Excel operations guidance](artifact/excel.md) <br>
- [CSV handling guidance](artifact/csv.md) <br>
- [Spreadsheet memory template](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update user-approved spreadsheet files and local memory under ~/spreadsheet/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
