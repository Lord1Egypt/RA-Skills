## Description: <br>
多 Agent 协作调度。将大任务拆分为子任务，分配给多个 Agent 并行执行，自动汇总结果。Team Lead 负责拆分、分发、监控、汇总。触发词：协作、swarm、分工、团队任务、并行执行、多 Agent、team work。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wavmson](https://clawhub.ai/user/wavmson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Swarm Coord to break complex, multi-domain requests into parallel subtasks, dispatch them to specialized agents, monitor progress, and aggregate the results into one report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation and multi-agent dispatch can cause work to begin before the user has checked whether the decomposition matches their intent. <br>
Mitigation: Review and approve the proposed subtask plan before execution, especially for messages, document edits, commits, pushes, or other user-visible actions. <br>
Risk: Child agents may receive more context or credentials than they need for a subtask. <br>
Mitigation: Give child agents only the files, credentials, and task context required for their assigned work. <br>
Risk: Task-state or memory persistence can retain sensitive work context after a swarm run. <br>
Mitigation: Disable or avoid memory and task-state persistence for sensitive work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wavmson/swarm-coord) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text, shell commands] <br>
**Output Format:** [Markdown task plans, coordination updates, and final summary reports with occasional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include subtask assignments, dependency notes, progress states, retries, skipped tasks, and aggregated results.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
