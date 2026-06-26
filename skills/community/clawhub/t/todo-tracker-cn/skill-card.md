## Description: <br>
生成、跟踪和验证待办列表的执行状态。提供 generate-todo-list, mark-completed, show-progress, verify-completion 四个核心动作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elderyang](https://clawhub.ai/user/elderyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents, developers, and operators use this skill to create, update, display, and verify task checklists for multi-step work. It is most useful when an agent needs to make execution progress visible and confirm that planned steps are complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task names, timestamps, completion details, and progress history may persist in long-lived local files beyond the current todo database. <br>
Mitigation: Do not put secrets, credentials, customer data, incident details, or other sensitive information in task titles or todo items; periodically review and clean local memory and history files. <br>
Risk: The skill reads and writes local todo state and may append progress records to a local memory file. <br>
Mitigation: Run it only in the intended user workspace and review the local todo and memory files if the workspace is shared with other agents or users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elderyang/todo-tracker-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-like command output from Python CLI actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes todo state to local files under the user's OpenClaw workspace when actions are executed.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
