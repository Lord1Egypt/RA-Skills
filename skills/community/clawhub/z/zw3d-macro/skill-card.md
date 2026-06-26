## Description: <br>
Create, edit, validate, and execute ZW3D CAD macro files for CAD automation, model edits, feature creation, UDF workflows, and macro debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shemin1024](https://clawhub.ai/user/shemin1024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CAD automation engineers use this skill to generate ZW3D .mac files, translate modeling tasks into macro syntax, debug macro behavior, and prepare macros for execution in ZW3D. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated macros can automatically create or modify local ZW3D CAD models when executed. <br>
Mitigation: Review the generated .mac file before running it, confirm the exact model path and operation, and work from a copy or backup of important CAD files. <br>
Risk: Vague requests such as modifying a previous model can lead to changes being applied to the wrong file. <br>
Mitigation: Require an explicit target file and intended parameter changes before executing or handing off the macro. <br>


## Reference(s): <br>
- [ZW3D Macro Syntax Reference](references/syntax_reference.md) <br>
- [ZW3D Macro Template](assets/macro_template.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/shemin1024/zw3d-macro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with ZW3D macro code blocks and optional PowerShell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated macros should be reviewed before execution in ZW3D.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
