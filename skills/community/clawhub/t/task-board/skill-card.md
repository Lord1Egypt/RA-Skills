## Description: <br>
进度任务管理 helps an agent maintain a local task board, record progress, and report current task status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanklive](https://clawhub.ai/user/tanklive) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to track todo, in-progress, blocked, completed, and cancelled work in a workspace-local task board and receive concise progress summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task notes may include secrets or sensitive personal details if users place them in task text. <br>
Mitigation: Avoid putting secrets or sensitive personal details into task descriptions, notes, or daily progress logs. <br>
Risk: Local task, memory, or learning files may accumulate unwanted or inaccurate entries over time. <br>
Mitigation: Periodically review TASKS.md, memory files, and .learnings entries, and correct or remove stale or inaccurate content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tanklive/task-board) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown task board entries, daily progress notes, and concise text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains TASKS.md, memory/YYYY-MM-DD.md, and .learnings entries when task changes or progress updates occur.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
