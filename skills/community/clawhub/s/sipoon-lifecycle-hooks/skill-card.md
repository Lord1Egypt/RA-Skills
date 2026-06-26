## Description: <br>
Lifecycle Hooks guides agents in simulating OpenClaw lifecycle events with heartbeat polling, subagent session callbacks, cron-based session-end checks, and behavior-level task completion detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sipoon](https://clawhub.ai/user/sipoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to plan lifecycle automation for OpenClaw sessions, including subagent lifecycle logging, session-end memory updates, and task-completion checks. It is most useful when teams need hook-like behavior while recognizing that tool-level hooks depend on explicit agent behavior conventions rather than automatic interception. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lifecycle automation may schedule session-end checks, spawn subagents, and write memory or heartbeat state. <br>
Mitigation: Install only when that behavior is desired, prefer explicit commands, and confirm before enabling persistent hook behavior. <br>
Risk: Pre-tool-use and post-tool-use hooks are not automatically intercepted by the OpenClaw kernel. <br>
Mitigation: Use explicit agent behavior rules for high-risk operations, including confirmation before destructive actions. <br>
Risk: Behavior-level task-completion detection can miss events or produce misleading hook signals. <br>
Mitigation: Review proposed lifecycle behavior before deployment and scan the skill as part of release validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sipoon/sipoon-lifecycle-hooks) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python-like pseudocode, trigger phrases, and configuration patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose heartbeat, cron, subagent, and memory-writing patterns; does not provide kernel-level tool interception.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
