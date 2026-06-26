## Description: <br>
Remind Me creates, lists, and cancels channel-scoped one-time or recurring reminders, using timezone-aware scheduling to deliver reminders back to the originating chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youpele52](https://clawhub.ai/user/youpele52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to schedule, review, and cancel chat-based reminders or recurring jobs after confirming reminder content, schedule, delivery context, and timezone. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cancel feature can delete reminders without verifying they belong to the current chat. <br>
Mitigation: List reminders for the current channel and chat first, verify the reminder tag, and cancel only a matching scoped job. <br>
Risk: Shared or multi-chat environments can expose reminders to unintended cancellation if channel context is not enforced. <br>
Mitigation: Require channel and chat context for all cancel operations and prefer job IDs obtained from the scoped reminder list. <br>
Risk: The skill may read USER.md for timezone and may update it when a timezone is missing. <br>
Mitigation: Read only the timezone field needed for scheduling and update USER.md only after explicit user consent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/youpele52/remind-me-pro) <br>
- [Publisher profile](https://clawhub.ai/user/youpele52) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command invocations and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses channel and chat scoping tags plus timezone labels in reminder descriptions.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
