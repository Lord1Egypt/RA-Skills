## Description: <br>
Fill and edit Word .docx templates on Windows using Microsoft Word automation while preserving formatting, images, underlines, and layout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[winezzz999](https://clawhub.ai/user/winezzz999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document automation users on Windows use this skill to fill cover fields, append answers, insert page breaks, update section fields, and replace text in .docx templates while preserving Word layout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Debug instructions include a taskkill command that can forcibly close all open Microsoft Word documents. <br>
Mitigation: Save and close Word documents before debugging; avoid taskkill unless necessary and prefer closing only the Word instance created for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/winezzz999/skills/win32-word-filler) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance, Files] <br>
**Output Format:** [Markdown guidance with bash and Python examples; generated .docx files from the bundled CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Windows, Microsoft Word, and pywin32; users provide input and output .docx paths plus CLI options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
