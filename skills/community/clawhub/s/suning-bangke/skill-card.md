## Description: <br>
苏宁帮客预约服务，支持用户输入手机号和故障描述进行服务预约下单。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miantiaor](https://clawhub.ai/user/miantiaor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to have an agent collect a phone number and repair issue description, confirm those details, and prepare or submit a Suning Bangke service reservation. The skill is intended for service-booking conversations involving appliance or repair requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send a user's phone number and repair description to Suning's production service. <br>
Mitigation: Confirm the phone number, repair description, and user intent before submitting the reservation. <br>
Risk: The external reservation service may require additional validation or login that the skill cannot complete by itself. <br>
Mitigation: Tell the user when additional verification is needed and direct them to complete the booking through Suning's official flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/miantiaor/suning-bangke) <br>
- [Suning Bangke reservation endpoint](https://asapps.suning.com/asapps/mcp/serviceReserveNew) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a POST request containing a phone number and service description after user confirmation.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
