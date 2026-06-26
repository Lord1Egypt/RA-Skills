## Description: <br>
Manage tasks and projects using the TaskBoardAI Kanban system. Includes MCP server integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyddd](https://clawhub.ai/user/hyddd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams using Clawdbot use this skill to create, start, block, complete, and summarize TaskBoardAI Kanban cards through an MCP integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task details and summaries may be retained in TaskBoardAI outside the chat. <br>
Mitigation: Avoid saving secrets or sensitive business data in task cards, and install the skill only when external task retention is acceptable. <br>
Risk: The MCP server path and npm package dependency must match the user's local TaskBoardAI installation. <br>
Mitigation: Verify the installed npm package and update the MCP server path before enabling the skill. <br>
Risk: Broad automatic task triggers can create or update cards when the user did not intend persistent tracking. <br>
Mitigation: Narrow the optional AGENTS.md trigger so card creation happens only after explicit user commands. <br>


## Reference(s): <br>
- [TaskBoardAI](https://github.com/taskboardai/taskboardai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell and XML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Task card content is intended to be stored as Markdown in TaskBoardAI.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
