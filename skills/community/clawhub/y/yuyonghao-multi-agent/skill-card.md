## Description: <br>
Multi Agent coordinates specialized planner, executor, reviewer, and coordinator roles to decompose, execute, review, and aggregate work across multi-step agent tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to coordinate role-based agent teams for complex tasks that benefit from planning, tool-assisted execution, review, and result aggregation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Executor behavior can grant broad local file, web, and command authority through the external react-agent dependency and direct tool execution. <br>
Mitigation: Run the skill only in a trusted or disposable workspace and require sandboxing or explicit approval for file writes, web access, and command execution. <br>
Risk: Tasks containing untrusted text may steer tool-using agents toward unsafe local actions. <br>
Mitigation: Avoid untrusted task input until the executor is constrained and review planned tool use before execution. <br>
Risk: The executor includes a shell-command fallback path. <br>
Mitigation: Disable or wrap shell execution with an allowlist and time-limited, least-privilege sandbox before broader deployment. <br>


## Reference(s): <br>
- [Multi Agent ClawHub listing](https://clawhub.ai/yuyonghao-123/yuyonghao-multi-agent) <br>
- [Publisher profile](https://clawhub.ai/user/yuyonghao-123) <br>
- [Foundation of Multi-Agent Systems](https://www.masfoundations.org/) <br>
- [FIPA ACL Message Structure Specification](http://www.fipa.org/specs/fipa00061/) <br>
- [SharedPlans Theory](https://www.aaai.org/Papers/AAAI/1996/AAAI96-066.pdf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Console output, JavaScript API results, markdown guidance, code snippets, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs vary by execution mode and can include task plans, per-agent execution results, review scores, approval status, timing, and aggregate statistics.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
