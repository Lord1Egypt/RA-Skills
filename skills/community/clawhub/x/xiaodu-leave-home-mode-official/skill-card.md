## Description: <br>
基于已安装的 xiaodu-control-official 编排离家场景，当用户准备出门时复用现有脚本关闭小度智能屏和小度 IoT 设备、汇总天气、日历和提醒事项，并帮助确认出门前是否遗漏事项。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dueros-mcp](https://clawhub.ai/user/dueros-mcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with an existing xiaodu-control-official setup use this skill to run a leave-home routine that coordinates device shutdown, weather, calendar, and reminder checks. The skill is intended for smart-home departure workflows where users need a concise safety and status summary before leaving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect smart-home devices and scenes through an existing xiaodu-control-official setup. <br>
Mitigation: Install only in trusted Xiaodu environments and review which scenes and devices the underlying setup can control before use. <br>
Risk: The skill may read or summarize calendar, reminder, and weather information in shared spaces. <br>
Mitigation: Avoid broad trigger phrases or spoken summaries where household members or visitors should not hear schedule and reminder details. <br>
Risk: Saved preferences could reduce future confirmation prompts, including preferences related to locks. <br>
Mitigation: Review saved preferences regularly and avoid storing preferences that skip confirmation for lock-related actions unless the user explicitly accepts that behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dueros-mcp/xiaodu-leave-home-mode-official) <br>
- [Usage notes](references/usage-notes.md) <br>
- [Test cases](references/test-cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and natural-language status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces smart-home orchestration guidance and user-facing summaries; relies on the adjacent xiaodu-control-official setup for device access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
