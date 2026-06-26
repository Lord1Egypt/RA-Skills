## Description: <br>
This skill helps users set up scheduled or recurring content pushes to WeChat Work group webhooks with daily, weekly, monthly, and advanced schedule patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luckyethan](https://clawhub.ai/user/luckyethan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations users use this skill to configure recurring messages for WeChat Work group robots. It supports webhook validation, message formatting, schedule selection, and automation setup for routine group notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a WeChat Work group robot webhook that functions like a posting credential. <br>
Mitigation: Treat webhook URLs and keys like passwords, avoid sharing them in transcripts or logs, and rotate the webhook if it is exposed. <br>
Risk: A recurring automation can post to the wrong group or at the wrong cadence if the webhook or schedule is misconfigured. <br>
Mitigation: Confirm the target group, schedule, message content, and activation status before enabling the automation; validate in a non-production group when possible. <br>
Risk: Validation and test pushes send real messages to the configured WeChat Work group. <br>
Mitigation: Use a test group for validation when possible, or warn group members before sending a test message to a production group. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luckyethan/wecom-post-in-group) <br>
- [Schedule Patterns Reference](references/schedule_patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and automation configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include masked webhook identifiers, RRULE schedule strings, date-guard logic, and formatted WeChat Work text or markdown messages.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
