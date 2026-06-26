## Description: <br>
Prevent subagent timeout using checkpoint + cron wake + resume via session spawn mechanism. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cong91](https://clawhub.ai/user/cong91) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Smart Wake to keep long-running agent tasks resumable across timeout boundaries by checkpointing progress, scheduling cron wakeups, and resuming from the latest saved state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may schedule cron wakeups or spawn resume sessions without a clear approval step. <br>
Mitigation: Require explicit user approval before creating wakeups or spawned resume sessions. <br>
Risk: A resumed task may continue sensitive or irreversible work after context has changed. <br>
Mitigation: Resume only when the pending scope is clear, the checkpoint is valid, and pending wakeups can be inspected and canceled. <br>
Risk: Repeated wakeups can continue longer than intended. <br>
Mitigation: Use retry limits, cancel remaining cron jobs when work is done, and expose pending wakeups for review. <br>


## Reference(s): <br>
- [Smart Wake on ClawHub](https://clawhub.ai/cong91/smart-wake) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, JSON] <br>
**Output Format:** [Markdown guidance with JSON checkpoint and wake-cycle objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defines checkpoint, resume packet, wake-cycle status, retry-limit, and cleanup expectations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
