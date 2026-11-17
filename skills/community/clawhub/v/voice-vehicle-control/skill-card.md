## Description:

语音控制车辆助手，支持启动熄火、车窗门锁、方向控制、状态查询与场景模式；适用于"帮我发动汽车"、"打开回家模式"或"查询电量"等语音交互场景

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamling](https://clawhub.ai/user/jamling)

### License/Terms of Use:

MIT-0

## Use Case:

Drivers and vehicle-assistant developers use this skill to turn multilingual voice or text requests into vehicle control commands, status queries, scenario executions, and natural-language feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote physical vehicle actions such as unlocking, engine start or stop, window and sunroof movement, and seat movement can affect occupant and bystander safety.

Mitigation: Limit use to trusted vehicles and authenticated users, and require explicit confirmation, vehicle-state checks, occupant safety checks, cancellation paths, and logging before sensitive actions.

Risk: Vehicle status and location queries can expose sensitive user or vehicle information.

Mitigation: Require user consent and authenticated sessions for status or location access, and return only the information needed for the requested task.

Risk: Multi-action scenarios can compound a mistaken intent classification or unsafe command ordering.

Mitigation: Confirm scenario intent before execution, check dependencies and vehicle state before each command, and use documented failure handling such as rollback, stop, or manual user guidance.

## Reference(s):

- [车辆控制协议](references/vehicle-protocol.md)
- [场景配置规范](references/scenario-config.md)
- [JSON Schema Draft 7](http://json-schema.org/draft-07/schema#)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [Markdown with JSON command and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces vehicle control commands, status query payloads, scenario execution payloads, and multilingual user feedback.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
