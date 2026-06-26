## Description: <br>
Manages work todo items, including adding, viewing, completing, deleting, progress updates, deadlines, and daily work summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liumeixin](https://clawhub.ai/user/liumeixin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and individual work users use this skill to maintain local work todo records, update task status and progress, and generate categorized daily work summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Todo entries may contain sensitive work details stored in a local JSON file. <br>
Mitigation: Confirm local file permissions and backups are appropriate, and avoid storing highly sensitive details unless those controls are acceptable. <br>
Risk: The skill can create, edit, and delete todo entries in the disclosed local todo file. <br>
Mitigation: Review requested task changes before applying them, especially deletion or bulk update requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liumeixin/work-todo) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON task records and Python-style implementation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores todo data in the disclosed local JSON path ~/.openclaw/workspace/shared/work-todo/lwork/todos.json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
