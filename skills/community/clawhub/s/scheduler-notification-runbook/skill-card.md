## Description: <br>
A runbook for creating, reviewing, validating, and troubleshooting scheduled reminders and notification workflows with OpenClaw cron. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atomiccn](https://clawhub.ai/user/atomiccn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this runbook to design, review, validate, and troubleshoot scheduled reminders and notification workflows that use OpenClaw cron. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled agent jobs or webhook delivery could notify the wrong destination or send unnecessary data. <br>
Mitigation: Confirm the destination, session target, and payload with the user; avoid secrets and unnecessary personal data; periodically review recurring or named-session jobs. <br>
Risk: Reminder text, schedule choices, or timezone assumptions could make a delivered notification confusing or late. <br>
Mitigation: Use future-readable reminder text and validate the schedule shape, enabled state, timezone assumptions, job identifier, run history, and delivery location. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/atomiccn/scheduler-notification-runbook) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with decision rules, checklists, and examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only runbook; no executable code or tool calls are included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
