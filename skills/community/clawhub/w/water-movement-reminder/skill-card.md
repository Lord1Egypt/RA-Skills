## Description: <br>
Sends hydration and movement reminders every 45 minutes from 8:00 to 23:00 to promote healthy work habits and prevent prolonged sitting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RenchZhao](https://clawhub.ai/user/RenchZhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to schedule recurring hydration, movement, and eye-rest reminders during extended work sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: USER.md and heartbeat-state.json may contain a channel or session identifier. <br>
Mitigation: Keep those files private and review their contents before enabling the skill. <br>
Risk: Recurring reminders may run at an unexpected cadence or outside the intended working-hours window if heartbeat or timezone settings are misconfigured. <br>
Mitigation: Review the heartbeat setting and the GMT+8 8:00-23:00 reminder window before enabling the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RenchZhao/water-movement-reminder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reminder behavior guidance and configuration notes for local heartbeat state and channel delivery.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
