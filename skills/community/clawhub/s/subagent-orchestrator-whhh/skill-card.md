## Description: <br>
Breaks complex agent tasks into planned subagent workstreams with persistent task files, workspace management, checkpoints, queued messages, progress updates, and final delivery summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whhh1994](https://clawhub.ai/user/whhh1994) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multi-step work that benefits from subagents, persistent intermediate artifacts, and explicit progress tracking. It is intended for tasks with more than three steps, multiple sources or platforms, or context growth risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad automation powers, including spawning subagents, reading and writing files, running shell commands, scheduling work, and sending progress messages. <br>
Mitigation: Install only when that orchestration behavior is intended, and review the proposed plan, workspace path, required tools, and command scope before allowing execution. <br>
Risk: Persistent task workspaces, memory notes, checkpoints, and message queues may retain sensitive task details or intermediate artifacts. <br>
Mitigation: Confirm where task files and memory entries will be written, avoid sensitive inputs unless necessary, and define cleanup expectations before using the skill for sensitive work. <br>
Risk: The skill sends progress and completion results back to the initiating channel, which can expose outputs if the destination is misidentified. <br>
Mitigation: Verify the notification destination and require delivery proof that points to the expected channel or thread. <br>
Risk: Activation behavior is broad for multi-step, multi-source, or context-heavy tasks. <br>
Mitigation: Confirm that subagent orchestration is appropriate for the request before proceeding, especially for short tasks that do not need delegation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/whhh1994/subagent-orchestrator-whhh) <br>
- [Path Reference](artifact/references/paths.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with task plans, status updates, file paths, shell commands, and structured handoff notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local task workspaces, plan files, status files, data files, checkpoints, message queues, and delivery checklists when used by an agent with the required tools.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata, released 2026-05-25) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
