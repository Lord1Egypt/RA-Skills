## Description: <br>
Set up a new Google Tasks list with initial tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this recipe to create a Google Tasks task list and seed it with initial planning tasks through the Google Workspace CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands will create a real Google Tasks task list and sample tasks in the Google account currently authenticated through gws. <br>
Mitigation: Confirm that gws is authenticated to the intended Google account and replace the sample list title, task names, notes, and due date before running the commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-create-task-list) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and the gws-tasks skill; commands create a task list, add sample tasks, and list the resulting tasks.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence); artifact metadata version 0.22.5 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
