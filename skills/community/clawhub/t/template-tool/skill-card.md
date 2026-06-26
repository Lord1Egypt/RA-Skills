## Description: <br>
Process text templates with variable substitution. Use for generating dynamic content from template files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate text, markdown, code, shell-oriented templates, and configuration-like content by substituting variables into template files or initialized templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled scripts can create or overwrite files beyond the narrow text-substitution behavior described in the skill overview. <br>
Mitigation: Review the target directory and generated file list before running the scripts, and use a disposable or controlled working directory. <br>
Risk: Path-like template names, output directories, or initialized template names can write files in locations the user did not intend. <br>
Mitigation: Avoid using important project folders as output targets unless the file writes have been reviewed and are expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/template-tool) <br>
- [Publisher profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Plain text and generated files from templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read JSON variable files and may create or overwrite files when template initialization or project template generation is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
