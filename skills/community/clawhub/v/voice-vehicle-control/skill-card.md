## Description: <br>
语音控制车辆助手，支持启动熄火、车窗门锁、方向控制、状态查询与场景模式；适用于"帮我发动汽车"、"打开回家模式"或"查询电量"等语音交互场景 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jamling](https://clawhub.ai/user/jamling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Drivers or vehicle-app teams use this skill to parse multilingual voice or text requests into vehicle control commands, status queries, and scene executions with natural-language feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle control actions can affect a real car if connected to a live vehicle API without sufficient boundaries. <br>
Mitigation: Use only a trusted, scoped vehicle API and require explicit confirmation for every control action and scene. <br>
Risk: Status queries and control actions may need different authorization levels. <br>
Mitigation: Separate status-only access from control access and protect tokens outside the skill. <br>
Risk: Batch scene execution can leave the vehicle in a partial state if a command fails. <br>
Mitigation: Verify vehicle state checks, audit logging, and rollback or stop behavior before deployment. <br>


## Reference(s): <br>
- [车辆控制协议](artifact/references/vehicle-protocol.md) <br>
- [场景配置规范](artifact/references/scenario-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON command payload examples and natural-language feedback] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces vehicle control, status query, and scenario execution payloads; requires vehicle API authorization and safety checks outside the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
