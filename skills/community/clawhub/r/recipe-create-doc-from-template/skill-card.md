## Description: <br>
Copy a Google Docs template, fill in content, and share with collaborators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and Google Workspace users use this recipe to create a new Google Doc from a template, add initial content, and share it with collaborators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recipe can copy, edit, and share Google Drive documents through authenticated tooling. <br>
Mitigation: Review the target template ID, generated document ID, content, role, recipient type, and email address before running the commands. <br>
Risk: The required gws CLI and Google Workspace skills may affect real workspace state. <br>
Mitigation: Use the skill only in a trusted environment with the intended Google account and workspace permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-create-doc-from-template) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the gws CLI and the gws-drive and gws-docs skills.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
