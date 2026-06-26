## Description: <br>
分层任务分解与执行工作流，将复杂任务分解为可执行的子步骤，并提供错误处理和进度跟踪。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whoisme007](https://clawhub.ai/user/whoisme007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to break large tasks into staged plans, executable steps, progress records, and final reports. It is intended for structured workflow execution where task decomposition, retries, logging, and optional backups or email reports are useful. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and stores project files, logs, outputs, and backups that may contain task content. <br>
Mitigation: Review the configured project, logging, and backup paths before use, and avoid running it on sensitive projects unless retention and storage locations are acceptable. <br>
Risk: Optional email and backup features can transmit or copy workflow artifacts outside the active project directory. <br>
Mitigation: Keep email, cloud backup, and Git backup disabled until recipients, repositories, and storage paths have been reviewed. <br>


## Reference(s): <br>
- [Workflow overview](references/workflow_overview.md) <br>
- [ClawHub skill page](https://clawhub.ai/whoisme007/xiaolongxia-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown reports, JSON project files, Python workflow outputs, and shell or Python command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates project folders, task summaries, plans, step reports, logs, backups, and optional email or progress reports depending on configuration.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release evidence, package.json, skill.json, and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
