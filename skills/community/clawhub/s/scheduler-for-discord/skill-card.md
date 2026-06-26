## Description: <br>
Create and manage scheduled reminders and posts for Moltbot, especially delivery back to the current Discord channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AaronWander](https://clawhub.ai/user/AaronWander) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Moltbot users and operators use this skill to turn natural-language reminder or recurring-post requests into scheduled jobs. It is most useful for Discord workflows where the agent should capture the current channel at setup time and deliver the scheduled message there later. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled jobs can post to Discord after the original chat ends. <br>
Mitigation: Before installing or running the skill, confirm the destination channel ID, schedule, timezone, message content, and how to list or cancel the job. <br>
Risk: Recurring schedules or channel targets may be incorrect if the request is ambiguous. <br>
Mitigation: Verify the explicit channel target and schedule details before creating recurring jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AaronWander/scheduler-for-discord) <br>
- [Publisher profile](https://clawhub.ai/user/AaronWander) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Moltbot cron command guidance that may create one-shot or recurring Discord delivery jobs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
