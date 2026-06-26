## Description: <br>
Assist macOS users in preparing, converting, reviewing, exporting, and troubleshooting Word, PDF, Markdown, PowerPoint, and Excel files for reliable WPS Office workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lethehades](https://clawhub.ai/user/lethehades) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare and troubleshoot document workflows on macOS when WPS Office is part of the editing, compatibility review, or export path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional helper script processes local document files and may write an output file chosen by the user. <br>
Mitigation: Run it only on files intended for processing and choose a new output filename to avoid overwriting important work. <br>
Risk: Document conversion results can vary when the external conversion toolchain is installed or updated independently. <br>
Mitigation: Pin or pre-install the conversion toolchain when reproducibility or supply-chain control is required. <br>
Risk: WPS and Word layout compatibility issues can persist after conversion, especially around fonts, page size, tables, headers, footers, and page breaks. <br>
Mitigation: Visually review representative pages in WPS before final export and keep original files untouched by default. <br>


## Reference(s): <br>
- [WPS macOS Helper on ClawHub](https://clawhub.ai/lethehades/wps-macos-helper) <br>
- [workflow](references/workflow.md) <br>
- [case-studies](references/case-studies.md) <br>
- [compatibility](references/compatibility.md) <br>
- [export-and-format](references/export-and-format.md) <br>
- [troubleshooting](references/troubleshooting.md) <br>
- [release-checklist](references/release-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional shell command output and generated workflow notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a new Markdown workflow note or conversion output when the optional helper script is run with an output path.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
