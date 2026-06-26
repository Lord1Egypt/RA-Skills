## Description: <br>
Parse and analyze STDF (Standard Test Data Format) semiconductor test files. Convert STDF to CSV/XLSX, generate analysis reports, correlation reports, PDF charts, and extract specific test data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[showjim](https://clawhub.ai/user/showjim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and semiconductor test engineers use this skill to run local STDF Reader CLI workflows for converting STDF data, generating XLSX reports, creating PDF charts, and extracting targeted test records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on an external PyPI package that is not pinned in the skill instructions. <br>
Mitigation: Pin or review the stdf-reader package version before use in controlled or production environments. <br>
Risk: STDF and CSV files may contain sensitive semiconductor manufacturing or test data. <br>
Mitigation: Process data only in a trusted local workspace and follow the organization's data handling requirements. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local CLI commands that produce CSV, XLSX, PDF, and text outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
