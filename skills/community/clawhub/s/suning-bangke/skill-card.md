## Description:

苏宁帮客预约服务，支持用户输入手机号和故障描述进行服务预约下单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[miantiaor](https://clawhub.ai/user/miantiaor)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support agents use this skill to collect a phone number and fault description, confirm the details, and submit a Suning Bangke service appointment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit real appointment requests to a production Suning endpoint.

Mitigation: Use it only for explicit Suning Bangke booking requests and require clear user confirmation before submission.

Risk: Phone numbers and fault descriptions may contain personal or sensitive information.

Mitigation: Tell the user exactly what data will be sent and avoid exposing real personal data in visible command-line arguments or logs.

Risk: Generic repair complaints may activate the skill when the user did not intend to book Suning Bangke service.

Mitigation: Confirm that the user wants a Suning Bangke appointment before collecting contact details or making an API request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/miantiaor/skills/suning-bangke)
- [Suning Bangke service reservation endpoint](https://asapps.suning.com/asapps/mcp/serviceReserveNew)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit phone number and fault description to a production Suning service endpoint after user confirmation.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
