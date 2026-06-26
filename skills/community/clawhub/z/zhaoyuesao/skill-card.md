## Description: <br>
找月嫂 helps users request matched maternity-care service support by collecting city, due-date, service-period, budget, and verified phone contact details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dj-skillhub](https://clawhub.ai/user/dj-skillhub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users looking for yuesao maternity and newborn-care services use this skill to provide appointment details, verify a phone number, and submit a service-matching request to a provider. <br>

### Deployment Geography for Use: <br>
Mainland China <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive personal information, including phone number, SMS verification code, due date, city, service period, and budget. <br>
Mitigation: Confirm the collected details with the user before submission, mask phone numbers in responses, and avoid retaining or exposing raw verification data outside the intended workflow. <br>
Risk: ClawScan flagged under-disclosed backend routing and logging concerns for the provider workflow. <br>
Mitigation: Review the ClawHub security guidance before installation and use the skill only when the user is comfortable sending the listed details to the provider. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/dj-skillhub/zhaoyuesao) <br>
- [Command reference](references/commands.md) <br>
- [Error handling reference](references/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown-style conversational text with command invocations for the agent to execute] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Collects and confirms appointment details before phone verification; phone numbers should be displayed only in masked form.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
