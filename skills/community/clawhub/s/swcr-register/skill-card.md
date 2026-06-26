## Description: <br>
Swcr Register helps generate Chinese software copyright registration materials, including source-code evidence documents, operating manuals, form-filling information, and optional guided online filing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daxiongdi666](https://clawhub.ai/user/daxiongdi666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and software owners use this skill to prepare Chinese software copyright registration materials from a project repository or local source directory. It can generate DOCX source-code and operating-manual documents, produce Markdown form-filling information, and optionally guide a user through online filing after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated registration text may contain generic assumptions or inaccurate source, ownership, function, feature, date, or rights-holder details. <br>
Mitigation: Manually verify all generated source excerpts and registration fields before uploading, submitting, or relying on the materials. <br>
Risk: The skill reads a selected project source directory to create registration documents. <br>
Mitigation: Use it only on source trees the user is comfortable exposing to the agent, and review generated files before sharing them externally. <br>
Risk: Optional browser-assisted filing interacts with an official registration workflow. <br>
Mitigation: Proceed only after explicit user confirmation, require user review of the filled information, and do not automatically submit the application. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/daxiongdi666/swcr-register) <br>
- [WiseFlow Project Homepage](https://github.com/TeamWiseFlow/wiseflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated artifacts include DOCX and Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read the selected project source and create registration documents; optional browser-assisted filing requires explicit user confirmation.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
