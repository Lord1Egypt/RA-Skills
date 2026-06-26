## Description: <br>
Pandas-powered CSV & Excel management for quick previews, summaries, filtering, transforming, and format conversions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CrimsonDevil333333](https://clawhub.ai/user/CrimsonDevil333333) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use Sheetsmith to inspect CSV, TSV, and Excel files, summarize columns, filter rows, transform fields, and export cleaned spreadsheet data without writing pandas boilerplate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spreadsheet transformations can overwrite or alter source data when in-place writes are explicitly requested. <br>
Mitigation: Prefer writing to a separate output file, keep raw backups, and preview unfamiliar schemas before saving changes. <br>
Risk: Spreadsheet formulas or shared outputs may expose sensitive or unintended data. <br>
Mitigation: Review formulas and clear sensitive spreadsheet content before sharing outputs through consumer chat apps or other external channels. <br>


## Reference(s): <br>
- [Sheetsmith usage reference](references/usage.md) <br>
- [ClawHub skill page](https://clawhub.ai/CrimsonDevil333333/sheetsmith) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, files, guidance] <br>
**Output Format:** [Markdown and plain text with optional generated CSV, TSV, or XLSX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local spreadsheet files and write transformed outputs when the user supplies an output path or explicitly requests in-place modification.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
