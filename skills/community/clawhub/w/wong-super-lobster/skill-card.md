## Description: <br>
Super Lobster helps organize Feishu meeting notes, classify work tasks, create daily todo documents, manage sharing permissions, and support scheduled productivity updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ybridge](https://clawhub.ai/user/ybridge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operators who coordinate work in Feishu can use this skill to turn meeting notes into categorized daily todo documents, set document permissions, and send scheduled task updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports an embedded Feishu app secret in the skill package. <br>
Mitigation: Remove the embedded secret, rotate the credential, and configure credentials through a reviewed local secret store before installation. <br>
Risk: The skill uses fixed recipient identifiers and can grant edit access to generated Feishu documents. <br>
Mitigation: Replace fixed IDs with user-controlled configuration and require explicit confirmation before granting permissions or sending notifications. <br>
Risk: The skill can read meeting notes and create or share work documents automatically. <br>
Mitigation: Review the source documents, destination workspace, and generated todo content before running automated or scheduled tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ybridge/wong-super-lobster) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Feishu documents, update permissions, and send notifications when configured and executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
