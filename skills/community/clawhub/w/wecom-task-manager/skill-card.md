## Description: <br>
WeCom Task Manager helps authorized agents manage enterprise WeCom smart-sheet tasks and goals, including creation, progress updates, status reporting, filtering, dependency handling, and completion workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhzheng222](https://clawhub.ai/user/jhzheng222) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams and authorized agents use this skill to coordinate work in a WeCom smart sheet: tracking task lifecycle state, decomposing goals into executable tasks, finding the next task, and generating status and statistics reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete live task data in the configured WeCom smart sheet. <br>
Mitigation: Use it only with a dedicated WeCom sheet and require explicit confirmation before delete_task or delete_goal operations. <br>
Risk: The security review reports an unsafe command-execution pattern around mcporter calls. <br>
Mitigation: Review and replace shell=True mcporter execution with argv-based subprocess calls before production installation. <br>
Risk: Agent identity is used as part of the access-control flow. <br>
Mitigation: Do not rely on AGENT_ID alone as an authorization boundary; pair it with trusted publisher review and environment-level controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jhzheng222/wecom-task-manager) <br>
- [API reference](references/api.md) <br>
- [Quickstart guide](QUICKSTART.md) <br>
- [Priority levels](PRIORITY_LEVELS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python API examples, shell commands, JSON configuration, and task status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read, create, update, or delete records in the configured WeCom smart sheet when invoked by an authorized agent.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
