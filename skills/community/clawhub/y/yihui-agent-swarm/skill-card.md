## Description: <br>
Multi-agent orchestration framework for OpenClaw that defines roles, routes tasks, manages state, and coordinates agent teams using structured YAML configs and communication protocols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1yihui](https://clawhub.ai/user/1yihui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to define role-specific agent teams, route tasks through master, specialist, and critic workflows, and keep task state visible through structured memory protocols. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can store private or sensitive team context without enough limits or deletion controls. <br>
Mitigation: Exclude secrets and private data from memory, define what may be stored, and establish a process to review or delete stored memories. <br>
Risk: External message routing can send tasks to unintended Feishu targets if sample or default targets are left in place. <br>
Mitigation: Replace all Feishu targets before use and require human approval for sensitive cross-agent routing. <br>
Risk: Broad triggers and autonomous handoffs can route work outside the intended scope. <br>
Mitigation: Narrow triggers and role domains, and document which tasks require human approval before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1yihui/yihui-agent-swarm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML configuration examples and structured message schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces role definitions, routing workflows, memory protocol guidance, and review criteria for coordinated agent teams.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
