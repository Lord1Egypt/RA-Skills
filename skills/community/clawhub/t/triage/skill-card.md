## Description: <br>
Auto-learns to prioritize tasks by urgency, impact, and user patterns. Grows smarter with each decision. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to help an agent classify incoming work by urgency and importance, route P0-P3 tasks, and learn confirmed priority preferences from repeated corrections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Learned priority rules and override notes may capture sensitive client, personnel, security, or operational details if users include them in task descriptions. <br>
Mitigation: Avoid storing sensitive details in priority notes, keep learned rules at the category level where possible, and periodically review or remove stored patterns. <br>
Risk: Stale or overgeneralized learned rules may cause the agent to misclassify urgency or interrupt work unnecessarily. <br>
Mitigation: Confirm durable rules only after repeated corrections, ask when priority signals conflict, and review learned rules periodically. <br>


## Reference(s): <br>
- [Triage ClawHub release](https://clawhub.ai/ivangdavila/triage) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Conversational text and markdown priority notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces priority labels, queue ordering guidance, and proposed learned priority rules for user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
