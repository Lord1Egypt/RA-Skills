## Description: <br>
Detects simple Spanish or English reminder phrases with HH:MM times, schedules a one-time reminder for today or tomorrow, and sends the alert via Telegram or console. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jul879n](https://clawhub.ai/user/jul879n) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Quick Reminder to turn chat or console messages into simple one-time reminders without a separate reminder service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder text may be sent back through the same Telegram chat or console channel where the skill was used. <br>
Mitigation: Avoid entering secrets or highly sensitive information in reminder text, and install the skill only where that delivery channel is acceptable. <br>
Risk: Scheduled reminders depend on the OpenClaw gateway process remaining alive until the reminder time. <br>
Mitigation: Use the skill for lightweight reminders where process restarts or shutdowns will not create unacceptable impact. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text scheduling confirmations and reminder messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports one-time reminders using HH:MM times; repeated reminders are not supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
