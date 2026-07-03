## Description: <br>
Track in-session work progress by registering multi-step tasks, updating task status, and guiding cleanup or resume workflows across supported agent environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to keep multi-step work visible, preserve in-progress state, and resume remaining tasks after interruptions or context compaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can clean or delete task state automatically, which may remove useful work-tracking context. <br>
Mitigation: Review pending and completed task state before installation, and require explicit confirmation before deleting task records or home-directory state. <br>
Risk: The skill may run external verification commands based on task text. <br>
Mitigation: Review proposed shell, network, repository, and deployment checks before execution and scope them to the current task. <br>
Risk: The ClawHub security scan classified the release as suspicious because task-state cleanup and external checks are not sufficiently scoped by the skill text. <br>
Mitigation: Deploy only after security review, and prefer a version that requires explicit user confirmation for shell or network checks and destructive state changes. <br>


## Reference(s): <br>
- [WIP skill overview](SKILL.md) <br>
- [Resume workflow](resume.md) <br>
- [Claude Code WIP guide](claude.md) <br>
- [Antigravity WIP tracking](antigravity.md) <br>
- [ClawHub skill page](https://clawhub.ai/drumrobot/skills/wip) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with task checklists, tool-call patterns, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or update task tracking artifacts such as TodoWrite entries, task.md, checklist.md, fix_plan.md, or WIP commit guidance.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata and CHANGELOG, released 2026-06-30) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
