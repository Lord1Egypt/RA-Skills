## Description: <br>
Enables an AI agent to autonomously select, execute, evaluate, record, and report tasks in a recurring self-directed loop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adminlove520](https://clawhub.ai/user/adminlove520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run a self-directed task loop where the agent reads prior memory, chooses a task, executes it, self-assesses the result, and records a report. It is suited to recurring task management and continuous-improvement workflows that have explicit guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed around an autonomous recurring agent loop and does not define clear approval controls. <br>
Mitigation: Install only in a tightly scoped workspace, keep cron scheduling disabled until guardrails are explicit, and require confirmation before changes outside the memory folder or before external messages, account actions, purchases, deletions, or public publishing. <br>
Risk: Repeated self-directed execution can accumulate misleading or low-quality task records if memory files are not reviewed. <br>
Mitigation: Review memory/self-driven/tasks.md and memory/self-driven/log.md regularly and prune or correct tasks that are stale, unsafe, or unsupported. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adminlove520/self-driven) <br>
- [Publisher profile](https://clawhub.ai/user/adminlove520) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file path examples, task records, reports, and optional cron-style schedule snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs the agent to maintain memory/self-driven task and log files and may support recurring execution when separately scheduled.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
