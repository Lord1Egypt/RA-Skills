## Description: <br>
Spawn isolated subagents to handle long-running, complex, or blocking tasks without stalling the main session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to decide when to delegate slow, multi-step, or blocking work to a subagent and how to provide clear task boundaries, timeouts, completion criteria, and failure handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated subagents may access private email, calendar data, credentials, external accounts, or private output files if examples are copied into real workflows without scoping. <br>
Mitigation: Require explicit user approval before a subagent touches private accounts or credentials, and include narrow input paths, account scopes, output locations, and retention expectations in each task. <br>
Risk: Long-running background tasks can fail, time out, or produce incomplete results without immediate user visibility. <br>
Mitigation: Set a timeout for each subagent task, require a clear completion signal, review generated output before use, and fall back to the main session when retries fail. <br>


## Reference(s): <br>
- [Spawn Subagent release page](https://clawhub.ai/netanel-abergel/spawn-subagent) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands] <br>
**Output Format:** [Markdown guidance with Python-style delegation examples and task templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended as instructions for an agent to spawn and monitor delegated background work.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
