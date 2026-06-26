## Description: <br>
腾讯出行服务叫车助手，帮助用户发起打车、快捷通勤叫车、查询订单、取消订单、查看司机位置，并引导完成 token 和常住城市配置。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to coordinate Tencent ride-service workflows through an agent, including address confirmation, fare estimation, ride ordering, order status checks, cancellation, driver-location lookup, and account token setup. The skill is suited to users who are comfortable giving the agent a ride-service token and confirming trip details before booking. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a stored Tencent ride-service token to create, cancel, and query real ride orders. <br>
Mitigation: Install only from a trusted publisher, keep the token private, and require explicit confirmation of pickup, dropoff, price, and vehicle choice before order creation. <br>
Risk: Sensitive location, address shortcut, ride-state, and token data may be persisted under local tms-takecar configuration files. <br>
Mitigation: Treat the local configuration directory as sensitive, restrict local file access, and delete saved token or ride-state data when no longer needed. <br>
Risk: Shortcut phrases such as commute or saved-address requests can enter ride workflows from broad everyday language. <br>
Mitigation: Use clear intent checks for shortcut phrases and confirm trip details before any booking or cancellation action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tencent-adm/tencen-ride-skill) <br>
- [Quick Start workflow](references/quick-start-workflow.md) <br>
- [API contract](references/api-contract.md) <br>
- [Ride workflow](references/takecar-workflow.md) <br>
- [Order workflow](references/order-workflow.md) <br>
- [Shortcut workflow](references/short-cut-workflow.md) <br>
- [Error handling workflow](references/error_handling.md) <br>
- [State schema](references/state-schema.md) <br>
- [Address schema](references/addr-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with inline shell commands and JSON-backed workflow outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local Python scripts that call Tencent ride-service APIs and read or write local token, address, and ride-state configuration files.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
