## Description: <br>
Automatically groups questionnaire scale columns by prefix and item number, calculates dimension averages, and supports reverse scoring and missing-value handling for Excel and CSV files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[y-egg](https://clawhub.ai/user/y-egg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to score questionnaire or scale datasets by generating per-dimension average columns from CSV or Excel inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-selected CSV or Excel files and writes a scored copy, so an unintended output path could overwrite or misplace important spreadsheet data. <br>
Mitigation: Use the default _scored output or a clearly safe output path, and keep backups of important spreadsheets before running it. <br>
Risk: The local Python script depends on pandas to process spreadsheet data. <br>
Mitigation: Run it only in a trusted Python environment with dependencies installed from trusted sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/y-egg/scale-scorer) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Text] <br>
**Output Format:** [CSV or Excel file with added dimension-score columns, plus console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a scored copy by default using the input filename with a _scored suffix; a custom output path can be supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
