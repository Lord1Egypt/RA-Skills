## Description: <br>
Activates Sport Mode to temporarily increase OpenClaw heartbeat frequency, write a monitoring task to HEARTBEAT.md, and reset cleanup when finished. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[l1veIn](https://clawhub.ai/user/l1veIn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to supervise long-running builds, coding agents, migrations, or other tasks that need short-interval heartbeat checks and a clear auto-off condition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-frequency heartbeat settings can keep OpenClaw checking a task more often than intended. <br>
Mitigation: Include a clear stop condition in the task and run sport-mode off when monitoring is finished. <br>
Risk: Sport Mode writes to HEARTBEAT.md and clears it when turned off. <br>
Mitigation: Back up or review any existing HEARTBEAT.md before activating the skill. <br>
Risk: Task text can influence active agent behavior. <br>
Mitigation: Do not put secrets or untrusted instructions in the monitoring task. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/l1veIn/sport-mode) <br>
- [Publisher Profile](https://clawhub.ai/user/l1veIn) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and generated HEARTBEAT.md content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a task for on mode; accepts an optional heartbeat interval.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
