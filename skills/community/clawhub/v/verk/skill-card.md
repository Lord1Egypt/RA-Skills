## Description: <br>
Manage tasks, projects, and workflows in Verk task management, including creating, updating, assigning, tracking, commenting on, and listing automation flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhibavishi](https://clawhub.ai/user/abhibavishi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to manage Verk tasks, projects, comments, status, priority, assignment, and automation workflow listings from an agent through the bundled Node.js CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can immediately delete Verk tasks when given a task ID. <br>
Mitigation: Confirm exact task IDs and user intent before running delete operations. <br>
Risk: The skill uses a Verk API key and organization ID to access organization task data. <br>
Mitigation: Use a scoped, revocable API key and provide it only in the expected VERK_API_KEY environment variable. <br>
Risk: VERK_API_URL can redirect requests to an alternate API server. <br>
Mitigation: Set VERK_API_URL only when the alternate Verk-compatible API endpoint is intentionally trusted. <br>


## Reference(s): <br>
- [Verk website](https://verkapp.com) <br>
- [ClawHub skill listing](https://clawhub.ai/abhibavishi/verk) <br>
- [Publisher profile](https://clawhub.ai/user/abhibavishi) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, VERK_API_KEY, and VERK_ORG_ID; command results are returned as JSON and should be summarized for users.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
