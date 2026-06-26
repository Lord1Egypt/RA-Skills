## Description: <br>
Manage WEEEK Task Manager work through the WEEEK Public API, including listing, creating, updating, completing, reopening, and moving tasks across boards and columns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex-indi](https://clawhub.ai/user/alex-indi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and WEEEK users use this skill to operate WEEEK tasks, boards, projects, and board columns from an agent workflow. It is suited for task-management automation where the user can review reads and writes before running them against a workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a WEEEK API token to access task-management data. <br>
Mitigation: Keep WEEEK_TOKEN private, use the narrowest available token permissions, and avoid exposing command output that contains workspace data. <br>
Risk: Create, update, complete, uncomplete, and move commands can change tasks in a WEEEK workspace. <br>
Mitigation: Review the target task, board, column, and payload before executing write commands, especially in shared workspaces. <br>


## Reference(s): <br>
- [WEEEK Public API reference](references/api.md) <br>
- [WEEEK Public API base URL](https://api.weeek.net/public/v1) <br>
- [ClawHub skill page](https://clawhub.ai/alex-indi/weeek-tasks) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands call the WEEEK Public API using WEEEK_TOKEN and may return JSON responses from WEEEK.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
