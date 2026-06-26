## Description: <br>
将需求拆解为结构化任务清单，生成长时运行 Agent 的任务管理系统（基于 Anthropic Effective harnesses 方法论）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kangarooking](https://clawhub.ai/user/kangarooking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to break larger implementation requests into structured task files that can be resumed across multiple agent sessions. It is intended for project planning, progress tracking, and long-running agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add persistent workflow files and AGENTS.md guidance that influence future agent sessions. <br>
Mitigation: Review generated files before relying on the harness, especially AGENTS.md, init.sh, feature_list.json, progress.txt, and task.json. <br>
Risk: The workflow text instructs agents to commit and push changes, which could send work to a remote repository without a separate approval gate. <br>
Mitigation: Require explicit human approval before any commit or push and confirm the target remote and branch. <br>


## Reference(s): <br>
- [Task Harness Methodology](references/methodology.md) <br>
- [Harness Templates](references/templates/) <br>
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus JSON, shell script, and plain-text task files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create persistent repository workflow files such as feature_list.json, progress.txt, init.sh, task.json, and AGENTS.md guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
