## Description: <br>
Manage TODO.md todo lists through Telegram commands to query, organize, and complete tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hengbo12345](https://clawhub.ai/user/hengbo12345) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent workflows use this skill to manage a Markdown todo list from Telegram. It supports listing tasks, adding or editing entries, deleting or moving items, and marking tasks complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and rewrites the workspace TODO.md file, so mistaken commands or parser behavior can change important todo content. <br>
Mitigation: Keep backups or version control for TODO.md and review changes after organize, execute, delete, or move operations. <br>
Risk: Security evidence notes task-number reliability issues for complete and delete behavior. <br>
Mitigation: Confirm task numbers with /todo query before mutating tasks and verify TODO.md after completion or deletion. <br>
Risk: Todo contents may be displayed through the Telegram workflow. <br>
Mitigation: Avoid storing secrets or sensitive private data in TODO.md, and treat the file as data rather than trusted instructions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hengbo12345/telegram-todolist) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, files, guidance] <br>
**Output Format:** [Telegram-ready text summaries, Markdown todo entries, and TODO.md file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and rewrites /root/.openclaw/workspace/TODO.md; task-number operations should be reviewed because security evidence notes reliability issues.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
