## Description: <br>
Converts Vietnamese or English reminder requests into structured JSON reminder data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AnhducNA](https://clawhub.ai/user/AnhducNA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill to turn natural-language reminder requests into structured reminder data, including title, scheduled time, recurrence, priority, and notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lunar-date reminders depend on a separate lunar conversion skill. <br>
Mitigation: Review and trust the lunar-convert skill before relying on reminders that use lunar dates. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Raw JSON object or one concise clarification question when required reminder details are missing.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs Gregorian ISO 8601 datetimes and supports custom field names when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
