## Description: <br>
Validate YAML syntax using python3, lint configs, and convert YAML to JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to validate YAML files, lint common formatting issues, convert YAML to JSON, and inspect top-level keys during configuration work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YAML content may be printed to the terminal when converting files or previewing keys, which can expose secrets in logs or shared sessions. <br>
Mitigation: Run the skill only on YAML files whose contents are acceptable to display, and avoid converting or previewing files that contain secrets. <br>
Risk: Without PyYAML, validation and conversion use basic fallback checks that are less complete than full YAML parsing. <br>
Mitigation: Install PyYAML and rerun validation before relying on results for production configuration changes. <br>


## Reference(s): <br>
- [Yamlcheck on ClawHub](https://clawhub.ai/bytesagain-lab/yamlcheck) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown with command examples and terminal-oriented diagnostic text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit JSON when converting YAML with the to-json command.] <br>

## Skill Version(s): <br>
3.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
