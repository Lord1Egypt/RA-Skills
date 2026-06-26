## Description: <br>
Smart Todo - AI智能代办管理 helps an agent create, review, update, deduplicate, remind on, and archive local todo items while preserving task context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[13770626440](https://clawhub.ai/user/13770626440) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and WorkBuddy users use this skill to manage personal or project todos through natural language, including priority tracking, duplicate detection, status updates, reminders, interruption handling, and local Markdown storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store recent conversation snippets, workspace file names, task goals, and todo context in local plaintext files. <br>
Mitigation: Use it only in workspaces where local plaintext todo storage is acceptable, narrow context capture for confidential work, and review retention and deletion practices before deployment. <br>
Risk: Security evidence reports that context can still be saved after a user declines creating a todo. <br>
Mitigation: Require review or configuration changes so a refusal stops all saving before using the skill with sensitive or regulated work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/13770626440/smart-todo) <br>
- [README](artifact/README.md) <br>
- [Todo template reference](artifact/references/todo_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Natural-language responses and Markdown todo files with JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores active and archived todos as local Markdown files and uses configurable thresholds for reminders and duplicate detection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
