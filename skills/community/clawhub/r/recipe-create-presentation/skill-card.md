## Description: <br>
Create a new Google Slides presentation and add initial slides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace automation users use this recipe to create a Google Slides presentation, capture its presentation ID, and add an initial Drive sharing permission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recipe includes a persistent Google Drive sharing step to a fixed email address outside its core presentation-creation purpose. <br>
Mitigation: Remove or edit the sharing command unless that recipient should receive edit access. <br>
Risk: Running Drive permission commands with the wrong Google account, file ID, recipient, or role can expose the presentation unintentionally. <br>
Mitigation: Confirm the active Google account, presentation file ID, recipient email, and permission role before executing the command. <br>


## Reference(s): <br>
- [Recipe Create Presentation on ClawHub](https://clawhub.ai/googleworkspace-bot/recipe-create-presentation) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws command-line tool and the gws-slides skill.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
