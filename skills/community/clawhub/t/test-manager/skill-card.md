## Description: <br>
Manage ClickUp tasks by listing, creating, updating statuses, searching, and retrieving task details through the ClickUp API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[savelieve](https://clawhub.ai/user/savelieve) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and workflow operators use this skill to let an agent interact with a ClickUp workspace for task lookup, creation, status updates, and assignment guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create tasks or change task statuses in a ClickUp workspace. <br>
Mitigation: Require explicit confirmation before creating tasks or changing statuses in important workspaces. <br>
Risk: The ClickUp API token may grant access to workspace task data. <br>
Mitigation: Use a least-privilege ClickUp API token and avoid storing the token in shared markdown when possible. <br>


## Reference(s): <br>
- [ClickUp API v2](https://api.clickup.com/api/v2) <br>
- [ClawHub skill page](https://clawhub.ai/savelieve/test-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API calls, Guidance] <br>
**Output Format:** [Text summaries with JSON task payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ClickUp workspace, list, task, query, and status values supplied through credentials or agent/user input.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
