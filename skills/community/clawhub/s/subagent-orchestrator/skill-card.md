## Description: <br>
Orchestrate OpenClaw subagents for continuous autopilot workflows, including task-line continuation, structured handoffs, memory preservation, and task-board updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hackjsw](https://clawhub.ai/user/hackjsw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to manage multi-round OpenClaw subagent workflows without dropping active task lines. It helps route handoffs, require compact structured returns, update task boards, and preserve durable memory records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory records can retain sensitive or stale instructions from completed subagent sessions. <br>
Mitigation: Review MEMORY.md and daily memory records, and keep only durable task facts, current rules, risks, and next steps. <br>
Risk: Continuous autopilot workflows can continue beyond the intended scope if task boards do not define goals, stop conditions, and allowed scope clearly. <br>
Mitigation: Keep AGENT_TASK_BOARD entries explicit about the objective, current node, completion condition, blocker states, and permitted follow-up roles. <br>
Risk: Cleanup of temporary artifacts can remove proof needed to verify external deliveries. <br>
Mitigation: Preserve screenshot or delivery proof artifacts before cleanup when a human-checkable record may be needed. <br>


## Reference(s): <br>
- [SUBAGENT_RECORD_PROTOCOL](references/SUBAGENT_RECORD_PROTOCOL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown task records and concise structured status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses structured headers for tag, line, node, goal_status, and next_role.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, README.md, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
