## Description: <br>
Maintains local relationship memory by recording people profiles, future birthdays or appointments, reminders, and past shared experiences for later lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yujintang](https://clawhub.ai/user/yujintang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users use this skill to maintain a local social relationship memory, record upcoming birthdays, anniversaries, and appointments, archive past interactions, and receive reminder outputs from a recurring scan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive relationship details such as personal facts, birthdays, addresses, phone numbers, and shared history in local JSON files. <br>
Mitigation: Use a protected data directory, avoid storing unnecessary sensitive details, and periodically review or delete stored relationship records. <br>
Risk: The installation flow configures a recurring reminder scan every 15 minutes. <br>
Mitigation: Install only when persistent reminders are desired, and review the configured OpenClaw cron job after installation. <br>
Risk: Reminder text may be sent to an external service when RELATION_KEEPER_CHANNEL is configured. <br>
Mitigation: Configure external reminder channels only for trusted destinations and avoid including sensitive personal details in reminders. <br>
Risk: The bundled sample profile may contain placeholder personal data that is not relevant to the user. <br>
Mitigation: Review or delete bundled sample data before using the skill for real relationship records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yujintang/relation-keeper) <br>
- [Publisher profile](https://clawhub.ai/user/yujintang) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON data] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-backed local data updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local relationship and reminder records and may emit reminder text from scheduled scans.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
