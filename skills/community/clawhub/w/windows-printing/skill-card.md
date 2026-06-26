## Description: <br>
Windows Printing helps an agent list available Windows printers and print local files with user-selected printer, color mode, copy count, duplex mode, flip edge, and paper size. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuetsui](https://clawhub.ai/user/fuetsui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users use this skill to prepare and submit local Windows print jobs after confirming the target file, printer, color mode, copy count, duplex setting, and paper size. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports that the skill references missing PowerShell helper scripts before real print actions. <br>
Mitigation: Review the package before installing and use it only after the publisher provides the referenced scripts or a corrected package. <br>
Risk: Printing can affect shared printer configuration and submit unintended jobs if parameters are wrong. <br>
Mitigation: Confirm the file, printer, copies, color mode, duplex mode, and paper size before submission, and check printer settings afterward on shared or important printers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fuetsui/windows-printing) <br>
- [Printing Options Reference](references/options.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with PowerShell command examples and confirmation or receipt text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should confirm the selected file, printer, color mode, copies, duplex mode, paper size, queue status, and result when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
