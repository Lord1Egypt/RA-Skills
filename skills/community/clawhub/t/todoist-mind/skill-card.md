## Description: <br>
Provides Todoist task-management commands and a utility script for adding tasks, completing or deleting tasks, and listing projects or tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AI-MindMarket](https://clawhub.ai/user/AI-MindMarket) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Todoist task workflows from an agent, including creating tasks with due dates and priorities, completing or deleting known tasks, and navigating projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A plaintext Todoist token is bundled with the skill evidence. <br>
Mitigation: Revoke the bundled token, replace it with a placeholder, and require credentials to be supplied through approved secret handling before installation. <br>
Risk: The skill can sync, list, complete, and delete Todoist account data while being described as a mock. <br>
Mitigation: Disclose live account access clearly and require explicit confirmation before destructive actions such as completing or deleting tasks. <br>
Risk: Task and project data can contain sensitive personal or business information. <br>
Mitigation: Avoid logging task contents, task IDs, project names, tokens, or raw API error bodies unless debugging is explicitly enabled and protected. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/AI-MindMarket/todoist-mind) <br>
- [Publisher Profile](https://clawhub.ai/user/AI-MindMarket) <br>
- [Todoist API v2](https://api.todoist.com/api/v2) <br>
- [Clawdis Homepage](https://t.me/fugguri) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Todoist credentials and may read or modify Todoist account data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
