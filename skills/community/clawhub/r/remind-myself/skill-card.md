## Description: <br>
Set a one-shot reminder delivered via Telegram at a specific time or after a duration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spideystreet](https://clawhub.ai/user/spideystreet) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and operators use this skill to schedule one-shot Telegram reminders through an OpenClaw gateway after confirming the reminder text and delivery time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder text containing shell metacharacters may be interpreted by the local shell when the documented command is invoked. <br>
Mitigation: Review reminder text before scheduling and avoid quotes, backticks, dollar signs, semicolons, and command substitutions until invocation hardening is verified. <br>
Risk: A reminder can be delivered to the wrong Telegram destination if the chat ID is missing or stale. <br>
Mitigation: Verify the Telegram chat ID resolved from TOOLS.md or pass an explicit chat ID before scheduling. <br>
Risk: Absolute reminder times can be interpreted in an unexpected timezone. <br>
Mitigation: Confirm the human-readable delivery time and timezone with the user before running the scheduling script. <br>


## Reference(s): <br>
- [Remind Myself on ClawHub](https://clawhub.ai/spideystreet/remind-myself) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Schedules one OpenClaw cron reminder that delivers to Telegram and deletes after it runs.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
