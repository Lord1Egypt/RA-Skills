## Description: <br>
Generates and updates living reference documentation by extracting schemas, parameters, and configuration from code and system files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brad-sl](https://clawhub.ai/user/brad-sl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create persistent reference documentation for codebases and systems so future agent sessions can reuse current schemas, configuration, architecture notes, and operational guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reference files may preserve sensitive configuration or credential details from the source material. <br>
Mitigation: Run the skill only on explicitly chosen paths, avoid secrets and credential stores, and review generated files before reuse or commit. <br>
Risk: The skill writes durable documentation outputs that future sessions may treat as trusted references. <br>
Mitigation: Review generated Markdown, YAML, and JSON outputs for accuracy, scope, and sensitive content before using them as long-lived context. <br>


## Reference(s): <br>
- [Documentation Template](artifact/references/templates/documentation_template.md) <br>
- [Reference Schema Template](artifact/references/templates/schema.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown, YAML, and JSON reference files with supporting shell commands and guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces durable local documentation files and may write a generation log.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
