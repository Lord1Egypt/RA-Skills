## Description: <br>
Set timers and alarms. When a background timer completes, you receive a System notification - respond with the reminder message (NOT HEARTBEAT_OK) to notify the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hisxo](https://clawhub.ai/user/hisxo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to start background countdown timers, monitor or cancel running timers, and receive a reminder message when a timer completes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Each timer starts a local background Node process. <br>
Mitigation: Use the documented process list, poll, log, and kill controls to monitor or cancel running timers. <br>
Risk: Reminder labels are passed through shell command examples. <br>
Mitigation: Keep reminder labels simple or safely quoted when starting timers. <br>
Risk: On macOS, completed timers may play a system notification sound. <br>
Mitigation: Install only in environments where a local sound notification is acceptable. <br>


## Reference(s): <br>
- [Timer Skill on ClawHub](https://clawhub.ai/hisxo/timer) <br>
- [hisxo Publisher Profile](https://clawhub.ai/user/hisxo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands and timer status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Timer completion output includes the reminder label when one is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
