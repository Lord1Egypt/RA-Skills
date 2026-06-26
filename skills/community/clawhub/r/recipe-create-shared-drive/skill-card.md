## Description: <br>
Create a Google Shared Drive and add members with appropriate roles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Workspace administrators and developers use this recipe to create a Google Shared Drive, add a member with an appropriate role, and list the drive permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands could target the wrong Google account or workspace. <br>
Mitigation: Verify the active Google account and workspace before running any gws command. <br>
Risk: Incorrect placeholders, member emails, or roles could create an unintended Shared Drive or grant improper access. <br>
Mitigation: Replace placeholders carefully and double-check the drive name, drive ID, member email, and role before executing permission commands. <br>
Risk: The recipe depends on local gws tooling and the gws-drive skill. <br>
Mitigation: Confirm gws and gws-drive are installed from trusted sources before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-create-shared-drive) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires gws and the gws-drive skill; replace placeholders for request ID, drive ID, drive name, member email, and role before execution.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
