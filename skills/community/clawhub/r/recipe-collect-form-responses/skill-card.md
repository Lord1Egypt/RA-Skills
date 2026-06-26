## Description: <br>
Retrieve and review responses from a Google Form. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and workspace operators use this recipe to list Google Forms, inspect a selected form, and retrieve form responses for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Form responses may contain private or business-sensitive data. <br>
Mitigation: Use the correct authorized Google account and handle retrieved responses according to applicable privacy and data-handling requirements. <br>
Risk: The recipe depends on the gws CLI and the gws-forms skill dependency. <br>
Mitigation: Install and run this skill only when those dependencies are trusted and appropriate for the target Google Workspace environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-collect-form-responses) <br>
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the gws CLI and the gws-forms dependency to read Google Form metadata and responses.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact frontmatter metadata.version is 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
