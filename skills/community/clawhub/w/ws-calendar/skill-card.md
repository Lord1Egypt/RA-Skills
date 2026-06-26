## Description: <br>
Helps users create schedules, set reminders, view calendar plans, and detect time conflicts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fhbillwer](https://clawhub.ai/user/fhbillwer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to manage calendar entries, reminders, schedule lookups, and basic conflict checks through natural-language calendar requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar events and reminder details may be saved locally under /workspace/data/calendar/. <br>
Mitigation: Avoid entering sensitive schedule details unless local storage is acceptable for the deployment environment. <br>
Risk: Broad time-related trigger phrases may activate the skill for ambiguous requests. <br>
Mitigation: Use clear calendar commands and confirm create or reminder actions before committing them. <br>


## Reference(s): <br>
- [Calendar on ClawHub](https://clawhub.ai/fhbillwer/ws-calendar) <br>
- [Publisher profile: fhbillwer](https://clawhub.ai/user/fhbillwer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or conversational text with calendar actions and schedule summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local calendar storage under /workspace/data/calendar/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
