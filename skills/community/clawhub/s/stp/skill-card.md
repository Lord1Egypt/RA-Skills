## Description: <br>
Structured Task Planning V2 turns a user-approved plan into asynchronous subagent steps with verification, status tracking, heartbeat monitoring, and interruption support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scotthuang](https://clawhub.ai/user/scotthuang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to break complex tasks into confirmed, serial steps that run in isolated subagents while the main session remains available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create subagents and recurring heartbeat jobs that continue work outside the main session. <br>
Mitigation: Use explicit /stp-style invocation, review the generated plan before confirming, and monitor or interrupt task IDs when work should stop. <br>
Risk: Cleanup behavior may terminate work, delete cron jobs, or remove task records. <br>
Mitigation: Do not enable task-directory deletion unless losing those task artifacts is acceptable, and confirm interruption requests before cleanup. <br>
Risk: The skill can inspect global OpenClaw session history while checking subagent status. <br>
Mitigation: Avoid sensitive prompts and install only in environments where session-history access is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scotthuang/stp) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown plans and task status files with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces plan files, task step tracking, subagent prompts, heartbeat status, and cleanup records.] <br>

## Skill Version(s): <br>
1.0.7 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
