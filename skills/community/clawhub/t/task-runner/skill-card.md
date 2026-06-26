## Description: <br>
Manage and track tasks and projects persistently with priorities, completion status, filtering, and secure markdown export across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johstracke](https://clawhub.ai/user/johstracke) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agents use Task Runner to keep persistent task lists for multi-session projects, sprint planning, experiment tracking, and progress reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores task data persistently on the local filesystem, which may retain sensitive task descriptions across sessions. <br>
Mitigation: Review the storage location before use and avoid adding secrets or sensitive data to task descriptions. <br>
Risk: Markdown export writes files to user-selected paths within allowed directories. <br>
Mitigation: Confirm export paths before writing files and keep exports within expected workspace, home, or /tmp locations. <br>
Risk: The skill may activate for broad task or productivity requests. <br>
Mitigation: Confirm that persistent task tracking is intended before adding, completing, reprioritizing, or exporting tasks. <br>


## Reference(s): <br>
- [Task Runner on ClawHub](https://clawhub.ai/johstracke/task-runner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Terminal text and Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists task data as JSON under ~/.openclaw/workspace/tasks_db.json; markdown export paths are restricted to workspace, home, and /tmp locations while blocking system paths and sensitive dotfiles.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
