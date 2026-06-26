## Description: <br>
Notify guides agents to send timely, batched notifications through appropriate channels while respecting user preferences, quiet hours, and escalation limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent builders use this skill to choose notification channels, timing, batching, message formats, and escalation behavior for user-facing alerts and summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notification bodies may be sent through an external email API example. <br>
Mitigation: Confirm recipients are user-approved and avoid sending secrets or regulated data in notification content. <br>
Risk: The optional API example uses a sensitive SKILLBOSS_API_KEY credential. <br>
Mitigation: Store the key securely and grant only the least privilege needed for notification delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/toby-notify) <br>
- [SkillBoss API Hub endpoint](https://api.skillbossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with tables, examples, checklists, and a Python API example] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional third-party email API usage; notification recipients and content should be user-approved.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
