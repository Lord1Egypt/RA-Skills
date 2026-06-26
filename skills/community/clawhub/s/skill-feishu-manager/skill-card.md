## Description: <br>
Comprehensive Feishu management toolkit for documents, knowledge bases, bitables, and cloud storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[limoxt](https://clawhub.ai/user/limoxt) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Workspace administrators, operations teams, and developers use this skill to have an agent manage Feishu documents, wiki pages, bitables, and drive folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or modify live Feishu workspace content. <br>
Mitigation: Use a dedicated Feishu app, grant only the scopes and workspace access needed, and review create or write requests before execution. <br>
Risk: A leaked Feishu app_secret could expose workspace data or write access. <br>
Mitigation: Store the app_secret in a protected secret store or environment configuration, avoid logging it, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/limoxt/skill-feishu-manager) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline JSON, YAML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials and scoped permissions for documents, wiki, drive, and bitable access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
