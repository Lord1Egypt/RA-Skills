## Description: <br>
Review who attended a Google Meet conference and for how long. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Workspace administrators and team operators use this recipe to review Google Meet attendance by listing conference records, participants, and participant session details with the Google Workspace CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recipe can expose Google Meet attendance records available to the configured Google Workspace account. <br>
Mitigation: Use an account that is authorized to review the target meeting records and confirm the records are appropriate to inspect before running the commands. <br>
Risk: The workflow depends on the local `gws` binary and `gws-meet` skill. <br>
Mitigation: Install `gws` and `gws-meet` only from trusted sources before using the recipe. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-review-meet-participants) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Google Workspace CLI binary `gws` and the `gws-meet` skill; uses the permissions of the configured Google Workspace account.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
